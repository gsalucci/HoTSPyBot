import multiprocessing
from Utils.CV.ColorFinder import ColorFinder
import time
import numpy as np
import cv2
import mss
class MapScanner(multiprocessing.Process):
    class MapObj:
        def __init__(self,keypoint):
            self.keypoint = keypoint
            self.x = int(keypoint.pt[0])
            self.y = int(keypoint.pt[1])
            self.size = keypoint.size
            self.center = (self.x , self.y)
            self.rect = ( ( int(self.x - self.size/5), int(self.y - self.size/5) ) , ( int(self.x+self.size/5), int(self.y+self.size/5) ) )
    
    def __init__(self,gameStateObject,logObject,mapObj,state):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.mapObj = mapObj
        self.gameStateObject = gameStateObject
        self.log = logObject.log
        self.name = 'MapScanner'
        self.state = state
        self.log(f"[ {self.name} ] Initialized")
    
    def run(self):
        self.log(f"[ {self.name} ] Running")
        while not self.exit.is_set():
            while self.state.getState() == "inGame" and not self.exit.is_set():
                with mss.mss() as sct:
                    img = cv2.cvtColor(np.array(sct.grab(self.mapObj["box"])),cv2.COLOR_BGRA2BGR)
                    mapMask = np.zeros_like(self.colorFilter(img))
                    imgBlurred = cv2.GaussianBlur(img, (5, 5), 0)
                    rp,gp,bp,yp = self.colorFilterMap(imgBlurred)
                    #create map mask
                    allPoints = []
                    for p in rp:
                        allPoints.append(p["center"])
                    for p in bp:
                        allPoints.append(p["center"])
                    xOffset = 50
                    yOffset = 20
                    #print(f"ALLPOINTS: {allPoints}")
                    minX = min(allPoints, key = lambda t: t[0])[0] - xOffset
                    minY = min(allPoints, key = lambda t: t[1])[1] - yOffset
                    maxX = max(allPoints, key = lambda t: t[0])[0] + xOffset
                    maxY = max(allPoints, key = lambda t: t[1])[1] + yOffset
                    #print(f"minX: {minX} minY: {minY} maxX: {maxX} maxY: {maxY}")
                    h = maxY - minY
                    w = maxX - minX
                    verts = np.array([[minX, minY+int(h/2)],[minX + int(w/3),minY],[minX + int(2*w/3),minY],[maxX, minY + int(h/2)],[minX + int(2*w/3),maxY],[minX + int(w/3),maxY],[minX,minY+ int(h/2)]],"int32")
                    #print(f"VERTS: {verts}")
                    cv2.fillConvexPoly(mapMask, verts, (255,255,255))
                    

                    roughMaskedMap = cv2.bitwise_and(img,img,mask = cv2.cvtColor(mapMask,cv2.COLOR_BGR2GRAY))
                    
                    blue = self.colorFilter(img,np.array(self.mapObj["colors"]["blueLower"]),np.array(self.mapObj["colors"]["blueUpper"]))
                    red = self.colorFilter(img,np.array(self.mapObj["colors"]["redLower"]),np.array(self.mapObj["colors"]["redUpper"]))
                    violet = self.colorFilter(roughMaskedMap, np.array(self.mapObj["colors"]["violetLower"]),np.array(self.mapObj["colors"]["violetUpper"]))
                    violet = cv2.add(cv2.add(red,blue),violet)
                    violet = cv2.cvtColor(violet,cv2.COLOR_BGR2GRAY)

                    cnt ,hi = cv2.findContours(violet,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                    for c in cnt:
                        cv2.fillConvexPoly(violet,c,(255,255,255))
                    violet = cv2.erode(violet, np.ones((5,5),np.uint8)/25,iterations = 1)
                    
                    mapMask = violet

                    gCount = 0
                    gXsum = 0
                    gYsum = 0
                    gSsum = 0
                    gP = {}#self.MapObj(cv2.KeyPoint(0,0,0))
                    gSampleThresh = 10
                    scanCondition = True
                    fpsSum=0
                    fpsTime=0
                    count=0

                    while self.state.getState() == "inGame" and not self.exit.is_set():
                        last_time = time.time()
                        img = cv2.cvtColor(np.array(sct.grab(self.mapObj["box"])),cv2.COLOR_BGRA2BGR)
                        maskedMap = cv2.bitwise_and(img,img,mask = mapMask)
                        blurredMaskedMap = cv2.GaussianBlur(maskedMap, (5, 5), 0)
                        redPoints, greenPoints, bluePoints, yellowPoints = self.colorFilterMap(blurredMaskedMap)
                        if greenPoints:
                            for p in greenPoints:
                                gXsum += p["x"]
                                gYsum += p["y"]
                                gSsum += p["size"]
                                gCount += 1
                                gP["x"] = int(gXsum / gCount)
                                gP["y"] = int(gYsum / gCount)
                                gP["size"] = int(gSsum / gCount)

                            gCount = 0
                            gXsum = 0
                            gYsum = 0
                            gSsum = 0
                            self.gameStateObject.setGameStateKeyValue("greenPoint",gp)
                        
                        self.gameStateObject.setGameStateKeyValue("redPoints",redPoints)
                        self.gameStateObject.setGameStateKeyValue("bluePoints",bluePoints)
                        self.gameStateObject.setGameStateKeyValue("yellowPoints",yellowPoints)

                        #self.log(f"{self.name}: GreenPoint:\t {len(gp)}, RedPoints:\t{len(redPoints)}, BluePoints:\t {len(bluePoints)}, yellowPoints:\t{len(yellowPoints)}")
                        
                        fps = 1/(time.time()-last_time)
                        fpsSum = fpsSum + fps
                        count = count + 1
                        if time.time() - fpsTime >= 10:
                            self.gameStateObject.setGameStateKeyValue("mapScanFPS",fpsSum/count)
                            # self.log(f"{self.name}:\tAverage FPS (10s): {fpsSum/count}")
                            fpsTime = time.time()
                            count = 0
                            fpsSum=0
                        
                        final = np.zeros_like(img)
                        if gP:
                            cv2.rectangle(final,(int(gP["x"] - gP["size"]/2), int(gP["y"] - gP["size"]/2)),(int(gP["x"] + gP["size"]/2), int(gP["y"] + gP["size"]/2)), (0,255,0),2)
                        for p in redPoints:
                            cv2.rectangle(final, p["rect"][0],p["rect"][1], (0,0,255),2)
                        
                        for p in bluePoints:
                            cv2.rectangle(final, p["rect"][0],p["rect"][1], (255,0,0),2)
                        for p in yellowPoints:
                            cv2.rectangle(final, p["rect"][0],p["rect"][1], (0,255,255),2)
                        
                        cv2.imshow("VIOLET",violet)
                        cv2.imshow("filled",violet)
                        cv2.imshow("roughMaskedMap", roughMaskedMap)
                        cv2.imshow("mapMask",mapMask)

                        cv2.imshow("COLOR FILTERING RESULT",final)
                        summed = cv2.addWeighted(maskedMap,0.4,final,0.6,0)
                        cv2.imshow("SUM",summed)
                        if cv2.waitKey(25) & 0xFF == ord("q") or self.state.getState() != 'inGame' or self.exit.is_set():
                            self.log(f"[ {self.name} ] destorying all windows")
                            cv2.destroyAllWindows()
            pass
        self.log(f"[ {self.name} ] Shutdown complete")

    def shutdown(self):
        self.log(f"[ {self.name} ] Shutdown initiated")
        self.exit.set()
    
    def colorFilter(self,img, lower = np.array([0,0,0]), upper= np.array([255,255,255])):
        filtered_color = cv2.bitwise_and(img,img,mask = cv2.inRange(img, lower, upper))
        _,mask = cv2.threshold(filtered_color,1,255,cv2.THRESH_BINARY)
        return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((10,10),np.float32)/10) #espansione

    def colorFilterMap(self,img):
        red = self.colorFilter(img,np.array(self.mapObj["colors"]["redLower"]),np.array(self.mapObj["colors"]["redUpper"]))
        green = self.colorFilter(img,np.array(self.mapObj["colors"]["greenLower"]),np.array(self.mapObj["colors"]["greenUpper"]))
        blue = self.colorFilter(img,np.array(self.mapObj["colors"]["blueLower"]),np.array(self.mapObj["colors"]["blueUpper"]))
        yellow = self.colorFilter(img,np.array(self.mapObj["colors"]["yellowLower"]),np.array(self.mapObj["colors"]["yellowUpper"]))

        return self.findPoints(red,1,1000), self.findPoints(green,1,100), self.findPoints(blue,1,1000), self.findPoints(yellow,1,1000)

    def findPoints(self,img, minArea=10, maxArea=100,circularity = False):
        mask = img
        params = cv2.SimpleBlobDetector_Params()
        params.minThreshold = 1
        params.maxThreshold = 255
        
        params.filterByArea = True
        params.minArea = minArea
        params.maxArea = maxArea
        
        params.filterByCircularity = circularity
        params.filterByInertia = False
        params.filterByConvexity = False
        params.filterByColor = False
        params.blobColor = 255
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3:
            detector = cv2.SimpleBlobDetector(params)
        else: 
            detector = cv2.SimpleBlobDetector_create(params)

        pts = []    
        for k in detector.detect(mask):
            pts.append({"x":k.pt[0],"y":k.pt[1],"size":k.size,"center":(k.pt[0] , k.pt[1]), "rect":( ( int(k.pt[0] - k.size/5), int(k.pt[1] - k.size/5) ) , ( int(k.pt[0]+k.size/5), int(k.pt[1]+k.size/5) ) )})
            #pts.append(self.MapObj(k))
        return pts
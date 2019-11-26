import cv2
import mss
import numpy as np
class ColorFinder():
    def __init__(self):
        pass
    def checkColor(self, zone, color, sens, retPoints = False,vis = False):
        s = int(sens / 2)
        lower = np.array([i - s for i in color])
        upper = np.array([i + s for i in color])
        color = np.array(color)
        minArea = 1
        maxArea = 1000
        circularity = False

        with mss.mss() as sct:
            img = cv2.cvtColor(np.array(sct.grab(zone)), cv2.COLOR_BGRA2BGR) #sct.grab(zone)
            #color filtering
            filtered_color = cv2.bitwise_and(img,img,mask = cv2.inRange(img, lower, upper))
            _,mask = cv2.threshold(filtered_color,1,255,cv2.THRESH_BINARY)
            masked = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((10,10),np.float32)/10) #espansione
            #blob detection
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
            # Create a detector with the parameters
            ver = (cv2.__version__).split('.')
            if int(ver[0]) < 3:
                detector = cv2.SimpleBlobDetector(params)
            else: 
                detector = cv2.SimpleBlobDetector_create(params)
            points = []
            keypoints = []    
            for k in detector.detect(masked):
                keypoints.append(k)
                points.append([k.pt[0],k.pt[1]])
            #print(f"keypoints: {keypoints}, points: {points}")

            if vis:
                cv2.imshow("Ori", img)
                cv2.imshow("filtered_color", filtered_color)
                cv2.imshow("mask", mask)
                cv2.imshow("masked", masked)
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
            
            if retPoints:
                return keypoints, points
            else:
                if len(keypoints) > 0:
                    return True
                else: 
                    return False
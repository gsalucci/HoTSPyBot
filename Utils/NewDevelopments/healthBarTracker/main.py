import numpy as np
import cv2
import mss
import time
from TrackableEntity import TrackableEntity, Hero
from EntityManager import EntityManager
import traceback
minContourAreaThreshold = 1
minAspectRatioThreshold = 350
def nothing(x):
    pass

def getAspectRatio(w,h):
    return float(w) / h

class ColorNames:
    BLUE = "blue"
    RED = "red"
    GREEN = "green"

def drawFound(c, color,image, filterManaBar = False):
    if(cv2.contourArea(c) >= minContourAreaThreshold):
        x,y,w,h = cv2.boundingRect(c)
        aspectRatio = getAspectRatio(w,h)
        if(aspectRatio >= minAspectRatioThreshold):
            if filterManaBar:
                if h >= 4:
                    if h >= 8 and h <= 16:
                        hero = Hero(x,y,"Hero Blue")
                        hero.color = color
                        hero.drawRectangle(image)
                    # cv2.drawContours(original,[c], 0, color, 2)
                    else:
                        cv2.putText(original, "Entity", (x+50,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            else: 
                # cv2.putText(original, str(h), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                # cv2.drawContours(original,[c], 0, color, 2)
                if h >= 8 and h <= 16:
                    hero = Hero(x,y,"Hero Red")
                    hero.color = color
                    hero.drawRectangle(image)
                else:
                    cv2.putText(original, "Entity", (x+50,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)                

def filterContours(contours,filterManaBar=False):
    mc = contours
    toPop = []
    for i,c in enumerate(contours):
        if(cv2.contourArea(c) >= minContourAreaThreshold):
            x,y,w,h = cv2.boundingRect(c)
            aspectRatio = getAspectRatio(w,h)
            if(aspectRatio >= minAspectRatioThreshold):
                if filterManaBar:
                    if h >= 4:
                        pass
                    else:
                        toPop.append(i)
            else:
                toPop.append(i)
        else:
            toPop.append(i)
    for i in sorted(toPop,reverse=True):
        mc.pop(i)
    return mc

wName="Controls"
wImageName="Image"
entityManager = EntityManager()
lower = np.array([162,183,186], dtype="uint8")
upper = np.array([179, 255, 219], dtype="uint8")
lowerBlue = np.array([77, 188, 167], dtype="uint8")
upperBlue = np.array([123, 255, 255], dtype="uint8")
# lower = np.array([158, 204, 4], dtype="uint8")
# upper = np.array([179, 255, 255], dtype="uint8")
# lowerBlue = np.array([73, 50, 182], dtype="uint8")
# upperBlue = np.array([109, 219, 255], dtype="uint8")
lowerGreen = np.array([36 ,145,189], dtype="uint8")
upperGreen = np.array([82,243,223], dtype="uint8")
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
cv2.namedWindow(wName,cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('AspectRatio',wName,1,1000,nothing)
cv2.setTrackbarPos('AspectRatio', wName, minAspectRatioThreshold)
cv2.createTrackbar('minArea',wName,1,1000,nothing)
cv2.setTrackbarPos('minArea', wName, minContourAreaThreshold)
# cv2.createTrackbar('orientationDelta',wName,0,1000,nothing)
# cv2.setTrackbarPos('orientationDelta', wName, 100)
with mss.mss() as sct:
    while 1:
        last_time = time.time()
        image = cv2.cvtColor(np.array(sct.grab({"top":120,"left":0,"width":1920,"height":900})), cv2.COLOR_BGRA2BGR)
        original = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(image, lower, upper)
        maskBlue = cv2.inRange(image, lowerBlue, upperBlue)

        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        closingBlue = cv2.morphologyEx(maskBlue, cv2.MORPH_CLOSE, kernel, iterations=1)


        cnts = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cntsBlue = cv2.findContours(closingBlue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cntsBlue = cntsBlue[0] if len(cntsBlue) == 2 else cntsBlue[1]

        minAspectRatioThreshold = cv2.getTrackbarPos('AspectRatio',wName) / 100
        # orientationDelta = cv2.getTrackbarPos('orientationDelta',wName) / 100
        # shapeFactor = cv2.getTrackbarPos('shapeFactor',wName) / 100
        minContourAreaThreshold = cv2.getTrackbarPos('minArea',wName)


        # for c in cntsBlue:
        #     drawFound(c,(255, 0, 0),original,True)
        # for c in cnts:
        #     drawFound(c, (0,0,255),original)
                
        redCts = filterContours(cnts)
        blueCts = filterContours(cntsBlue)
        # print("redEntitiesLen",len(redCts),"blueEntitiesLen",len(blueCts))

        redEntities = entityManager.updateEntities(redCts,mask,ColorNames.RED)
        blueEntities = entityManager.updateEntities(blueCts,maskBlue,ColorNames.BLUE)
        # redEntities = entityManager.updateEntities(redCts,cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR),ColorNames.RED)
        # blueEntities = entityManager.updateEntities(blueCts,cv2.cvtColor(maskBlue,cv2.COLOR_GRAY2BGR),ColorNames.BLUE)

        # allEntities = entityManager.entities[ColorNames.RED]
        # allEntities.extend(entityManager.entities[ColorNames.BLUE])

        for rE in redEntities:
            rE.drawRectangle(original)

        for bE in blueEntities:
            bE.drawRectangle(original)

        # for e in allEntities:
        #     e.drawRectangle(original)

        # print(f"allEntities",allEntities)

        cv2.imshow(wImageName,original)
        # cv2.imshow("mask",closing)
        # cv2.imshow("maskBlue",closingBlue)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            for rE in redEntities:
                rE.deleteTracker()

            for bE in blueEntities:
                bE.deleteTracker()
            break
exit(0)
import math
import cv2
import time
class TrackableEntity:

    def __init__(self, x,y, width, height, xOffset=42, yOffset=42, name="Entity",colorName = "nd"):
        self.color = (127,127,127)
        self.x = x
        self.y = y
        self.name = name
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.width = width
        self.height = height
        self.hitBox = self.computeHitbox(x,y)
        self.direction = 0
        self.speed = 0
        self.tracker = None
        self.time = time.time()
        self.timeDiff = 0

    def computeCenter(self, hitBox=None):
        if hitBox == None:
            hitBox = self.hitBox
        return (hitBox[top]+hitBox["height"]/2, hitBox["left"]+hitBox["width"]/2)
    
    def getPosition(self):
        return (self.x,self.y)

    def getDirection(self):
        return self.direction
        
    def getSpeed(self):
        return self.speed

    def getNextCenter(self):
        y = self.y + (self.speed * sin(self.direction))
        x = self.x + (self.speed * cos(self.direction))
        return self.computeCenter(self.computeHitbox(x,y))

    def setPosition(self,x,y):
        self.x0 = self.x
        self.y0 = self.y
        self.x = x
        self.y = y
        self.hitBox = self.computeHitbox(x,y)
        self.setDirection(x,y)

    def setDirection(self,x,y):
        self.speed = math.sqrt((self.x0 - x)**2 + (self.y0 - y)**2)
        if self.speed > 0:
            self.direction = math.asin( abs(self.y0 - y) / self.speed ) 

    def computeHitbox(self, x, y):
        return {"top":y+self.yOffset, "left":x+self.xOffset, "width": self.width, "height":self.height }

    def drawRectangle(self, image):
        cv2.putText(image, "{:.2f}".format(self.timeDiff), (self.hitBox["left"],self.hitBox["top"] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, self.color, 2)
        return cv2.rectangle(image, (self.hitBox["left"],self.hitBox["top"]),(self.hitBox["left"]+self.hitBox["width"],self.hitBox["top"]+self.hitBox["height"]),self.color,2)

    def setTracker(self, tracker, image, bbox):
        self.tracker = tracker
        try:
            self.tracker = tracker
            return self.tracker.init(image,bbox)
        except Exception:
            self.tracker = None
            print("cannot create tracker")
        


    def updateTracker(self, image):
        self.timeDiff = time.time() - self.time
        if self.tracker:
            try:
                return self.tracker.update(image)
            except Exception:
                print("Tracker exception")
                return False,False
            # return self.tracker.update(image)
        else:
            return False,False
    
    def deleteTracker(self):
        del self.tracker

    def getDistanceFromPoint(self, x, y):
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)

class Hero(TrackableEntity):
    def __init__(self, x,y,color=(250, 0, 233), name="Hero", colorName="nd"):
        self.x = x
        self.y = y
        self.xOffset=0
        self.yOffset=58
        self.width = 122
        self.height = 155
        super().__init__(x,y,self.width,self.height,self.xOffset, self.yOffset,name)
        self.color = color
        self.colorName = colorName
        self.name = name+" "+colorName


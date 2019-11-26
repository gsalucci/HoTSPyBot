import queue
class State():
    def __init__(self):
        self.state = "undefined"
        self.side = "undefined"
        self.speed = 0
        self.maxSize = 13
        self.stateQ = queue.Queue(maxsize = self.maxSize)

        self.speedCount = 0

    def getState(self):
        return self.state
    def setState(self,state):
        if self.stateQ.qsize() >= self.maxSize:
            self.stateQ.get()
        self.stateQ.put(state)
        self.state = max(self.stateQ.queue)
    def getSide(self):
        return self.side
    def setSide(self,side):
        self.side = side
    def getSpeed(self):
        if self.speedCount > 0:
            return self.speed/self.speedCount
        return self.speed
        # return self.speed
    def setSpeed(self,speed):
        self.speed += speed
        self.speedCount += 1
        # self.speed = speed
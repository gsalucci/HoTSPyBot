import multiprocessing
from Utils.CV.ColorFinder import ColorFinder
class HealthBarScanner(multiprocessing.Process):

    def __init__(self,gameStateObject,logObject,hpBar,state):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.colorFinder = ColorFinder()
        self.sampleNum = 8
        self.hpBar = hpBar
        self.gameStateObject = gameStateObject
        self.log = logObject.log
        self.name = 'HealthBarScanner'
        self.state = state
        self.log(f"[ {self.name} ] Initialized")
    def run(self):
        self.log(f"[ {self.name} ] Running")
        sampleWidth = int(self.hpBar["box"]["width"] / self.sampleNum)
        boxes = []
        for i in range(self.sampleNum):
            boxes.append({"top":self.hpBar["box"]["top"],"left":self.hpBar["box"]["left"] + (sampleWidth * i),"width":sampleWidth,"height":self.hpBar["box"]["height"]})
        sens = 50
        while not self.exit.is_set():
            while self.state.getState() == "inGame" and not self.exit.is_set():
                hp = 0
                for i in range(self.sampleNum):
                    if self.colorFinder.checkColor(boxes[i],self.hpBar["hpColor"],sens) or self.colorFinder.checkColor(boxes[i],self.hpBar["shieldColor"],sens):
                        hp = hp + 1
                hp = int((hp / self.sampleNum)* 100)
                self.gameStateObject.setGameStateKeyValue("hp",hp)    
            pass
        self.log(f"[ {self.name} ] Shutdown complete")

    def shutdown(self):
        self.log(f"[ {self.name} ] Shutdown initiated")
        self.exit.set()


import multiprocessing
from Utils.CV.TemplateFinder import TemplateFinder
from Utils.CV.ColorFinder import ColorFinder
class StateFinder(multiprocessing.Process):

    def __init__(self, stateObject, log, settings, **kwargs):
        multiprocessing.Process.__init__(self)
        self.name = "StateFinder"
        self.stateObject = stateObject
        self.exit = multiprocessing.Event()
        self.log = log.log
        self.templateFinder = TemplateFinder()
        self.colorFinder = ColorFinder()
        self.settings = settings
        self.log(f"[ {self.name} ] Initialized")

    def run(self):
        self.log(f"[ {self.name} ] Running")
        while not self.exit.is_set():
            if self.checkClientCommon():
                if self.checkLobby():
                    self.stateObject.setState("lobby")
                elif self.checkLeave():
                    self.stateObject.setState("leave")
                elif self.checkSearching():
                    self.stateObject.setState("searching")
                elif self.checkHome():
                    self.stateObject.setState("home")
                # else:
                #     self.stateObject.setState("undefined")                                
            elif self.checkRejoin():
                self.stateObject.setState("rejoin")
            elif self.checkThanks():
                self.stateObject.setState("thanks")
            elif self.checkLobby():
                self.stateObject.setState("roster")
            elif self.checkMVP():
                self.stateObject.setState("mvp")
            elif self.checkLoading():
                self.stateObject.setState("loading")
            elif self.checkInGame():
                self.stateObject.setState("inGame")
            # else:
            #     self.stateObject.setState("undefined")
        self.log(f"[ {self.name} ] Shutdown complete")

    def shutdown(self):
        self.log(f"[ {self.name} ] Shutdown initiated")
        self.exit.set()

    def checkClientCommon(self):
        l= ["coin","logo","gem"]
        th = 0.9
        return self.findTemplateInBox("clientCommon",l,th)

    def checkLobby(self):
        l = ["hero", "readyBL","readyBR","readyTR","readyTL"]
        th = 0.9
        return self.findTemplateInBox("lobby",l,th)

    def checkLeave(self):
        l= ["btnOne","btnTwo"]
        th = 0.9
        retval = self.findTemplateInBox("leave",l,th)
        if retval: self.stateObject.setSide("undefined")
        return  retval

    def checkSearching(self):
        l= ["TL","BR"]
        th = 0.9
        return self.findTemplateInBox("searching",l,th)

    def checkRejoin(self):
        l= ["btnOneTL","btnOneBR","btnTwoTL","btnTwoBR"]
        th = 0.9
        return self.findTemplateInBox("rejoin",l,th)

    def checkThanks(self):
        l= ["question","btnTL","btnBR"]
        th = 0.9
        return self.findTemplateInBox("thanks",l,th)
    
    def checkHome(self):
        l= ["ico"]
        th = 0.9
        return self.findTemplateInBox("home",l,th)

    def checkMVP(self):
        l1= ["arrowB"]
        l2= ["arrowR"]
        th = 0.9
        return self.findTemplateInBox("mvp",l1,th) or self.findTemplateInBox("mvp",l2,th)

    def checkInGame(self):
        #l=["exa","exa1","exa2","exa3"]
        l=["exa1","exa2","exa3"]
        th = 0.9
        return self.findTemplateInBox("inGame",l,th)

    def findTemplateInBox(self, category, tempList, th, vis = False):
        for l in tempList:
            if not self.templateFinder.find(self.settings[category][l]["box"],self.settings[category][l]["template"],th,vis):
                return False
        return True

    def checkLoading(self):
        sens = 50

        left = self.colorFinder.checkColor(self.settings["loading"]["left"],self.settings["loading"]["color"],sens) 
        right = self.colorFinder.checkColor(self.settings["loading"]["right"],self.settings["loading"]["color"],sens)

        #if self.stateObject.getSide() == "undefined":
        if left: self.stateObject.setSide("left")
        elif right: self.stateObject.setSide("right")
        return left or right
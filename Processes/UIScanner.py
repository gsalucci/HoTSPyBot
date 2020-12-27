import multiprocessing
from Utils.CV.ColorFinder import ColorFinder
from Utils.CV.OCR import OCR
import mss
import cv2
import numpy as np
class UIScanner(multiprocessing.Process):

    def __init__(self,gameStateObject,logObject,state, uiObject):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.gameStateObject = gameStateObject
        self.uiObject=uiObject
        self.log = logObject.log
        self.name = 'UIScanner'
        self.state = state
        self.log(f"[ {self.name} ] Initialized")
    def run(self):
        self.log(f"[ {self.name} ] Running")
        while not self.exit.is_set():
            while self.state.getState() == "inGame" and not self.exit.is_set():
                with mss.mss() as sct:
                    leftImg = cv2.cvtColor(np.array(sct.grab(self.uiObject["level"]["left"]["box"])),cv2.COLOR_BGRA2BGR)
                    rightImg = cv2.cvtColor(np.array(sct.grab(self.uiObject["level"]["right"]["box"])),cv2.COLOR_BGRA2BGR)
                    leftText, leftProcessedImage = OCR.getText(leftImg)
                    rightText, rightProcessedImage = OCR.getText(rightImg)
                    # self.log(f"[ {self.name} ] Left Level: {leftText} Right Level: {rightText}")
                    self.gameStateObject.setGameStateKeyValue("level",{"left": leftText, "right":rightText})
                    self.gameStateObject.setMapImage("levelLeft",leftProcessedImage)
                    self.gameStateObject.setMapImage("levelRight",rightProcessedImage)
            pass
        self.log(f"[ {self.name} ] Shutdown complete")

    def shutdown(self):
        self.log(f"[ {self.name} ] Shutdown initiated")
        self.exit.set()


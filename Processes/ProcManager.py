from multiprocessing.managers import BaseManager
from Utils.SharedObjects.Keyboard import Keyboard
from Utils.SharedObjects.Log import Log
from Utils.SharedObjects.GameState import GameState
from Utils.SharedObjects.ServerObject import ServerObject
from Utils.SharedObjects.State import State
from Processes.HeathBarScanner import HealthBarScanner
from Processes.KeyboardListener import KeyboardListener
from Processes.MapScanner import MapScanner
from Processes.UIScanner import UIScanner
from Processes.StateFinder import StateFinder
from Processes.SocketServer import SocketServer
class ProcManager():
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.name = "ProcManager"
        self.classes = {
            'Keyboard':     Keyboard,
            'Log':          Log,
            'State':        State,
            'GameState':    GameState,
            # 'ServerObject': ServerObject
        }
        for k, v in self.classes.items():
            BaseManager.register(k,v)
        
        self.manager = BaseManager()
        self.manager.start()

        self.sharedObjectsInstances = {
            'keyboard':     self.manager.Keyboard(),
            'log':          self.manager.Log(),
            'state':        self.manager.State(),
            'gameState':    self.manager.GameState(),
            # 'serverObject': self.manager.ServerObject(),
        }

        self.procList = {
            'HealthBarScanner':     HealthBarScanner(self.sharedObjectsInstances["gameState"],self.sharedObjectsInstances["log"],self.settings["inGameResources"]["hpBar"],self.sharedObjectsInstances["state"]),
            'KeyboardListener':     KeyboardListener(self.sharedObjectsInstances["keyboard"], self.sharedObjectsInstances["log"]),
            'MapScanner':           MapScanner(self.sharedObjectsInstances["gameState"],self.sharedObjectsInstances["log"],self.settings["inGameResources"]["map"],self.sharedObjectsInstances["state"]),
            'UIScanner':            UIScanner(self.sharedObjectsInstances["gameState"],self.sharedObjectsInstances["log"],self.sharedObjectsInstances["state"],self.settings["inGameResources"]["ui"]),
            'StateFinder':          StateFinder(self.sharedObjectsInstances["state"],self.sharedObjectsInstances["log"],self.settings["stateFindingResources"]),
            # 'SocketServer':         SocketServer(self.sharedObjectsInstances["serverObject"],self.sharedObjectsInstances["log"])
        }
        self.log = self.sharedObjectsInstances["log"].log
        self.log(f"[ {self.name} ] All good!")

    def start(self,name):
        self.procList[name].start()

    def stop(self,name):
        self.procList[name].shutdown()
    
    def stopAll(self):
        for i in self.procList:
            self.procList[i].shutdown()

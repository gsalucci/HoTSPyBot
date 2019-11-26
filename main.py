import Utils.RuntimeHelpers.SettignsManager as settingsManager
from Processes.ProcManager import ProcManager
import Utils.RuntimeHelpers.Stopwatch as stopwatch
ver = 0.1
settings = None
def main():
    print(f"Welcome to HoTSPyBot {ver}")
    settings = settingsManager.init()
    procManager = ProcManager(settings)
    log = procManager.sharedObjectsInstances["log"].log
    log("[ Main ] Enter the lobby and press F5 to start the bot, F6 to stop it!")

    procManager.start("KeyboardListener")

    while not procManager.sharedObjectsInstances["keyboard"].getAction() == "Start":
        pass
    
    for k in procManager.procList:
        if k != "KeyboardListener":
            procManager.procList[k].start()

    while not procManager.sharedObjectsInstances["keyboard"].getAction() == "Stop":
        stopwatch.start()
        log(f"[ Main ] {stopwatch.stop()}\t {procManager.sharedObjectsInstances['state'].getState()}\t{procManager.sharedObjectsInstances['state'].getSide()}\t{procManager.sharedObjectsInstances['gameState'].getGameStateValue('hp')}")
    
    procManager.stopAll()
    stillRunning = True
    while stillRunning:
        s = False
        for p in procManager.procList:
            s = s or procManager.procList[p].is_alive()
        if not s:
            stillRunning = False
    exit(0)
if __name__ == '__main__':
    main()
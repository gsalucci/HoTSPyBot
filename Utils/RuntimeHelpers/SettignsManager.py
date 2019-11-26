import json
import pickle
from pathlib import Path
settingsFile =      Path(Path(__file__).parents[1] / 'settings.json')
templatesFile =     Path(Path(__file__).parents[1] / 'templates.pickle')

def checkFirstRun(settings):
    if settings["resolution"] == "undefined":
        return True
    return False

def firstRun(settings):
    resString = input("[ SettingsManager ] Enter the inGame resolution ex 1920x1080> ")
    if "x" in resString:
        settings["resolution"] = [int(i) for i in resString.split("x")]
        print(f"Res: {settings['resolution']}")
        print(f"Updating settings file")
        with open(settingsFile,"w") as f:
            json.dump(settings,f)
    else:
        print("resolution\'s dimensions should be separed by a \"x\"")
        firstRun()

def init():
    print("[ SettingsManager ] Loading settings...")
    with open(settingsFile) as f:
        settings = json.load(f)
        if checkFirstRun(settings):
            firstRun(settings)
    print("[ SettingsManager ] Loading templates...")        
    with open(templatesFile,"rb") as f:
        t = pickle.load(f)
        for k,v in t.items():
            for k1,v1 in v.items():
                settings["stateFindingResources"][k][k1]["template"] = t[k][k1]["template"] 
    return settings
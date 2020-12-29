import Utils.RuntimeHelpers.SettignsManager as settingsManager
from Processes.ProcManager import ProcManager
import Utils.RuntimeHelpers.Stopwatch as stopwatch
import asyncio
from aiohttp import web
import socketio
import threading
import eventlet
import time
import sys
import os
import json
import traceback
from dotenv import load_dotenv, find_dotenv
from enum import Enum

load_dotenv(find_dotenv())
static_files = {
    "/": {'filename': 'index.html', 'content_type': 'text/html'},
}

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

mgr = socketio.AsyncRedisManager(os.getenv("REDIS"))
sio = socketio.AsyncServer(client_manager=mgr)
app = web.Application()
sio.attach(app)
app.router.add_get('/', index)
httpServerEventLoop = asyncio.new_event_loop()
ver = 0.1
UIUpdateInterval = 0.1
settings = None
wst = None #WebSocketThread

class SocketMessageTypes(Enum):
    CONNECTED = "Connected"
    DISCONNECTED = "Disconnected"
    CONTROL = "Control"

class SocketMessageHandler():
    def __init__(self, settings, manager):
        self.settings = settings
        self.manager = manager
        self.name = 'SocketMessageHandler'

    def log(self,message):
        self._log = self.manager.sharedObjectsInstances["log"].log
        self._log(f"[ {self.name} ] {message}")
    
    def handleMessage(self,message):
        self.log(f"Received message: ( {message['type']} ) {message['message']} {message['data']}")
        if message["type"] == SocketMessageTypes.CONTROL.name:
            if message["message"] == "updateUIRate":
                global UIUpdateInterval
                UIUpdateInterval = message["data"]

def serve_app():
    asyncio.set_event_loop(httpServerEventLoop)
    try:
        web.run_app(app,host="0.0.0.0",port=3000)
    except Exception:
        print(f"HTTP Server EXCEPTION")
        traceback.print_exc()

async def main():
    settings = settingsManager.init()
    procManager = ProcManager(settings)
    global socketMessageHandler
    socketMessageHandler= SocketMessageHandler(settings,procManager)
    log = procManager.sharedObjectsInstances["log"].log
    log(f"[ Main ] Welcome to HoTSPyBot {ver}")
    procManager.start("KeyboardListener")
    log("[ Main ] Enter the lobby and press F5 to start the bot, F6 to stop it!")

    while not procManager.sharedObjectsInstances["keyboard"].getAction() == "Start":
        pass
    
    for k in procManager.procList:
        if k != "KeyboardListener":
            procManager.procList[k].start()

    async def updateUI():
        message = {"state":procManager.sharedObjectsInstances['state'].getState(),"side":procManager.sharedObjectsInstances['state'].getSide(),"gameState":procManager.sharedObjectsInstances['gameState'].getGameState(),"images":procManager.sharedObjectsInstances['gameState'].getMapImages(),"log":procManager.sharedObjectsInstances['log'].getLastMessage()}
        try:
            await mgr.emit('state', message)
            # print(f"{message}")
            with open('history.txt', 'a') as history:
                history.write(json.dumps(message)+'\n')
        except Exception:
            print("UpdateUI exception:")
            traceback.print_exc()

    lastTime = time.time()
    while not procManager.sharedObjectsInstances["keyboard"].getAction() == "Stop":
        stopwatch.start()
        if (time.time() - lastTime) >= UIUpdateInterval:
            lastTime = time.time()
            await updateUI()
        stopwatch.stop()

    updateUIThread.stop()
    procManager.stopAll()
    stillRunning = True
    while stillRunning:
        s = False
        for p in procManager.procList:
            s = s or procManager.procList[p].is_alive()
        if not s:
            stillRunning = False
    await app.shutdown()
    sys.exit(0)
    exit(0)

@sio.event
def connect(sid, environ):
    try:
        # socketMessageHandler.log(f"connected: {sid}")
        socketMessageHandler.handleMessage({"type":SocketMessageTypes.CONNECTED.name, "message":"Client connected", "data":sid})
    except NameError:
        pass

@sio.event
def disconnect(sid):
    try:
        socketMessageHandler.handleMessage({"type":SocketMessageTypes.DISCONNECTED.name, "message":"Client disconnected", "data":sid})
    except NameError:
        pass

@sio.event
def changeUIUpdateRate(sid, data):
    try:
        socketMessageHandler.handleMessage({"type":SocketMessageTypes.CONTROL.name, "message":"updateUIRate", "data":data})
    except NameError:
        pass

# @sio.event
# async def chat_message(sid, data):
#     print("message ", data)
#     await sio.emit('reply', room=sid)


if __name__ == '__main__':
    # web.run_app(app, host="0.0.0.0",port=3000)
    wst = threading.Thread(target=serve_app)
    wst.daemon = True
    wst.start()

    asyncio.get_event_loop().run_until_complete(main())

    # main()
    # asyncio.run(web.run_app(app, host="0.0.0.0",port=3000))
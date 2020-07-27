import Utils.RuntimeHelpers.SettignsManager as settingsManager
from Processes.ProcManager import ProcManager
import Utils.RuntimeHelpers.Stopwatch as stopwatch
import asyncio
from aiohttp import web
import socketio
import threading
import eventlet
from time import sleep
static_files = {
    "/": {'filename': 'index.html', 'content_type': 'text/html'},
}

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

mgr = socketio.AsyncAioPikaManager('amqp://guest:guest@localhost:5672')
sio = socketio.AsyncServer(client_manager=mgr)
app = web.Application()
sio.attach(app)
app.router.add_static('/www', 'www')
app.router.add_get('/', index)
event_loop_a = asyncio.new_event_loop()
ver = 0.1
settings = None

@sio.event
def connect(sid, environ):
    print("connect ", sid)
    # main()

@sio.event
async def chat_message(sid, data):
    print("message ", data)
    await sio.emit('reply', room=sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


def serve_app():
    asyncio.set_event_loop(event_loop_a)
    web.run_app(app,host="0.0.0.0",port=3000)

async def main():
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
    i = 0
    while not procManager.sharedObjectsInstances["keyboard"].getAction() == "Stop":
        stopwatch.start()
        await mgr.emit('state', {"state":procManager.sharedObjectsInstances['state'].getState(),"side":procManager.sharedObjectsInstances['state'].getSide(),"hp":procManager.sharedObjectsInstances['gameState'].getGameStateValue('hp')})
        # sio.emit('side', procManager.sharedObjectsInstances['state'].getSide())
        # sio.emit('gameState', procManager.sharedObjectsInstances['gameState'].getGameStateValue('hp'))
        i = i+1
        # sleep(0.01)
        # log(f"[ Main ] {stopwatch.stop()}\t {procManager.sharedObjectsInstances['state'].getState()}\t{procManager.sharedObjectsInstances['state'].getSide()}\t{procManager.sharedObjectsInstances['gameState'].getGameStateValue('hp')}")
    
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
    # web.run_app(app, host="0.0.0.0",port=3000)
    wst = threading.Thread(target=serve_app)
    wst.daemon = True
    wst.start()

    asyncio.run(main())

    # main()
    # asyncio.run(web.run_app(app, host="0.0.0.0",port=3000))
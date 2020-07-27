import multiprocessing
from pynput import keyboard
import eventlet
import socketio

class SocketServer(multiprocessing.Process):
    sio = socketio.Server()

    @sio.event
    def connect(sid, environ):
        print('connect ', sid)

    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)

    def __init__(self, serverObject, log, **kwargs):
        multiprocessing.Process.__init__(self)
        self.name = "SocketServer"
        self.serverObject = serverObject
        self.exit = multiprocessing.Event()
        self.log = log.log
        # create a Socket.IO server
        self.sio = socketio.Server(async_mode='eventlet')


        self.static_files = {
            '/': {'filename': 'index.html', 'content_type': 'text/html'},
        }
        # wrap with WSGI application
        self.app = socketio.WSGIApp(self.sio, static_files=self.static_files)
        # eventlet.monkey_patch()

        self.log(f"[ {self.name} ] Initialized")

    def run(self):
        self.log(f"[ {self.name} ] Running")
        eventlet.wsgi.server(eventlet.listen(('', 3000)), self.app)
        self.log(f"[ {self.name} ] Shutdown complete")

    def sendMessage(self,messageType, message):
        self.log(f"[ {self.name} ] [sendMessage] sending {messageType} with content: {message}")
        self.sio.emit('state', {'data': 'foobar'})

    async def shutdown(self):
        self.log(f"[ {self.name} ]Shutdown initiated")
        self.exit.set()
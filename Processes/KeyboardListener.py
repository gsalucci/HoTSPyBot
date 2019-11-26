import multiprocessing
from pynput import keyboard
class KeyboardListener(multiprocessing.Process):

    def __init__(self, keyboardObject, log, **kwargs):
        multiprocessing.Process.__init__(self)
        self.name = "KeyboardListener"
        self.keyboardObject = keyboardObject
        self.exit = multiprocessing.Event()
        self.log = log.log
        self.log(f"[ {self.name} ] Initialized")

    def run(self):
        self.log(f"[ {self.name} ] Running")
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        while not self.exit.is_set():
            pass
        self.log(f"[ {self.name} ] Shutdown complete")

    def shutdown(self):
        self.log(f"[ {self.name} ]Shutdown initiated")
        self.exit.set()

    def on_press(self,key):
        try:
            if key==keyboard.Key.f5:
                self.keyboardObject.setAction("Start")
                #self.log(f"{self.name}: {self.keyboardObject.getAction()}")
            if key==keyboard.Key.f6:
                self.keyboardObject.setAction("Stop")
            if key==keyboard.Key.f7:
                self.keyboardObject.setAction("Exit")  
        except AttributeError:
            self.log('key {0} pressed'.format(key))
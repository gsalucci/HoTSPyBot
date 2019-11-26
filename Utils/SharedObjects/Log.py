class Log():
    def __init__(self):
        self.messages = []
    def getMessages(self):
        return self.message
    def setMessages(self,m):
        self.message = m
    def log(self, m):
        if len(self.messages) > 0:
            if m != self.messages[-1]:
                print(f"{m}")
                self.messages.append(m)
        else:
            print(f"{m}")
            self.messages.append(m)            
    
    def lastMessage(self):
        print(f"{self.messages[-1]}")
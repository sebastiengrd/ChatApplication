class SocketClient:
    def __init__(self, websocket):
        self.websocket = websocket
        self.username = None
        self.to = None

from MessageField import MessageField
import json


class Message:
    def __init__(self, messageFields: list[MessageField]):
        self.messageFields = messageFields

    async def send(self, client):
        data = {}
        for field in self.messageFields:
            data[field.name] = field.value
        await client.websocket.send(json.dumps(data))

    def sendToAll(self, clients):
        for cl in clients:
            self.send(cl)

    def parse(self, message):
        data = json.loads(message)
        for field in self.messageFields:
            field.value = data[field.name]

    def getField(self, name):
        for field in self.messageFields:
            if field.name == name:
                return field
        return None
    def addField(self, field):
        self.messageFields.append(field)

    def removeField(self, name):
        for field in self.messageFields:
            if field.name == name:
                self.messageFields.remove(field)


    def executeMessageAction(self):
        pass
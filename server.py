import asyncio
import json
import websockets

class Client:
    def __init__(self, websocket):
        self.websocket = websocket
        self.username = None
        self.to = None


class ClientMessageHandler:
    currentlyConnectedClients = set()

    def __init__(self, websocket):
        self.websocket = websocket
        self.client = Client(websocket)
        ClientMessageHandler.currentlyConnectedClients.add(self.client)

        
    async def listenMessages(self):
        try:
            async for message in self.websocket:
                await self.parseMessage(message)
        finally:
            print(f'{self.client.username} disconnected')
            ClientMessageHandler.currentlyConnectedClients.remove(self.client)

    async def parseMessage(self, message):
        data = json.loads(message)
        print("Received: " + message)
        
        if data.get("username") != None:
            await self.updateUsername(data["username"])
        elif data.get("to") != None:
            self.client.to = data["to"]
            print(f'{self.client.username} is now talking to {data["to"]}')
        elif data.get("message") != None:
            print(f"Received message. Will send message to {self.client.to}" )
            for cl in ClientMessageHandler.currentlyConnectedClients:
                if (cl.username == self.client.to or self.client.to == "all" or self.client.to == "All" or self.client.to == None) and cl.username != self.client.username:
                    if(cl.websocket.open):
                        await cl.websocket.send(json.dumps({"message": data["message"], "from": self.client.username}))
        elif data.get("getUsers") != None:
            await self.sendGetUserReply(self.websocket, self.client)
            # await websocket.send(json.dumps({"users": [cl.username for cl in currentlyConnectedClients if cl.username != None and cl.username != client.username and cl.websocket.open]}))
        else:
            print("Invalid message")

    async def updateUsername(self, username):
        oldUsername = self.client.username 
        self.client.username = username
        print(f'{oldUsername} is now {username}')
        await self.sendUserUpdateToAllClients(self.client)


    async def sendUserUpdateToAllClients(self, client):
        for cl in ClientMessageHandler.currentlyConnectedClients:
            if cl.username != client.username and cl.websocket.open:
                await self.sendGetUserReply(cl.websocket, cl)

    async def sendGetUserReply(self, websocket, currentClient):
        await websocket.send(json.dumps({"users": [cl.username for cl in ClientMessageHandler.currentlyConnectedClients if cl.username != None and cl.username != currentClient.username and cl.websocket.open]}))

    async def getOtherClients(self):
        return [cl for cl in ClientMessageHandler.currentlyConnectedClients if cl.username != self.client.username and cl.websocket.open]

async def chat_server(websocket, path):
    messageHandler = ClientMessageHandler(websocket)
    await messageHandler.listenMessages()



async def main():
    server = await websockets.serve(chat_server, '0.0.0.0', 1234)
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
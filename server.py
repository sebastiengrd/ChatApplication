import asyncio
import json
import websockets

currentlyConnectedClients = set()

async def chat_server(websocket, path):
    currentlyConnectedClients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f'{data["username"]}: {data["message"]}')
            for client in currentlyConnectedClients:
                if client != websocket:
                    await client.send(message)
    finally:
        currentlyConnectedClients.remove(websocket)

async def main():
    server = await websockets.serve(chat_server, '0.0.0.0', 1234)
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
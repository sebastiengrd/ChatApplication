
import json
import asyncio
from websockets import connect

async def read(websocket):
    while True:
        response = await websocket.recv()
        data = json.loads(response)
        print(f'{data["username"]}: {data["message"]}')

async def write(websocket, username):
    while True:
        message = await asyncio.get_event_loop().run_in_executor(None, input, 'Type your message: ')
        await websocket.send(json.dumps({"username": username, "message": message}))

async def client(username):
    async with connect("ws://localhost:1234") as websocket:
        read_task = asyncio.create_task(read(websocket))
        write_task = asyncio.create_task(write(websocket, username))
        await asyncio.gather(read_task, write_task)

def getUsername():
    return input('Enter your username: ')

if __name__ == '__main__':
    username = getUsername()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        asyncio.run(client(username))
    except KeyboardInterrupt:
            loop.close()

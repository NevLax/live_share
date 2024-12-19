import asyncio
from websockets.asyncio.client import connect


async def stream():
    async with connect('ws://localhost:8765') as websocket:
        await websocket.send('stream')
        while True:
            mess = input()
            if mess:
                await websocket.send(mess)
            else:
                return


if __name__ == '__main__':
    asyncio.run(stream())

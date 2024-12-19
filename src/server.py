import asyncio
from websockets.asyncio.server import serve
from websockets.asyncio.server import broadcast

#CONNECTIONS = set()
SUBSCRIBE = {'nlx': set(),}


async def register(websocket):
    print('connect to server')
    message = await websocket.recv()
    if message == 'nlx':
        SUBSCRIBE['nlx'].add(websocket)
        print('connect to stream')
        try:
            await websocket.wait_closed()
        finally:
            print('disconnect stream and server')
            SUBSCRIBE['nlx'].remove(websocket)


async def sending(stream='nlx'):
    message = "print('hello')"
    print('sending stream')
    while True:
        broadcast(SUBSCRIBE[stream], message)
        print('broadcast')
        await asyncio.sleep(2)


async def main():
    async with serve(register, 'localhost', 8765,) as server:
        await sending()


if __name__ == '__main__':
    asyncio.run(main())

import asyncio
from websockets.asyncio.server import serve
from websockets.asyncio.server import broadcast

SUBSCRIBE = {'nlx': set(),}
MESSAGE = {'nlx': 'message'}
LISTEN = {'nlx': set()}

async def register(websocket):
    print('\tconnect to server')
    message = await websocket.recv()
    if message == 'nlx':
        SUBSCRIBE['nlx'].add(websocket)
        print('\tconnect to stream')
        try:
            await websocket.wait_closed()
        finally:
            print('\tdisconnect subscribe')
            SUBSCRIBE['nlx'].remove(websocket)
    if message == 'stream':
        print('\tconnect streamer')
        LISTEN['nlx'].add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            print('\tdisconnect streamer')
            LISTEN['nlx'].remove(websocket)


async def listen():
    print('\t\t\topen listener')
    await asyncio.sleep(1)
    while True:
        print('\t\t\t--listener iteration')
        await asyncio.sleep(1)
        for ws in LISTEN['nlx']:
            mess = await ws.recv()
            print(f'\t\t\t----message: {mess}')
            MESSAGE['nlx'] = mess


async def sending(stream='nlx'):
    print('sending stream')
    while True:
        broadcast(SUBSCRIBE[stream], MESSAGE[stream])
        print('broadcast')
        await asyncio.sleep(2)


async def main():
    async with serve(register, 'localhost', 8765,) as server:
        await asyncio.gather(
            listen(),
            sending(),
        )


if __name__ == '__main__':
    asyncio.run(main())

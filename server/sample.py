import asyncio
import datetime
import random
import websockets


async def time(websocket, path):
    while True:
        name = await websocket.recv()
        name += '!!!!!'
        await websocket.send(name)


start_server = websockets.serve(time, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

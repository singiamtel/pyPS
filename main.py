from websockets import client
from parser import parse, commands, sys
import asyncio
from config import socket_url

current_rooms = []

commands_file = open('commands.txt', 'w+')
async def updater(ws : client.WebSocketClientProtocol):
    while True:
        await asyncio.sleep(5)
        # print socket status
        res = await (await ws.ping())
        # print(f'Ping: {res}')
        # check if there are any commands to send
        for line in commands_file:
            if line.strip() == '':
                continue
            await ws.send('|' + line.strip())
            print(f'Sent {line.strip()}')
        #clear file contents
        commands_file.seek(0)
        commands_file.truncate()

async def ainput(string: str) -> str:
    await asyncio.to_thread(sys.stdout.write, f'{string} ')
    return (await asyncio.to_thread(sys.stdin.readline)).rstrip('\n')

async def process_input(ws):
    while True:
        msg = await ainput('')
        msg = msg.strip()
        await ws.send(msg)

async def process(ws, msg):
        msg = msg.decode('utf-8') if type(msg) == bytes else str(msg)
        roomid, cmd, args = parse(msg)
        print(f'cmd: {cmd}')
        if cmd in commands and commands[cmd].get('process') != None:
            print(f'Processing {cmd}')
            await commands[cmd]['process'](ws, args)
        elif cmd == 'pm':
            print('pm to', args[0], ' from ', args[1], ':', args[2])
        elif cmd == 'queryresponse':
            pass
        elif cmd == 'init':
            my_dict = args[0]
            current_rooms.append(my_dict)
            print(current_rooms[-1]['id'])


async def loop():
    async for ws in client.connect(socket_url):
        print('Trying to connect')
        asyncio.create_task(updater(ws))
        asyncio.create_task(process_input(ws))
        async for msg in ws:
            asyncio.create_task(process(ws, msg))

asyncio.run(loop())

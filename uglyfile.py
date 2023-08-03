# Here I hide the ugly code
# Please don't tell anyone

import json
from sys import stderr
from typing import List
from bs4 import BeautifulSoup
import requests
from bot import Bot, Message
from config import rooms

def removenewline(string):
    try:
        return string.strip()
    except AttributeError:
        print('Error removing newline from string: ' + str(string) + ' ' + str(type(string)), file=stderr)
        return string


def challstr_parser(roomid, cmd, args):
    return (cmd, ['|'.join(args)])

def updateuser_parser(roomid, cmd, args):
    # 'args': [('user', str), ('named', int), ('avatar', str), ('settings', dict)],
    try:
        parsed = json.loads(args[3])
        new_args = [*args[:3], parsed]
        return (cmd, new_args)
    except json.decoder.JSONDecodeError:
        print('Received invalid JSON from server: ' + args[3], file=stderr)
        return (cmd, args)

def init_parser(roomid, cmd, args: List[str]):
    bot = Bot()
    my_dict = {} 
    my_dict['roomtype'] = removenewline(args[0])
    my_dict['title'] = removenewline(args[2])
    my_dict['users'] = removenewline(args[4]).split(',')
    my_dict['id'] = removenewline(args[6])
    # all messages
    my_dict['messages'] = []
    # for i in range(7, len(args), 4):
    bot.add_room(roomid, my_dict['title'])
    i = 7
    while True:
        msg_type = args[i]
        if msg_type == 'raw':
            content = parse_html(args[i+1])
            i += 2
            message = Message(roomid, msg_type, content)
            my_dict['messages'].append(message)
            bot.add_message(roomid, message, event=False)
        elif msg_type == 'c:':
            msg_id = args[i+1]
            user = removenewline(args[i+2])
            content = removenewline(args[i+3])
            message = Message(roomid, msg_type, content, user, msg_id)
            bot.add_message(roomid, message, event=False)
            i += 4
        else:
            print('Unknown message type: ' + msg_type, file=stderr)
            i += 1
        if i >= len(args):
            break
    return (cmd, [my_dict]) # for compatibility with other parsers

def parse_html(html):
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text().strip()


async def login(ws, args):
    bot = Bot()
    username = bot.get_username()
    password = bot.get_password()
    if username == None or password == None:
        raise Exception('Bot credentials not set')
    post_response = requests.post('https://play.pokemonshowdown.com/api/login', params={
        'name': username,
        'pass': password,
        'challstr': args[0]
    }).content
    try:
        res = post_response[1:].decode('utf-8')
        res_json = json.loads(res)
        try:
            await ws.send(f'|/trn {username},0,{res_json["assertion"]}')
        except Exception as e:
            print(e, e.args, file=stderr)
            raise Exception('Bot credentials are incorrect')
        return res_json
    except Exception as e:
        print('Error logging in, weird response from loginserver', file=stderr)
        print(e, e.args, file=stderr)
        return None

async def challstr(ws, args):
    # print('Received challstr, logging in')
    bot = Bot()
    username = bot.get_username()
    res = await login(ws, args)
    if res == None:
        print('Could not log in')
        return None
    print('Logged in')
    for room in rooms:
        await ws.send(f'|/join {room}')
    await ws.send(f'|/avatar supernerd')
    await ws.send(f'|/trn {username}')
    # await ws.send(f'|/query roomlist')

def c_parser(roomid, cmd, args):
    msg_handler = Bot()
    msg_id = args[0]
    msg_user = removenewline(args[1])
    msg_content = removenewline(args[2])
    message = Message(roomid, cmd, msg_content, msg_user, msg_id)
    msg_handler.add_message(roomid,message)
    return (cmd, [message])

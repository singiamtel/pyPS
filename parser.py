import sys
from dataclasses import dataclass
import traceback
from bot import Message
from uglyfile import c_parser, challstr, challstr_parser, init_parser, json, updateuser_parser
from typing import Callable, TypedDict, cast

class Command(TypedDict):
    args: list
    weirdParse: Callable | None
    process: Callable | None

commands: dict[str, Command] = {
        'updateuser': {
            'args': [('user', str), ('named', int), ('avatar', str), ('settings', dict)],
            'weirdParse': updateuser_parser,
            'process': None,
            },
        'challstr': {
            'args': [('challstr', str)],
            'weirdParse': challstr_parser,
            'process': challstr,
            },
        'formats': {
            'args': [('formats', list)], # List implies that there are no more arguments after. Hopefully that's always the case :D
            'weirdParse': None,
            'process': None,
            },
        'updatechallenges': {
            'args': [('challenges', dict)],
            'weirdParse': None,
            'process': None,
            },
        'init': {
            'args': [ ('roomtype', str)],
            'weirdParse': None,
            'process': None,
            },
        'title': {
            'args': [ ('title', str)],
            'weirdParse': None,
            'process': None,
            },
        'users': {
            'args': [ ('users', list)],
            'weirdParse': None,
            'process': None,
            },
        'html': {
            'args': [ ('html', str)],
            'weirdParse': None,
            'process': None,
            },
        'uhtml': {
            'args': [('htmlid', str), ('html', str)],
            'weirdParse': None,
            'process': None,
            },
        'uhtmlchange': {
            'args': [ ('htmlid', str), ('html', str)],
            'weirdParse': None,
            'process': None,
            },
        'join': {
            'args': [ ('user', str)],
            'weirdParse': None,
            'process': None,
            },
        'leave': {
            'args': [ ('user', str)],
            'weirdParse': None,
            'process': None,
            },
        'name': {
            'args': [ ('old', str), ('user', str)],
            'weirdParse': None,
            'process': None,
            },
        'chat': {
            'args': [ ('user', str), ('message', str)],
            'weirdParse': None,
            'process': None,
            },
        'pm': {
            'args': [('sender', str), ('receiver', str) , ('message', list)],
            'weirdParse': None,
            'process': None,
            },
        'c:': {
            'args': [ ('message', Message)],
            'weirdParse': c_parser,
            'process': None,
            },
        'queryresponse': {
            'args': [('querytype', str), ('response', dict)],
            'weirdParse': None,
            'process': None,
            },
        'J': {
            'args': [('user', str)],
            'weirdParse': None,
            'process': None,
        },  
        'L': {
            'args': [('user', str)],
            'weirdParse': None,
            'process': None,
        },
        'init': {
            'args': [('roomtype', dict)],
            'process': None,
            'weirdParse': init_parser,
        },
        'updatesearch': {
            'args': [('search', dict)],
            'weirdParse': None,
            'process': None,
        },
        'deinit': { # I don't know what this is
            'args': [],
            'weirdParse': None,
            'process': None,
        },
        'N': {
            'args': [('newname', str), ('oldname', str)],
            'weirdParse': None,
            'process': None,
        },
}

def parse(data: str):
    arr = data.split('|')
    roomid = arr[0].lstrip('>').strip()
    cmd = arr[1]
    args = arr[2:]
    if cmd not in commands:
        print('---start unknown---')
        print('Warn: Unknown command %s' % cmd)
        print('roomid: %s' % roomid)
        print('args: %s' % str(args))
        print('---end unknown---')
    else:
        if 'weirdParse' in commands[cmd] and commands[cmd]['weirdParse'] is not None:
            # weirdparse is defined for this command, but we need to cast it
            cmd, args = cast(Callable, commands[cmd]['weirdParse'])(roomid, cmd, args)
        # if any argument is a dict, json.loads it
        for i in range(len(commands[cmd]['args'])):
            try:
                if commands[cmd]['args'][i][1] == list:
                    # print(commands[cmd]['args'][i])
                    # join the rest of the args
                    joined = '|'.join(args[i:])
                    args[i] = joined
                    # delete the rest of the args if they exist
                    args = args[:i+1]
                    break
                elif commands[cmd]['args'][i][1] == dict:
                    # join the rest of the args
                    if type(args[i]) == dict:
                        continue
                    joined = '|'.join(args[i:])
                    jsoned = json.loads(joined)
                    # delete the rest of the args if they exist
                    args = args[:i] + [jsoned]
                    break
            except Exception as e:
                print('Error parsing args for command %s' % cmd, file=sys.stderr)
                print(traceback.format_exc())
                print(e, e.args, file=sys.stderr)
        if len(args) != len(commands[cmd]['args']) and commands[cmd]['args'][-1][0] != 'list':
            print(f'Warn: Incorrect number of arguments for command {cmd} ({len(args)} != {len(commands[cmd]["args"])})')
            print('args: %s' % str(args))
    return (roomid, cmd, args)

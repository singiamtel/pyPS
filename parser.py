import sys
import traceback
from uglyfile import challstr, challstr_parser, init_parser, json, updateuser_parser

commands = {
        'updateuser': {
            'args': [('user', str), ('named', int), ('avatar', str), ('settings', dict)],
            'weirdParse': updateuser_parser,
            },
        'challstr': {
            'args': [('challstr', str)],
            'weirdParse': challstr_parser,
            'process': challstr,
            },
        'formats': {
            'args': [('formats', list)], # List implies that there are no more arguments after. Hopefully that's always the case :D
            },
        'updatechallenges': {
            'args': [('challenges', dict)],
            },
        'init': {
            'args': [ ('roomtype', str)],
            },
        'title': {
            'args': [ ('title', str)],
            },
        'users': {
            'args': [ ('users', list)],
            },
        'html': {
            'args': [ ('html', str)],
            },
        'uhtml': {
            'args': [('htmlid', str), ('html', str)],
            },
        'uhtmlchange': {
            'args': [ ('htmlid', str), ('html', str)],
            },
        'join': {
            'args': [ ('user', str)],
            },
        'leave': {
            'args': [ ('user', str)],
            },
        'name': {
            'args': [ ('old', str), ('user', str)],
            },
        'chat': {
            'args': [ ('user', str), ('message', str)],
            },
        'pm': {
            'args': [('sender', str), ('receiver', str) , ('message', list)],
            },
        'c:': {
            'args': [ ('userid', str), ('user', str), ('message', str)],
            },
        'queryresponse': {
            'args': [('querytype', str), ('response', dict)],
            },
        'J': {
            'args': [('user', str)],
        },  
        'L': {
            'args': [('user', str)],
        },
        'init': {
            'args': [('roomtype', dict)],
            'weirdParse': init_parser,
        },
        'updatesearch': {
            'args': [('search', dict)],
        },
        'deinit': { # I don't know what this is
            'args': [],
        },
        'N': {
            'args': [('newname', str), ('oldname', str)],
        },
}

def parse(data: str):
    arr = data.split('|')
    roomid = arr[0]
    cmd = arr[1]
    args = arr[2:]
    if cmd not in commands:
        print('---start unknown---')
        print('Warn: Unknown command %s' % cmd)
        print('roomid: %s' % roomid)
        print('args: %s' % str(args))
        print('---end unknown---')
    else:
        if 'weirdParse' in commands[cmd]:
            cmd, args = commands[cmd]['weirdParse'](cmd, args)
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

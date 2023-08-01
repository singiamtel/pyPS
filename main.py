# Example of how to use the library
import lib
import asyncio

from bot import Bot, Message
from utils import toID

whitelist = ['itszxc']


def handle_message(message: Message):
    print('Received message:', message)

def event_handler(event, *args):
    print('Received event:', event, args)

def eval(message: Message):
    if message.msg_content.startswith('#eval'):
        pass

Bot().event_emitter.on('message', handle_message)
Bot().event_emitter.on('*', event_handler)


asyncio.run(lib.start_bot())

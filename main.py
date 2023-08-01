# Example of how to use the library
import lib
import asyncio

from messages import Message, MessageHandler


def handle_message(message: Message):
    print('Received message:', message.user)

MessageHandler().event_emitter.on('message', handle_message)


asyncio.run(lib.start_bot())

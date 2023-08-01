from dataclasses import dataclass
from typing import TypedDict

from events import EventEmitter

# Singleton class for handling messages
class MessageHandler():
    event_emitter : EventEmitter
    instance = None
    def __init__(self):
        if not MessageHandler.instance:
            MessageHandler.instance = MessageHandler.__MessageHandler()
            MessageHandler.event_emitter = EventEmitter()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __MessageHandler:
        def __init__(self):
            self.messages = []

        def add_message(self, message):
            self.messages.append(message)
            if len(self.messages) > 1000:
                self.messages.pop(0) # oh no
            MessageHandler.event_emitter.emit('message', message)

        def get_messages(self):
            return self.messages

        def get_messages_len(self):
            return len(self.messages)

        def clear_messages(self):
            self.messages = []


@dataclass
class Message():
    msg_content: str
    msg_type: str
    id: str | None # user id
    user: str | None 
    def __init__(self, msg_type, msg_content, user=None, id=None):
        self.msg_type = msg_type
        self.msg_content = msg_content
        self.user = user
        self.id = id


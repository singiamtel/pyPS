from dataclasses import dataclass
from typing import TypedDict

# Singleton class for handling messages
class MessageHandler():
    instance = None
    def __init__(self):
        if not MessageHandler.instance:
            MessageHandler.instance = MessageHandler.__MessageHandler()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __MessageHandler:
        def __init__(self):
            self.messages = []

        def add_message(self, message):
            self.messages.append(message)
            if len(self.messages) > 1000:
                self.messages.pop(0) # oh no

        def get_messages(self):
            return self.messages

        def get_messages_len(self):
            return len(self.messages)

        def clear_messages(self):
            self.messages = []


@dataclass
class Message():
    def __init__(self, msg_type, msg_content):
        self.msg_type: str = msg_type
        self.msg_content: str = msg_content


class ChatMessage(Message):
    id: str # user id
    user: str
    def __init__(self, msg_type, msg_content, user, id):
        super().__init__(msg_type, msg_content)
        self.user = user
        self.id = id


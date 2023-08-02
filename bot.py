from dataclasses import dataclass

from events import EventEmitter

# Singleton class for handling messages
class Bot():
    event_emitter : EventEmitter
    instance = None
    def __init__(self):
        if not Bot.instance:
            Bot.instance = Bot.__Bot()
            Bot.event_emitter = EventEmitter()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Bot:
        def __init__(self):
            self.messages = []
            self.rooms = {}
            self.username = None
            self.password = None

        def add_room(self, roomid, name):
            self.rooms[roomid] = Room(roomid, name)
            Bot.event_emitter.emit('joinroom', (roomid, name))

        def set_credentials(self, username, password):
            self.username = username
            self.password = password

        def get_username(self):
            return self.username

        def get_password(self):
            return self.password

        def remove_room(self, room):
            self.rooms.pop(room)
            Bot.event_emitter.emit('leaveroom', room)

        def add_message(self, roomid, message):
            if roomid not in self.rooms:
                raise Exception(f'Room {roomid} not found')
            self.rooms[roomid].add_message(message)
            Bot.event_emitter.emit('message', message)

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
    msg_id: str | None
    room_id: str | None
    user: str | None 
    def __init__(self, roomid, msg_type, msg_content, user=None, id=None):
        self.msg_type = msg_type
        self.msg_content = msg_content
        self.user = user
        self.msg_id = id
        self.room_id = roomid

@dataclass
class Room():
    id: str
    name: str
    messages: list[Message]
    def __init__(self, roomid, name):
        self.name = name
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > 1000:
            self.messages.pop(0)


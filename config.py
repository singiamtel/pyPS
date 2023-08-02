from dotenv import load_dotenv
from os import getenv
load_dotenv()

URL = 'wss://sim3.psim.us/showdown/websocket'
rooms = ['botdev']#, 'lobby']
# error warning info verbose
socket_url = getenv('socket_url') or 'ws://sim.smogon.com:8000/showdown/websocket'

import socket

BUFFER = 64
PORT = 8000 
HOST = socket.gethostbyname(socket.gethostname()) # IPv4 for local network -> change to public server IP
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT = 'q'


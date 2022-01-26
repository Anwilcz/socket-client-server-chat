import socket
from config import BUFFER, ADDR, FORMAT, DISCONNECT

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(message):
  msg = message.encode(FORMAT)
  msg_len = len(msg)
  msg_len = str(msg_len).encode(FORMAT)
  msg_len += b' ' * (BUFFER - len(msg_len))
  client.send(msg_len)
  client.send(msg)
  response = client.recv(BUFFER).decode(FORMAT)
  print(f'Server response: {response}')


while True:
  msg = input('Enter your message: ')
  send(msg)
  if msg == DISCONNECT:
    break

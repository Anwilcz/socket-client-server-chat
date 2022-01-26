import socket
import threading
from config import BUFFER, PORT, HOST, ADDR, FORMAT, DISCONNECT
from helpers import hide, msg_formatter


# handling individual connection client - server
def client(connection, address):
  print(f'New connection: {hide(address)}')
  while True:
    msg_rec = connection.recv(BUFFER).decode(FORMAT)
    if msg_rec: 
      msg_len = int(msg_rec)
      msg = connection.recv(msg_len).decode(FORMAT)
      if msg == DISCONNECT:
        print(f'[{hide(address)}]: Client has disconnected.')
        connection.send(f'[Server]: Disconnected from the server.'.encode(FORMAT))
        connection.close()
        break
      else:
        print(f'[{hide(address)}]: {msg}')
        # connection.send(bytes('Message received', FORMAT))
        connection.send('[Server]: Message received'.encode(FORMAT))

def start():
  print('Server is starting..')
  print(msg_formatter('Server Info'))
  print('PORT:', PORT)
  print('HOST:', hide(HOST))

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(ADDR)
  server.listen()
  print(f'Server is listening on {hide(HOST)}')
  while True:
    connection, address = server.accept()
    thread = threading.Thread(target=client, args=(connection, address))
    thread.start()
    print(msg_formatter(f'Active connections: {threading.activeCount() - 1}'))


start()
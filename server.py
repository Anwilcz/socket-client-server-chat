import socket
import threading
from config import BUFFER, PORT, HOST, ADDR, FORMAT, DISCONNECT
from helpers import hide, msg_formatter
import re


connections = list()
names = list()

def get_len(message):
  length = len(message)
  length = str(length).encode(FORMAT)
  length += b' ' * (BUFFER - len(length))
  return length



# Broast message to all clients
def broadcast(message, index):
  recipent = re.findall('^\[.+\]:\s@(.+):\s', message)
  if len(recipent):
    recipent = recipent[0]
    sender = re.findall('^\[(.+)\]', message)[0]
    message = re.findall('@.+?:\s(.+)', message)[0]
    msg = f'[From: {sender}]: {message}'
    connections[names.index(recipent)].send(get_len(msg))
    connections[names.index(recipent)].send(msg.encode(FORMAT))
  else:
    msg = message
    length = get_len(msg)
    for connection in connections:
      if connections.index(connection) == index:
        continue 
      connection.send(length)
      connection.send(msg.encode(FORMAT)) 


def client(connection, address):
  # Print new connection estabilished
  print(f'New connection: {hide(address)}')
  set_name(connection)
  if connection in connections:
    while True:
      try:
        msg_len = connection.recv(BUFFER).decode(FORMAT)
        index = connections.index(connection)
        if msg_len:
          msg_len = int(msg_len)
          msg = connection.recv(msg_len).decode(FORMAT)
          name = re.findall('^name: (.+)', msg)
          if msg == DISCONNECT:
            broadcast(f'[Server]: {names[index]} has disconnected.', index)
            connections.pop(index)
            names.pop(index)
            msg = 'disconnected'
            connection.send(get_len(msg))
            connection.send(msg.encode(FORMAT))
            connection.close()
            print(f'Connection with {hide(address)} closed.')
            break    
          elif name:
            name = name[0]
            if name in names or not name:
              msg = '[Server]: Name is invalid or already in use'
              connection.send(get_len(msg))
              connection.send(msg.encode(FORMAT))
            else:
              broadcast(f'[Server]: {names[index]} is now {name}.', index)
              names[index] = name
          else:
            broadcast(f'[{names[index]}]: {msg}', index)

      except:      
        connection.close()
        broadcast(f'[Server]: {names[index]} has disconnected.', index)
        connections.pop(index)  
        names.pop(index)
        print(f'Connection with {hide(address)} lost. Error has occured')
        break

  else:
    print(f'Connection with {hide(address)} lost. Invalid name')
    return
  


 


# Ask new client to set client name and adding new client to the list
def set_name(connection):
  try:
    msg = f'''
{msg_formatter('Welcome to the chatroom')}
->  Choose your name.
->  Enter 'name: selected_name' to change your name.
->  Enter '@recipent_name: message' to send a private message.
->  Enter 'q' to disconnect.
    '''
    connection.send(get_len(msg))
    connection.send(msg.encode(FORMAT))
    while True:
      msg = 'name'
      connection.send(get_len(msg))
      connection.send(msg.encode(FORMAT))
      name_len = connection.recv(BUFFER).decode(FORMAT)
      name_len = int(name_len)
      name = connection.recv(name_len).decode(FORMAT)
      if name in names or not name:
        msg = 'name_error'
        connection.send(get_len(msg))
        connection.send(msg.encode(FORMAT))
      else:
        break
    msg = 'name_validated'
    connection.send(get_len(msg))
    connection.send(msg.encode(FORMAT))
    # Append new connection to the register
    connections.append(connection)
    names.append(name)
    index = -1
    # Inform active connections that new a client has joined 
    msg = f'[Server]: {name} has joined.'
    broadcast(msg, index)
    # Welcome new client
    msg = f'[Server]: Welcome {name}!'
    connection.send(get_len(msg))
    connection.send(msg.encode(FORMAT))
  except: 
    connection.close()

# Print the number of active connections
def active_conn():
  print(msg_formatter(f'Active connections: {threading.activeCount() - 1}'))



def start():
  print('Server is starting..')
  try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(msg_formatter('Server Info'))
    print('PORT:', PORT)
    print('HOST:', hide(HOST))
    print(f'Server is listening on {hide(HOST)}')
    active_conn()
  except: 
    print('Server start failed!')
    
  while True:
    # Start a new client thread
    connection, address = server.accept() 
    # Estabilish connection with the client
    thread = threading.Thread(target=client, args=(connection, address))
    thread.start()
    active_conn()


start()
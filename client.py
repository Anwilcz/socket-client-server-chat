
from os import abort
import socket
from config import BUFFER, ADDR, FORMAT, DISCONNECT
import threading


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
invalid_name = False


def get_len(message):
  length = len(message)
  length = str(length).encode(FORMAT)
  length += b' ' * (BUFFER - len(length))
  return length

def get_msg():
  response = client.recv(BUFFER).decode(FORMAT)
  if response:
    length = int(response)
    msg = client.recv(length).decode(FORMAT)
    if msg == 'disconnected':
      print('Disconnected from the server.')
      client.close()    
    else:
      print(msg)
  
def set_name():
  get_msg()
  while True:
    response = client.recv(BUFFER).decode(FORMAT)
    if response:
      length = int(response)
      msg = client.recv(length).decode(FORMAT)
      if msg == 'name':
        name = input('[Client]: Please enter your name: ')
        client.send(get_len(name))
        client.send(name.encode(FORMAT))
      elif msg =='name_error':
        global invalid_name
        invalid_name = True
        print('[Client]: Name is invalid or already in use.')
      elif msg =='name_validated':
        print('[Client]: Connection estabilished successfully')
        send_th = threading.Thread(target=write)
        receive_th = threading.Thread(target=receive)
        receive_th.start()
        send_th.start()
        break       
      else:
        print(msg)

def write():
  while True:
    try: 
      msg = input()
      client.send(get_len(msg))
      client.send(msg.encode(FORMAT))
      if msg == DISCONNECT:
        break
    except:
      if invalid_name:
        print('Disconnected from the server.')
      else:
        print('Server does not respond..')
      client.close() 
      break
      
def receive():
  while True:
    try:
      get_msg()
    except:
      client.close()
      break

def start():
  try:
    client.connect(ADDR)
    set_name()
  except:
    print('Connection cannot be estabilished.')

    
start()
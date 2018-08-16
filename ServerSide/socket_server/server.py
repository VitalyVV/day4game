from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import thread
import time
import datetime
import json

host = '0.0.0.0'
port = 8080
size = 4096 * 4

addr = (host, port)

serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serversocket.bind(addr)
serversocket.listen(150)

clients = [serversocket]
players = set()
multiplayers = set()


class User:
  def __init__(self, socket):
    self.socket = socket
    self.registered = False

def handler(clientsocket, clientaddr):
  print("Accepted connection from: {}".format(clientaddr))
  data = clientsocket.recv(1024)
  data = json.loads(data)

  print(type(data))
  print(data)
  if data['type'] == 'solo':
    # clientsocket.send("You requested solo game, user={}".format(clientaddr))
    thread.start_new_thread(solo_player, (clientsocket, ))
  elif data['type'] == 'multiplayer':
    # clientsocket.send("You requested multiplayer game, wait some time for another user")
    multiplayers.add(clientsocket)

def start_game(user1, user2):
  s1 = user1.socket
  s2 = user2.socket
  registration = "Player {} connected with player {}".format(s1, s2)
  response = 'Make action'

  while True:
    if (not user1.registered):
      response += registration
      user1.registered = True
    s1.send(response)
    response = s1.recv(size)

    if (not user2.registered):
      response = registration + '\n###\n' + response
      user2.registered = True
    s2.send(response)
    response = s2.recv(size)

def multiple_players():
  while True:
    if len(multiplayers) >= 2:
      player1 = multiplayers.pop()
      player2 = multiplayers.pop()
      thread.start_new_thread(start_game, (User(player1), User(player2)))
    time.sleep(3)

def solo_player(socket):
  user = User(socket)
  # monster = Monster()
  registration = "You will be playing against AI monster.\nMake your action"
  response = ''

  while True:
    if not user.registered:
      response += registration
      user.registered = True
    socket.send(response)
    response = socket.recv(size)
    # response = monster.act(response) # todo: me
    response = "I obey you"
    time.sleep(1)

thread.start_new_thread(multiple_players, ())


while True:
  try:
    print("Server is listening for connections\n")
    clientsocket, clientaddr = serversocket.accept()
    clients.append(clientsocket)
    thread.start_new_thread(handler, (clientsocket, clientaddr))
  except KeyboardInterrupt: # Ctrl+C # FIXME: vraci "raise error(EBADF, 'Bad file descriptor')"
    print "Closing server socket..."
    serversocket.close()
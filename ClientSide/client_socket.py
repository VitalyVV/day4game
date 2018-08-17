from socket import socket, AF_INET, SOCK_STREAM, error
import json
import time

host = "10.90.131.245"
port = 8080
size = 4096 * 4

class Connection:
	def create_connection(self):
		s = socket(AF_INET, SOCK_STREAM)
		s.connect((host, port))
		return s

	def send_message(self, content):
		buf = json.dumps(content)
		self.socket.send(buf.encode('utf-8'))

	def register(self):
		self.send_message({'type': self.game_type})

	def close(self):
		self.socket.close()

	def receive_message(self):
		try: 
			return json.loads(self.socket.recv(size))
		except ConnectionAbortedError:
			self.recursion_deep +=1
			if (self.recursion_deep > 120):
				print("You waited for too long, try once again")
				return
			time.sleep(1)
			return self.receive_message()


	def __init__(self, game_type='solo'):
		self.recursion_deep = 0
		self.socket = self.create_connection()
		self.game_type = game_type
		self.register()

if __name__ == '__main__':
	connection = Connection('solo')
	while True:
		msg = connection.send_message({'msg': 'hello bob', 'socket': connection.socket.getsockname()[1]})
		time.sleep(1)
		# print(msg.decode('utf-8'))
		print(msg)
	connection.close()
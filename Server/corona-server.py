#!/usr/bin/python3

import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 1234
serverSocket.bind((host, port))

serverSocket.listen(5)
while True:
  client, addr = serverSocket.accept()
  print('Connection from %s' % str(addr))
  msg='Thanks for connection' + "\r\n"
  client.send(msg.encode('ascii'))
  client.close()

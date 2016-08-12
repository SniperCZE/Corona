#!/usr/bin/python3

import configparser
import socket

config = configparser.ConfigParser()
config.read('corona-server.conf')

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = config['Corona']['ListenAddress']
port = config['Corona']['ListenPort']
serverSocket.bind((host, int(port)))

serverSocket.listen(5)
while True:
  client, addr = serverSocket.accept()
  print('Connection from %s' % str(addr))
  msg='Thanks for connection' + "\r\n"
  client.send(msg.encode('ascii'))
  client.close()

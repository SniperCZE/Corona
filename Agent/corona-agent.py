#!/usr/bin/python3

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 1234

clientSocket.connect((host, port))
msg=clientSocket.recv(1024)
clientSocket.close()

print (msg.decode('ascii'))
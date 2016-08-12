#!/usr/bin/python3

import configparser
import socket

config = configparser.ConfigParser()
config.read('corona-agent.conf')

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = config['Corona']['CoronaServer']
port = config['Corona']['CoronaServerPort']

clientSocket.connect((host, int(port)))
msg=clientSocket.recv(1024)
clientSocket.close()

print (msg.decode('ascii'))
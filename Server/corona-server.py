#!/usr/bin/python3
import os
import sys
sys.path.append('../libs')

import configparser
import socket
import coronaprotocol

config = configparser.ConfigParser()
config.read('corona-server.conf')

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = config['Corona']['ListenAddress']
port = config['Corona']['ListenPort']
serverSocket.bind((host, int(port)))

serverSocket.listen(5)

cp = coronaprotocol.CoronaProtocol()

while True:
    client, addr = serverSocket.accept()
    
    msg = client.recv(4096)
    msgDecoded = cp.decodeMessage(msg.decode('ascii'))
    
    print(msgDecoded)
    if msgDecoded['message'] == 'AGENT_ONLINE':
        msgReply = cp.agentRegistered(msgDecoded['parameters']['ip'], True)
        client.send(msgReply.encode('ascii'))
    else:
        print('Invalid message')
    
    client.close()

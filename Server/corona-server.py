#!/usr/bin/python3
import os
import sys
sys.path.append('../libs')

import configparser
import socket
import coronaprotocol
import coronalogger

config = configparser.ConfigParser()
config.read('corona-server.conf')

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = config['Corona']['ListenAddress']
port = config['Corona']['ListenPort']
serverSocket.bind((host, int(port)))

serverSocket.listen(5)

cp = coronaprotocol.CoronaProtocol()
log = coronalogger.CoronaLogger()
log.setLogTarget('stdout')

while True:
    client, addr = serverSocket.accept()
    
    msg = client.recv(4096)
    msgDecoded = cp.decodeMessage(msg.decode('ascii'))
    
    log.messageLog(msgDecoded)
    if msgDecoded['message'] == 'AGENT_ONLINE':
        msgReply = cp.agentRegistered(msgDecoded['parameters']['ip'], True)
        client.send(msgReply.encode('ascii'))
    else:
        print('Invalid message')
    
    client.close()

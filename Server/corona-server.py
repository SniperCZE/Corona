#!/usr/bin/python3
import os
import sys
sys.path.append('../libs')

import configparser
import socket
import coronaprotocol
import coronalogger
import threading
import time

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

connectedAgents = {}

class agentPingThread (threading.Thread):
    """Thread for pinging all registered agents. If not responding, deregister that agent from agent pool"""

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        self.pingAllAgents();
        
    def pingAgent(self, agentIp):
        log.messageLog('Agent %s pinged' % agentIp)
        
    def pingAllAgents(self):
        while True:
            log.messageLog('Pinging all registered agents')
            for agentIp, agentDetails in connectedAgents.items():
                self.pingAgent(agentIp)
            time.sleep(5)

pingThread = agentPingThread()
pingThread.daemon = True
pingThread.start()

while True:
    client, addr = serverSocket.accept()
    
    msg = client.recv(4096)
    msgDecoded = cp.decodeMessage(msg.decode('ascii'))
    
    log.messageLog(msgDecoded)
    if msgDecoded['message'] == 'AGENT_ONLINE':
        connectedAgents[msgDecoded['parameters']['ip']] = msgDecoded['parameters']
        msgReply = cp.agentRegistered(msgDecoded['parameters']['ip'], True)
        client.send(msgReply.encode('ascii'))
    else:
        print('Invalid message')
    
    client.close()

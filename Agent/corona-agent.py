#!/usr/bin/python3
import os
import sys
sys.path.append('../libs')

import configparser
import socket
import coronaprotocol
import coronalogger

version = '0.1'
cp = coronaprotocol.CoronaProtocol()
log = coronalogger.CoronaLogger()
log.setLogTarget('stdout')

agentClientSocket = None

class agentServer ():
    """Accepting messages from server. It's used for healthchecks, server status messages and commands"""

    host = None
    port = None

    def setAgentServerDetails(self, host, port):
        self.host = host
        self.port = int(port)

    def startAgentServer(self):
        agentServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        agentServerSocket.bind((self.host, self.port))
        agentServerSocket.listen(5)
        while True:
            remoteServer, addr = agentServerSocket.accept()
            msg=remoteServer.recv(4096)
            msgDecoded = msg.decode('ascii')
            print('Received message from remote server: %s' % msgDecoded)
            msgJson = cp.decodeMessage(msgDecoded);
            # find out my reaction is needed
            if msgJson['message'] == 'HEALTHCHECK_PING':
                replyMes = cp.agentPong(self.host, msgJson['parameters']['hcid'])
                remoteServer.send(replyMes.encode('ascii'))
            else:
                pass


class agentClient ():
    """Sending messages initialized by agent"""

    serverHost = ''
    serverPort = 0
    serverSocket = None

    def setServerDetails(self, host, port):
        """Settings of server details - hostname and port to connect"""
        self.serverHost = host
        self.serverPort = int(port)

    def connectToServer(self):
        """Makes connection to corona server"""
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.connect((self.serverHost, self.serverPort))

    def disconnectFromServer(self):
        """Disconnect agent from server. Agent should be connected only when needed"""
        self.serverSocket.close()

    def sendMessage(self, message, waitForReply=True):
        """Sends message generated by coronaprotocol to server and waits for response"""
        response = ''
        try:
            self.connectToServer()
            self.serverSocket.send(message.encode('ascii'))
            if waitForReply:
                res = self.serverSocket.recv(4096)
                response = res.decode('ascii')
            self.disconnectFromServer()
            return response
        except ConnectionRefusedError:
            """There is problem with connection to Corona server"""
            log.messageLog("Cannot connect to Corona server on {}:{}. Exiting.".format(self.serverHost, self.serverPort))
            sys.exit()




config = configparser.ConfigParser()
config.read('corona-agent.conf')

agentIp = config['Corona']['ListenAddress']
agentPort = config['Corona']['ListenPort']
serverHost = config['Corona']['CoronaServer']
serverPort = config['Corona']['CoronaServerPort']

agentServer = agentServer()
agentServer.setAgentServerDetails(agentIp, agentPort)

# thread user for sending messages into server
agentClientSocket = agentClient()
# @type agentClientSocket agentClient
agentClientSocket.setServerDetails(serverHost, serverPort)

msg=agentClientSocket.sendMessage(cp.agentIsOnline(agentIp, agentPort, version))

print (msg)

agentServer.startAgentServer()

#!/usr/bin/python3
import os
import sys
sys.path.append('../libs')

import configparser
import socket
import coronaprotocol
import coronalogger
import coronautils
import threading
import time
import signal
import agents
import mysql.connector as mariadb
import uuid

config = configparser.ConfigParser()
config.read('corona-server.conf')

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = config['Corona']['ListenAddress']
port = config['Corona']['ListenPort']
serverSocket.bind((host, int(port)))

serverSocket.listen(5)

cp = coronaprotocol.CoronaProtocol()
log = coronalogger.CoronaLogger()
log.setLogTarget('stdout')

try:
    mysqlConnData = mariadb.connect(user=config['MySQL']['User'], password=config['MySQL']['Passwd'], database=config['MySQL']['DbName'])
except mariadb.Error as me:
    log.messageLog("MySQL Error: {}".format(me))
    sys.exit()

connectedAgents = agents.CoronaAgents(log, mysqlConnData)

class agentPingThread (threading.Thread):
    """Thread for pinging all registered agents. If not responding, deregister that agent from agent pool"""

    def __init__(self):
        threading.Thread.__init__(self, name = 'Pinger')
        
    def run(self):
        connectedAgents.populateListFromMysql()
        self.pingAllAgents()
        
    def pingAgent(self, agentIp, agentPort):
        pingerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pingerSocket.settimeout(float(config['Corona']['PingTimeout']))
        log.messageLog('Agent %s pinged' % agentIp)
        try:
            pingerSocket.connect((agentIp, int(agentPort)))
            sourceHcid = coronautils.CoronaUtils().randomStringGenerator(24)
            message = cp.agentPing(agentIp, sourceHcid)
            log.messageLog(message)
            pingerSocket.send(message.encode('ascii'))
            response = pingerSocket.recv(4096)
            responseDecoded = cp.decodeMessage(response.decode('ascii'))
            log.messageLog('DEBUG: Response from agent: %s hcid: %s' % (responseDecoded['message'], responseDecoded['parameters']['hcid']))
            pingerSocket.close()
            if sourceHcid != responseDecoded['parameters']['hcid']:
                log.messageLog('Agent %s HCID check failed' % agentIp)
                connectedAgents.removeAgent(agentIp)
        except socket.timeout:
            log.messageLog('Socket timeout from agent %s' % agentIp)
            connectedAgents.removeAgent(agentIp)
        except socket.error as e:
            log.messageLog('Socket error %s from agent %s' % (e.strerror, agentIp))
            connectedAgents.removeAgent(agentIp)
        finally:
            pingerSocket.close()
        
    def pingAllAgents(self):
        while True:
            log.messageLog('Pinging all registered agents')
            for agentIp, agentDetails in connectedAgents.getAll().copy().items():
                self.pingAgent(agentIp, agentDetails['port'])
            time.sleep(5)

def signalHandler(signal, frame):
    log.messageLog('Signal %s received' % signal)
    serverSocket.shutdown(socket.SHUT_RDWR)
    serverSocket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signalHandler)

pingThread = agentPingThread()
pingThread.daemon = True
pingThread.start()

while True:
    client, addr = serverSocket.accept()
    
    try:
        msg = client.recv(4096)
        msgDecoded = cp.decodeMessage(msg.decode('ascii'))
    
        log.messageLog(msgDecoded)
        if msgDecoded['message'] == 'AGENT_ONLINE':
            agentRegInfo = connectedAgents.addAgent(msgDecoded['parameters']['ip'], msgDecoded['parameters'])
            if agentRegInfo['known']:
                msgReply = cp.agentMarkedAsOnline(msgDecoded['parameters']['ip'], agentRegInfo['uuid'])
            else:
                msgReply = cp.agentRegistered(msgDecoded['parameters']['ip'], agentRegInfo['uuid'])
            client.send(msgReply.encode('ascii'))
        else:
            log.messageLog('Invalid message %s' % msgDecoded['message'])
    except ConnectionResetError:
        log.messageLog("Connection reset")

    client.close()

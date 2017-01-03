# definition of Corona protocol messages
import json

class CoronaProtocol:
    def generateMessageObject(self, messageType, parameters):
        return {'message' : messageType, 'parameters' : parameters}

    def agentIsOnline(self, ip, port, version):
        msg = self.generateMessageObject('AGENT_ONLINE', { 'ip' : ip, 'port' : port, 'version' : version })
        return json.dumps(msg)

    def agentRegistered(self, ip, known):
        msg = self.generateMessageObject('AGENT_REGISTERED', { 'ip' : ip, 'known' : known })
        return json.dumps(msg)

    def decodeMessage(self, message):
        return json.loads(message)
    
    def agentPing(self, ip, hcid):
        msg = self.generateMessageObject('HEALTHCHECK_PING', { 'ip' : ip, 'hcid' : hcid })
        return json.dumps(msg)
    
    def agentPong(self, ip, hcid):
        msg = self.generateMessageObject('HEALTHCHECK_PONG', { 'ip' : ip, 'hcid' : hcid })
        return json.dumps(msg)
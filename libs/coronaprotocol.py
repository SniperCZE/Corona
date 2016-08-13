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
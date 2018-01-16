# definition of Corona protocol messages
import json

class CoronaProtocol:
    def generateMessageObject(self, messageType, parameters):
        """Generation of data object from message data"""
        return {'message' : messageType, 'parameters' : parameters}

    def agentIsOnline(self, ip, port, version):
        """Agent is reporting it's state as online"""
        msg = self.generateMessageObject('AGENT_ONLINE', { 'ip' : ip, 'port' : port, 'version' : version })
        return json.dumps(msg)

    def agentRegistered(self, ip, known, agentuuid):
        """Server sees this agent for the first time, so register it and generate UUID"""
        msg = self.generateMessageObject('AGENT_REGISTERED', { 'ip' : ip, 'known' : known, 'agentuuid' : str(agentuuid) })
        return json.dumps(msg)

    def agentMarkedAsOnline(self, ip, know):
        """Server already knows this agent, only marked as online"""
        msg = self.generateMessageObject('AGENT_MARKED_ONLINE', { 'ip' : ip, 'known' : known })
        return json.dumps(msg)

    def decodeMessage(self, message):
        return json.loads(message)
    
    def agentPing(self, ip, hcid):
        msg = self.generateMessageObject('HEALTHCHECK_PING', { 'ip' : ip, 'hcid' : hcid })
        return json.dumps(msg)
    
    def agentPong(self, ip, hcid):
        msg = self.generateMessageObject('HEALTHCHECK_PONG', { 'ip' : ip, 'hcid' : hcid })
        return json.dumps(msg)
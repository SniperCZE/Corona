# List of connected agents

class CoronaAgents:
    
    log = None
    connectedAgents = {}
    
    def __init__(self, logger):
        self.log = logger
    
    def addAgent(self, agentIp, params):
        self.log.messageLog('Agent %s added to list' % agentIp)
        self.connectedAgents[agentIp] = params
        
    def removeAgent(self, agentIp):
        self.log.messageLog('Agent %s removed from list' % agentIp)
        r = self.connectedAgents
        del r[agentIp]
        self.connectedAgents = r
        
    def getAll(self):
        return self.connectedAgents

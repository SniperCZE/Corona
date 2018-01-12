# List of connected agents

class CoronaAgents:
    
    log = None
    connectedAgents = {}
    mysqlConnection = None
    
    def __init__(self, logger, mysqlConn):
        self.log = logger
        self.mysqlConnection = mysqlConn
    
    def addAgent(self, agentIp, params):
        self.log.messageLog('Agent %s added to list' % agentIp)
        self.connectedAgents[agentIp] = params
        cursor = self.mysqlConnection.cursor()
        try:
            cursor.execute("INSERT INTO agents(agent_ip, agent_port, agent_version, is_online) values(INET_ATON('{}'), {}, {}, 1);".format(params['ip'], params['port'], params['version']))
            self.mysqlConnection.commit()
        except mariadb.Error as me:
            self.log.messageLog("MySQL Error: {}".format(me))
        
    def removeAgent(self, agentIp):
        self.log.messageLog('Agent %s removed from list' % agentIp)
        cursor = self.mysqlConnection.cursor()
        try:
            cursor.execute("DELETE from agents where agent_ip=INET_ATON('{}') and agent_port={} limit 1;".format(self.connectedAgents[agentIp]['ip'], self.connectedAgents[agentIp]['port']))
            self.mysqlConnection.commit()
        except mariadb.Error as me:
            self.log.messageLog("MySQL Error: {}".format(me))
        r = self.connectedAgents
        del r[agentIp]
        self.connectedAgents = r
        
    def getAll(self):
        return self.connectedAgents

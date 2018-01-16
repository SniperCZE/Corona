# List of connected agents
import uuid
import mysql.connector as mariadb

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
        retVal = { 'known' : False, 'uuid' : None }
        try:
            if params['uuid'] == 'None':
                agentuuid = uuid.uuid4()
                data = (params['ip'], params['port'], params['version'], agentuuid.bytes)
                cursor.execute("INSERT INTO agents(agent_ip, agent_port, agent_version, is_online, agent_uuid) values(INET_ATON(%s), %s, %s, 1, %s);", data)
                retVal['uuid'] = agentuuid
            else:
                data = (params['ip'], params['port'], uuid.UUID(params['uuid']).bytes)
                cursor.execute("UPDATE agents set is_online=1 where agent_ip=INET_ATON(%s) and agent_port=%s and agent_uuid=%s", data)
                retVal['known'] = True
                retVal['uuid'] = uuid.UUID(params['uuid'])
            self.mysqlConnection.commit()
        except mariadb.Error as me:
            self.log.messageLog("MySQL Error: {}".format(me))

        return retVal
        
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

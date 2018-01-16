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
            params['uuid'] = retVal['uuid']
            self.connectedAgents[agentIp] = params
        except mariadb.Error as me:
            self.log.messageLog("MySQL Error: {}".format(me))

        return retVal
        
    def removeAgent(self, agentIp):
        self.log.messageLog('Agent %s removed from list' % agentIp)
        cursor = self.mysqlConnection.cursor()
        try:
            data = (self.connectedAgents[agentIp]['ip'], self.connectedAgents[agentIp]['port'], self.connectedAgents[agentIp]['uuid'].bytes)
            cursor.execute("UPDATE agents set is_online=0 where agent_ip=INET_ATON(%s) and agent_port=%s and agent_uuid=%s limit 1;", data)
            self.mysqlConnection.commit()
        except mariadb.Error as me:
            self.log.messageLog("MySQL Error: {}".format(me))
        r = self.connectedAgents
        del r[agentIp]
        self.connectedAgents = r
        
    def getAll(self):
        return self.connectedAgents

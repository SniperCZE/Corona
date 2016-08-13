# logger module for Corona

class CoronaLogger:
    
    # logtarget:
    # logfile - all messages to logfile
    # stdout - all messages to stdout
    logtarget = 'stdout'
    logfile = ''
    
    def setLogTarget(self, logtarget):
        self.logtarget = logtarget
        
    def getLogTarget(self):
        return self.logtarget
    
    def messageLog(self, message):
        if self.logtarget=='logfile':
            print('Not implemented yet')
        elif self.logtarget=='stdout':
            print(message)
        else:
            print('Invalid log target %s' % str(self.logtarget));
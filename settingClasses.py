
import socket
#UserSettings
class UserSettings(object):
    def __init__(self,user):
        self.nick = user.nick
        self.ident = user.ident
        self.realname = user.realname

#ServerSettings
class ServerSettings(object):
    def __init__(self, predefinedServer):
        self.port = predefinedServer.port
        self.host = predefinedServer.host
        self.channels = []
        for channel in predefinedServer.channels:
            self.channels.append(channel.upper())
        self.s = None
        self.serverNumber = 0

    def getIrcSocket(self):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        errorMsg = None
        serverTries = 0
        while errorMsg != 0:
            errorMsg = self.s.connect_ex((self.host[serverTries], self.port))
            print errorMsg
            serverTries+=1
        self.serverNumber = serverTries-1
        return self.s
    def getNumber(self):
        return self.serverNumber
    def getId(self):
        return self.host[self.serverNumber]


class Settings(object):
    def __init__(self, serverSettings, userSettings):
        self.serverSettings = serverSettings
        self.channels = serverSettings.channels
        self.userSettings = userSettings

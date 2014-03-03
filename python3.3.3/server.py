from data import DataInterpreter
from utilities import *
import socket
import string

class IrcLoop(object):
    def __init__(self,servers, labelServer):
        self.servers = servers
        self.serverInputIndex=0
        self.changeTargetServerLabel(labelServer)
    def init(self):
        for server in self.servers:
            server.init()
    def getChannels(self):
        return
    def mainLoop(self):
        for server in self.servers:
            server.update()
    def getServers(self):
        return self.servers
    def key(self,event, lineEdit):
        self.servers[self.serverInputIndex].key(event, lineEdit)
    def changeInputTargetServer(self, up, labelServer):
        if up and self.serverInputIndex < len(self.servers)-1:
            self.serverInputIndex+=1
        elif not up and self.serverInputIndex > 0:
            self.serverInputIndex-=1
        self.changeTargetServerLabel(labelServer)
    def changeTargetServerLabel(self, labelServer):
        labelServer.setText("["+str(self.serverInputIndex)+"]--"+self.servers[self.serverInputIndex].getId()+"--")

class ActiveServer(object):
    def __init__(self, settings, window):
        self.settings = settings
        self.dataInterpreter = DataInterpreter(window, self.settings.channels, self.settings.userSettings.nick)
        self.s = None
        self.motdEnd = False
        self.window = window

    def getId(self):
        return self.settings.serverSettings.getId()


    def init(self):
        self.motdEnd = False
        self.connect()
        self.register()

    def connect(self):
        self.s = self.settings.serverSettings.getIrcSocket()
        self.s.setblocking(0)

    def register(self):
        self.sendSilent("NICK %s\r\n" % self.settings.userSettings.nick)
        self.sendSilent("USER %s %s bla :%s\r\n" % (self.settings.userSettings.ident, self.settings.serverSettings.host[self.settings.serverSettings.getNumber()]
            , self.settings.userSettings.realname))

    def joinChannels(self):
        for channel in self.settings.channels:
            self.sendSilent("JOIN "+channel+"\r\n")

    def getSettings(self):
        return self.settings

    def sendSilent(self, message):
        sendData(self.s, message, self.window)

    def parseMOTD(self,organizedData):
        replies = self.dataInterpreter.interpretData(organizedData)
        for reply in replies:
            self.sendSilent(reply.getMessage())
        if organizedData['command'] == "376":
            self.motdEnd = True;
            self.window.appendText("\nSERVER -==."+self.getId()+".fully.linked.==-\nSERVER --== y.0.|_|..7.|-|.3..|-|.4.x.0.r:1337 ==--\n")
            self.joinChannels()

    def updateNormal(self, organizedData):
        replies = self.dataInterpreter.interpretData(organizedData)
        for reply in replies:
            self.sendSilent(reply.getMessage())
    def update(self):
        try:
            readbuffer=self.s.recv(4096).decode()
        except socket.error as msg:
            return
        temp = readbuffer.split("\n")
        organizedData = []
        for line in temp:
            line = line.rstrip()
            if line:
                organizedLine = organizeData(line)
                if organizedLine:
                    organizedData.append(organizedLine)
        for line in organizedData:
            if not self.motdEnd:
                self.parseMOTD(line)
            else:
                self.updateNormal(line)

    def key(self, event, lineEdit):
        reply = self.dataInterpreter.key(event,lineEdit)
        if reply:
            self.sendSilent(reply.getMessage())


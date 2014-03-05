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
        labelServer.setText("["+str(self.serverInputIndex)+"]::["+self.servers[self.serverInputIndex].getId()+"]")


class ActiveServer(object):
    def __init__(self, settings, window):
        self.settings = settings
        self.window = window
        self.dataInterpreter = DataInterpreter(self.window, self.settings)
        self.s = None

    def getId(self):
        return self.settings.serverSettings.getId()

    def init(self):
        self.s = self.settings.serverSettings.getIrcSocket()
        if self.s == None:
            window.appendText("ERRORS could not connect to: "+self.getId())
            return
        replies = self.dataInterpreter.register()
        self._sendReplies(replies)

    def getSettings(self):
        return self.settings

    def update(self):
        messages = self._getMessages()
        if messages:
            for message in messages:
                if message:
                    self.handleMessage(message)

    def handleMessage(self, message):
        replies = self.dataInterpreter.interpretData(message)
        self._sendReplies(replies)

    def key(self, event, lineEdit):
        reply = self.dataInterpreter.key(event,lineEdit)
        self._sendReply(reply)

    def _getMessages(self):
        try:
            readbuffer=self.s.recv(4096)
        except socket.error as msg:
            return None
        return self._parseData(readbuffer)

    def _parseData(self, data):
        dataLines = data.split("\n")
        parsedData = []
        for line in dataLines:
            if line:
                line = string.rstrip(line)
                line = parseLine(line)
                parsedData.append(line)
        return parsedData

    def _sendReply(self, reply):
        if reply:
            self._sendSilent(reply.getMessage())

    def _sendReplies(self, replies):
        for reply in replies:
            self._sendSilent(reply.getMessage())

    def _sendSilent(self, message):
        sendData(self.s, message, self.window)


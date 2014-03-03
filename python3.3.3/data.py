from ChannelActionHandler import ChannelActionHandler
from utilities import *
import PyQt5.QtWidgets

def is_string(s):
  return isinstance(s, basestring)

class DataInterpreter(object):
    def __init__(self, window, channels, userName):
        self.channels = {}
        self.channelNames = channels
        self.window = window
        self.userName = userName
        for channel in self.channelNames:
            self.channels[channel] = ChannelActionHandler(channel, self.window, self.userName)
        self.inputChannelIndex = 0

        self.replies = []

    def interpretData(self, data):
        self.replies = []
        self.handleCommand(data)
        return self.replies

    def handleCommand(self,data):
        if data['command'] == "PRIVMSG":
            self.handlePrivMsg(data['prefix'],data['args'])
            return
        elif data['command'] == "PING":
            self.StackMessage('PONG '+data['args'][-1])

        elif data['command'] == "353":
            chanName = data['args'][-2].upper()
            self.makeSureExists(chanName)
            self.channels[chanName].appendUsers(data['args'][-1])
        elif data['command'] == "JOIN":
            chanName = data['args'][0].upper()
            self.makeSureExists(chanName)
            self.channels[chanName].appendUser(data['prefix'])
        elif data['command'] == "PART":
            chanName = data['args'][0].upper()
            self.makeSureExists(chanName)
            self.channels[chanName].removeUser(data['prefix'])
        self.window.appendText("\nSERVER |prfx| %s |cmd| %s |args| %s" % ( data['prefix'], data['command'], data['args'] ) )
    def makeSureExists(self, channel):
        if not channel in self.channels:
            self.channels[channel] = ChannelActionHandler(channel, self.window, self.userName)
            self.channelNames.append(channel)
    def handlePrivMsg(self, user, args):
        if args[0].startswith('#'):
            channel = args[0].upper()
            message = args[1]
            self.channels[channel].handleMessage(user,message)

    def key(self,event, lineEdit):
        self.handleChannelSwitch(event,lineEdit)
        message = None
        if event.key() == PyQt5.QtCore.Qt.Key_Return:
            event.accept()
            message = self.makeChannelMessage(lineEdit.text())
            lineEdit.clear()
        else:
            event.ignore()
        return message
    def handleChannelSwitch(self, event, lineEdit):
        if event.key() == PyQt5.QtCore.Qt.Key_F1 and self.inputChannelIndex > 0:
            self.inputChannelIndex -=1
        elif event.key() == PyQt5.QtCore.Qt.Key_F2 and self.inputChannelIndex < len(self.channelNames)-1:
            self.inputChannelIndex +=1
        self.window.setActiveChannel(self.channelNames[self.inputChannelIndex])

    def StackMessage(self,message):
        newMessage = Message(message+'\n\r')
        self.replies.append(newMessage)

    def makeChannelMessage(self, message):
        if message:
            if message.startswith("/"):
                return self.makeMessage(message[1:])
            else:
                self.window.appendText("\n"+self.channelNames[self.inputChannelIndex]+" "+self.userName+":"+message)
                return self.makeMessage("PRIVMSG "+self.channelNames[self.inputChannelIndex]+" :"+message)
        return None
    def makeMessage(self, message):
        newMessage = Message(message+'\n\r')
        return newMessage


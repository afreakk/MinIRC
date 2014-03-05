from ChannelActionHandler import ChannelActionHandler
from utilities import *
import PyQt5.QtWidgets

class DataInterpreter(object):
    def __init__(self, window, settings):
        self.window = window
        self.channelNames = []
        self.autoJoinChannels = settings.channels
        self.userSettings = settings.userSettings
        self.serverSettings = settings.serverSettings

        self.serverSpecificNick = self.userSettings.nick
        self.inputChannelIndex = 0
        self.replies = []
        self.channels = {}

    def interpretData(self, data):
        self.replies = []
        if data['command']:
            self._handleCommand(data)
            self._showData(data)
        return self.replies

    def key(self,event, lineEdit):
        self._handleChannelSwitch(event,lineEdit)
        return self._handleWriteInput(event, lineEdit)

    def register(self):
        self._setNickName()
        self._registerUser()
        return self.replies

    def _showData(self, data):
        if is_number( data['command'] ) and int(data['command']) >= 400:
            self.window.appendText("prfx: |%s| cmd: |%s| args: |%s|" % ( data['prefix'], data['command'], data['args'] ) , "ERRORS")
        elif data['command'] == "NOTICE":
            self.window.appendText("prfx: |%s| cmd: |%s| args: |%s|" % ( data['prefix'], data['command'], data['args'] ) , "NOTICES")
        else:
            self.window.appendText("prfx: |%s| cmd: |%s| args: |%s|" % ( data['prefix'], data['command'], data['args'] ) , "SERVER")

    def _setNickName(self):
        self._stackMessage("NICK  %s\r\n" % self.serverSpecificNick)

    def _nickTaken(self):
        self.serverSpecificNick+="_"

    def _registerUser(self):
        self._stackMessage( "USER %s %s bla :%s\r\n" % (self.userSettings.ident,
            self.serverSettings.host[self.serverSettings.getNumber()], self.userSettings.realname) )

    def _joinChannels(self):
        for channel in self.autoJoinChannels:
            self._stackMessage("JOIN "+channel)

    def _handleCommand(self,data):

        if data['command'] == "PRIVMSG":
            channel = data['args'][0].upper()
            message = data['args'][1]
            nick = data['prefix'];
            self.channels[channel].handleMessage(nick,message)

        elif data['command'] == "PING":
            self._stackMessage('PONG '+data['args'][-1])

        elif data['command'] == "353":
            chanName = data['args'][-2].upper()
            nickList = data['args'][-1]
            self._makeSureExists(chanName)
            self.channels[chanName].appendChannelNicks(nickList)

        elif data['command'] == "JOIN":
            chanName = data['args'][0].upper()
            nick = data['prefix']
            self._makeSureExists(chanName)
            self.channels[chanName].appendNick(nick)

        elif data['command'] == "PART":
            chanName = data['args'][0].upper()
            nick = data['prefix']
            self._makeSureExists(chanName)
            self.channels[chanName].removeNick(nick)

        elif data['command'] == "QUIT":
            nick = data['prefix']
            message = data['args']
            for channelName in self.channels:
                self.channels[channelName].handleNickQuit(nick, message)

        elif data['command'] == "433":
            self._nickTaken()
            self._setNickName()

        elif data['command'] == "376":
            self._joinChannels()


    def _makeSureExists(self, channel):
        if not channel in self.channels:
            self.channels[channel] = ChannelActionHandler(channel, self.window, self.userSettings.nick)
            self.channelNames.append(channel)

    def _handleWriteInput(self, event, lineEdit):
        message = None
        if event.key() == PyQt5.QtCore.Qt.Key_Return:
            event.accept()
            message = self._makeChannelMessage(lineEdit.text())
            lineEdit.clear()
        else:
            event.ignore()
        return message


    def _handleChannelSwitch(self, event, lineEdit):
        if len( self.channelNames ) == 0:
            return
        if event.key() == PyQt5.QtCore.Qt.Key_F1 and self.inputChannelIndex > 0:
            self.inputChannelIndex -=1
        elif event.key() == PyQt5.QtCore.Qt.Key_F2 and self.inputChannelIndex < len(self.channelNames)-1:
            self.inputChannelIndex +=1
        self.window.setActiveChannel(self.channelNames[self.inputChannelIndex])

    def _stackMessage(self,message):
        newMessage = Message(message)
        self.replies.append(newMessage)

    def _makeChannelMessage(self, message):
        if message:
            if message.startswith("/"):
                return self._handleUserCommand(message[1:])
            else:
                return self._sendUserMessage(message)

    def _handleUserCommand(self, message):
        message = message.upper()
        if   message[:4] == "PART":
            message = self._fixUserCommand(message)
        elif message[:4] == "JOIN":
            message = self._fixUserCommand(message)
        return self._makeMessage(message)

    def _fixUserCommand(self, userCommand):
        if not "#" in message:
            cmd, channel = userCommand.split(" ")
            channel = "#"+channel
            userCommand = part+" "+channel
        return userCommand

    def _sendUserMessage(self,message):
        if len(self.channelNames) > 0:
            self.window.appendText(self.serverSpecificNick+":"+message, self.channelNames[self.inputChannelIndex])
            return self._makeMessage("PRIVMSG "+self.channelNames[self.inputChannelIndex]+" :"+message)
        else:
            self.window.appendText(self.serverSpecificNick+":"+message+" join a channel to chat( /join #examplechannel )", "ERRORS")
            return None

    def _makeMessage(self, message):
        newMessage = Message(message)
        return newMessage


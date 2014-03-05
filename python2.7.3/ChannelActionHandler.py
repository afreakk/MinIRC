from utilities import *
import string

class ChannelActionHandler:

    def __init__(self, channelName, window, nick):
        self.channelName = channelName
        self.window = window
        self.window.appendChannel(self.channelName)
        self.selfNick = nick
        self.channelNicks = []

    def appendChannelNicks(self, nickString):
        nickList = nickString.split(" ")
        for nick in nickList:
            nick = self._streamLineNickWithoutIp(nick)
            self._addNickToList(nick)

    def handleNickQuit(self, nickAndIP, message):
        nick = self._streamLineNick(nickAndIP)
        if nick in self.channelNicks:
            self.window.appendText(nickAndIP+" quit:"+listPrint(message), self.channelName)
            self._removeNickFromList(nick)

    def handleMessage(self, nickAndIP, message):
        nick = stripNick(nickAndIP);
        self.window.appendText(nick+":"+message, self.channelName)

    def appendNick(self, nickAndIP):
        nick = self._streamLineNick(nickAndIP)
        if self._isYou(nick):
            self.window.appendText("<- you joined.", self.channelName)
        else:
            self.window.appendText(nick+" joined.", self.channelName)
        self._addNickToList(nick)

    def removeNick(self, nickAndIP):
        nick = self._streamLineNick(nickAndIP)
        self.window.appendText(" "+nick+" left.", self.channelName)
        self._removeNickFromList(nick)

    def _addNickToList(self, nick):
        if self._isYou(nick):
            return
        self.channelNicks.append(nick)
        self.window.appendNick(nick, self.channelName)

    def _removeNickFromList(self, nick):
        if self._isYou(nick):
            return
        if nick in self.channelNicks:
            self.channelNicks.remove(nick)
            self.window.removeNick(nick, self.channelName)

    def _streamLineNick(self, nick):
        nick = stripNick(nick)
        return nick

    def _streamLineNickWithoutIp(self, nickWithAuthotity):
        nick = stripAuthorities(nickWithAuthotity)
        return nick

    def _isYou(self, nick):
        return self._streamLineNick(nick).startswith(self.selfNick)

    def _chanStrCap(self, s):
        return s if len(s)<=3 else s[0:3]




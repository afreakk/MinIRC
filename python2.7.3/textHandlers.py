from collections import defaultdict
import time

class ChannelToggle(object):
    def __init__(self):
        self.totalChannels = {}
        self.totalChannels["SERVER"] = True
        self.totalChannels["ERRORS"] = True
        self.totalChannels["NOTICES"] = True
        self.mutedChannels = []
        self.changed = False
    def initChannels(self, channels):
        for channel in channels:
            self.totalChannels[channel] = True
    def handleMute(self, selectedItems):
        if self.mutedChannels != selectedItems:
            self.mutedChannels = selectedItems
            self.changed = True
            for channel in self.totalChannels:
                self.totalChannels[channel] = True
            for channel in self.mutedChannels:
                self.totalChannels[channel.text()] = False
    def isChanged(self):
        return self.changed
    def setChanged(self, val):
        self.changed = val
    def getTotalChannels(self):
        return self.totalChannels
    def insertChannel(self, channel):
        self.totalChannels[channel] = True
    def removeChannel(self, channel):
        del self.totalChannels[channel]
    def filterChannel(self, chanName):
        if chanName in self.totalChannels:
            return self.totalChannels[chanName]
        print str(chanName) + "was not in "
        return None

class NickHandler(object):
    def __init__(self, channelToggle):
        self.channelToggle = channelToggle
        self.nickXChannelList = defaultdict(list)
        self.fullNickString = ""
        self.filteredNickString = ""

    def filterUserText(self):
        filteredUserText = ""
        users = self.fullNickString.split("\n")
        for user in users:
            if user in self.nickXChannelList:
                for channel in self.nickXChannelList[user]:
                    if self.channelToggle.filterChannel(channel):
                        filteredUserText += ("\n"+user)
                        break
        self.filteredNickString = filteredUserText
        return self.filteredNickString

    def appendNick(self, nick, channel):
        nickToList = None
        if nick not in self.nickXChannelList:
            streamLinedNick = self._streamLineNick(nick)
            self.fullNickString += streamLinedNick
            if self.channelToggle.filterChannel(channel):
                self.filteredNickString += streamLinedNick
                nickToList = streamLinedNick
        self.nickXChannelList[nick].append(channel)
        print "join "+str(len(self.nickXChannelList[nick]))
        return nickToList

    def removeNick(self, nickToRemove, channel):
        self.nickXChannelList[nickToRemove].remove(channel)
        print "leave "+str(len (self.nickXChannelList[nickToRemove]))
        if len( self.nickXChannelList[nickToRemove] ) == 0:
            streamLinedNick = self._streamLineNick(nickToRemove)
            self.fullNickString = self.fullNickString.replace(streamLinedNick, "")
            self.filteredNickString = self.filteredNickString.replace(streamLinedNick, "")
            del self.nickXChannelList[nickToRemove]
            return self.filteredNickString
        return "dont"

    def _streamLineNick(self, nick):
        return nick+"\n"

class MessageHandler(object):
    def __init__(self, channelToggle):
        self.channelToggle = channelToggle
        self.text = ""

    def appendText(self, message, channelName):
        if not channelName in self.channelToggle.getTotalChannels():
            return self.appendText("UNPARSED|"+message+"|", "ERRORS")

        message = self._streamLineMessage(message, channelName)
        self.text += message
        if self.channelToggle.filterChannel(channelName):
            return message
        return "dont"

    def filterText(self):
        filteredText = ""
        lines = self.text.split("\n")
        for line in lines:
            chanName = self._extractChannelName(line)
            if self.channelToggle.filterChannel( chanName ):
                filteredText += ("\n"+line)
        return filteredText

    def _streamLineMessage(self, message, channelName):
        return time.strftime("%H:%M:%S::", time.localtime())+channelName + "::" + message + " \n"

    def _extractChannelName(self, line):
        try:
            chanName = line.split("::")[1]
            return chanName
        except Exception:
            print line

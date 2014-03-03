import sys
import time
import string

import PyQt5.QtGui
import PyQt5.QtWidgets
import PyQt5.uic

from settings import *
from server import ActiveServer

class ChannelToggle(object):
    def __init__(self):
        self.totalChannels = {}
        self.totalChannels["SERVER"] = True
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


class MyWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        PyQt5.uic.loadUi('textEdit.ui', self)

        self.channelToUser = {}
        self.channelToggle = ChannelToggle()

        self.show()
        self.mLoop = getServers(self)
        self.userString = ""
        self.filteredUserString = ""
        self.channelText.itemSelectionChanged.connect(self.selectionChanged)
        self.text = ""
        self.socketUpdateTimer = PyQt5.QtCore.QTimer()
        self.socketUpdateTimer.setInterval(100)
        self.socketUpdateTimer.timeout.connect(self.ircLoop)
        self.startIrcLoop()

    def appendText(self, message):
        chanName = self.extractChannelName(message[1:])
        if self.filterChannel(chanName):
            self.mainText.insertPlainText(message)
            self.mainText.verticalScrollBar().setValue(self.mainText.verticalScrollBar().maximum())
        elif not chanName in self.channelToggle.getTotalChannels():
            self.appendText("\nSERVER UNPARSED|"+message+"|")
        self.text += message

    def appendUser(self, user, channel):
        self.channelToUser[user] = channel

        user = "\n"+user
        self.userString += user
        if self.filterChannel(channel):
            self.filteredUserString += user
            self.userText.insertPlainText(user)

    def removeUser(self, userToRemove):
        del self.channelToUser[user]

        userToRemove = "\n"+userToRemove
        self.userString.replace(userToRemove, "")
        if self.filterChannel(channel):
            self.filteredUserText.replace(userToRemove, "")
        self.userText.setPlainText(self.filteredUserString)

    def selectionChanged(self):
        self.channelToggle.handleMute(self.channelText.selectedItems())
        if self.channelToggle.isChanged():
            self.filterText()
            self.filterUserText()
            self.channelToggle.setChanged(False)

    def appendChannel(self, channel):
        if channel not in self.channelToggle.getTotalChannels():
            self.channelToggle.insertChannel(channel)
        self.channelText.addItem(channel)

    def filterText(self):
        filteredText = ""
        textArr = self.text.split("\n")
        for line in textArr:
            if self.filterChannel( self.extractChannelName(line) ):
                filteredText += ("\n"+line)
            else:
                print "|"+self.extractChannelName(line)+"|"
        self.mainText.setPlainText(filteredText)
        self.mainText.verticalScrollBar().setValue(self.mainText.verticalScrollBar().maximum())
        self.mainText.moveCursor(PyQt5.QtGui.QTextCursor.End)

    def filterUserText(self):
        filteredUserText = ""
        users = self.userString.split("\n")
        for user in users:
            if user in self.channelToUser:
                if self.filterChannel(self.channelToUser[user]):
                    filteredUserText += ("\n"+user)
        self.filteredUserText = filteredUserText
        self.userText.setPlainText(self.filteredUserText)
        self.userText.moveCursor(PyQt5.QtGui.QTextCursor.End)


    def filterChannel(self, chanName):
        if chanName in self.channelToggle.getTotalChannels():
            return self.channelToggle.getTotalChannels()[chanName]
        return None

    def extractChannelName(self, line):
        chanName = line.split(" ")[0]
        chanName = string.rstrip(chanName)
        return chanName

    def startIrcLoop(self):
        self.mLoop.init()
        self.socketUpdateTimer.start()

    def ircLoop(self):
        self.mLoop.mainLoop()


    def setActiveChannel(self, channel):
        self.labelChannel.setText(channel)

    def keyPressEvent(self,event):
        if event.key() == PyQt5.QtCore.Qt.Key_F3:
            self.mLoop.changeInputTargetServer(False, self.labelServer)
        elif event.key() == PyQt5.QtCore.Qt.Key_F4:
            self.mLoop.changeInputTargetServer(True,self.labelServer)
        self.mLoop.key(event, self.lineEdit)










def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

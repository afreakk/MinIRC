from textHandlers import *
from settings import getServers
import PyQt5.uic

class MyWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        PyQt5.uic.loadUi('textEdit.ui', self)
        self.show()

        self.channelToggle = ChannelToggle()
        self.nickHandler = NickHandler(self.channelToggle)
        self.messageHandler = MessageHandler(self.channelToggle)

        self.servers = getServers(self)

        self.socketUpdateTimer = PyQt5.QtCore.QTimer()
        self.socketUpdateTimer.setInterval(100)
        self.socketUpdateTimer.timeout.connect(self.ircLoop)
        self.channelText.itemSelectionChanged.connect(self.selectionChanged)

        self.startIrcLoop()

    def appendText(self, message, channelName):
        message = self.messageHandler.appendText(message, channelName)
        if message != "dont":
            self.mainText.insertPlainText(message)
            self.mainText.verticalScrollBar().setValue(self.mainText.verticalScrollBar().maximum())

    def appendNick(self, nick, channel):
        nick = self.nickHandler.appendNick(nick,channel)
        if nick:
            self.userText.insertPlainText(nick)

    def removeNick(self, nickToRemove, channel):
        remainingNicks = self.nickHandler.removeNick(nickToRemove, channel)
        if remainingNicks != "dont":
            self.userText.setPlainText(remainingNicks)

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
        self.mainText.setPlainText(self.messageHandler.filterText())
        self.mainText.verticalScrollBar().setValue(self.mainText.verticalScrollBar().maximum())
        self.mainText.moveCursor(PyQt5.QtGui.QTextCursor.End)

    def filterUserText(self):
        filteredUserText = self.nickHandler.filterUserText()
        self.userText.setPlainText(filteredUserText)
        self.userText.moveCursor(PyQt5.QtGui.QTextCursor.End)


    def filterChannel(self, chanName):
        if chanName in self.channelToggle.getTotalChannels():
            return self.channelToggle.getTotalChannels()[chanName]
        return None

    def startIrcLoop(self):
        self.servers.init()
        self.socketUpdateTimer.start()

    def ircLoop(self):
        self.servers.mainLoop()


    def setActiveChannel(self, channel):
        self.labelChannel.setText(channel)

    def keyPressEvent(self,event):
        if event.key() == PyQt5.QtCore.Qt.Key_F3:
            self.servers.changeInputTargetServer(False, self.labelServer)
        elif event.key() == PyQt5.QtCore.Qt.Key_F4:
            self.servers.changeInputTargetServer(True,self.labelServer)
        self.servers.key(event, self.lineEdit)


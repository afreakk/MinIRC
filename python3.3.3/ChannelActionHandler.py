from utilities import *
import string
def parseIrcUser(user):
    user = user.replace('~', '') # owners
    user = user.replace('&', '') # admins
    user = user.replace('@', '') # ops
    user = user.replace('%', '') # half-ops
    user = user.replace('+', '') # voiced
    user = user.replace(':', '') # just because
    return user

class ChannelActionHandler:

    def __init__(self, channelName, window, nick):
        self.replies = []
        self.channelName = channelName
        self.window = window
        self.window.appendChannel(self.channelName)
        self.nick = nick

    def handleMessage(self, user, message):
        self.window.appendText("\n"+self.channelName+" "+ user.split("!")[0]+":"+message)

    def appendUsers(self, users):
        temp = users.split( " ")
        for line in temp:
            self.addUserToUserList(line)
    def appendUser(self, user):
        temp = user.split("!")
        self.window.appendText("\n"+self.channelName+" Join: "+temp[0])
        self.addUserToUserList(temp[0])

    def removeUser(self, user):
        temp = user.split("!")
        self.removeUserFromUserList(temp[0])

    def removeUserFromUserList(self,user):
        self.window.removeUser(user)

    def addUserToUserList(self,user):
        if parseIrcUser(user) != self.nick:
            self.window.appendUser(user, self.channelName)


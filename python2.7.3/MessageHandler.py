
class MessageHandler(object):
    def makeChannelMessage(self, message):
        self.makeMessage("PRIVMSG "+self.channel+" :"+message)

    def makeMessage(self,message):
        newMessage = Message(message+'\n\r')
        self.replies.append(newMessage)

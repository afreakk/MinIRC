import time
import string
import math

class PenisUsers(object):
    def __init__(self):
        self.penisUsers = []
    def handleMessage(self, user, message):
        if "!penis" in message:
            if user in self.penisUsers:
                self.penisUsers = filter(lambda a: a != user, self.penisUsers)
            else:
                self.penisUsers.append(user)
        else:
            if user in self.penisUsers:
                return "penis"
        return None


class USA(object):
    def __init__(self):
        self.flag = (
         "7,0                  //0,2* * * * * * 4,4#####################################"
        , "7,0                 //0,2* * * * * * 0,0###############"
        , "7,0                //0,2* * * * * * 4,4##############################"
        , "7,0               //0,2* * * * * * 0,0###&###### "
        , "7,0              //4,4################################## "
        , "7,0             //0,0###&##################  "
        , "7,0            //4,4############################## "
        , "7,0           //                            "
        , "7,0          /(                           ")
    def handleMessage(self, user, message):
        if "usa!!!" in message:
            return self.flag
class Arithmetic(object):
    def __init__(self):
        pass
    def handleMessage(self,user,message):
        if message.startswith("="):
            return str(self.calculate(message[1:]))
        return None

    def calculate(self, raw):
        try:
            result = eval(raw)
        except:
            result = "error"
        return result

class DatabaseMessage(object):
    def __init__(self, user, message, channel):
        self.user = user
        self.message = message
        self.channel = channel
class Logger(object):
    def __init__(self):
        self.messages = []
        pass
    def handleMessage(self,user,message,channel):
        self.messages.append( DatabaseMessage(user,message,channel))
        if message.startswith("!search"):
            self.search(message[8:])

    def search(self, word):
        pass





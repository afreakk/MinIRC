from server import ActiveServer, IrcLoop
from settingClasses import *

class Server_Freenode(object):
    host = ("chat.freenode.net", "adams.freenode.net", "barjavel.freenode.net", "calvino.freenode.net", "cameron.freenode.net", "gibson.freenode.net"
            , "hitchcock.freenode.net", "hobana.freenode.net", "holmes.freenode.net", "kornbluth.freenode.net", "leguin.freenode.net", "orwell.freenode.net")
    port = 6665
    channels = ["#theuberleets"]

class Server_Quakenet(object):
    host = ("underworld2.no.quakenet.org", "underworld1.no.quakenet.org", "servercentral.il.us.quakenet.org"
            , "portlane.se.quakenet.org", "port80c.se.quakenet.org", "port80a.se.quakenet.org", "jubii2.dk.quakenet.org")
    port = 6666
    channels = ["#koug", "#grimbatolx"]

class YourUserName(object):
    nick = "afreak_"
    ident = "afreak"
    realname = "afreak"

def getServers(mainWindow):
    freenode = ServerSettings(Server_Freenode)
    userSettings = UserSettings(YourUserName)
    freenodeSettings = Settings(freenode, userSettings)
    serverFreenode = ActiveServer(freenodeSettings, mainWindow)

    quakenet = ServerSettings(Server_Quakenet)
    quakenetSettings = Settings(quakenet, userSettings)
    serverQuakenet = ActiveServer(quakenetSettings, mainWindow)

    servers = [serverQuakenet,serverFreenode]

    #-------------------------------------------------------------> end settings
    ircLoop = IrcLoop(servers, mainWindow.labelServer)
    return ircLoop


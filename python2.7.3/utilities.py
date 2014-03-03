def sendData(ircSocket,message,window):
    ircSocket.send(message)

class Message(object):
    def __init__(self, message):
        self.message = message
    def getMessage(self):
        return self.message

def organizeData(s):
    """Breaks a message from an IRC server into its prefix, command, and arguments.
    """
    prefix = ''
    trailing = []
    if not s:
       raise Exception("Empty line.")
    try:
        if s[0] == ':':
            prefix, s = s[1:].split(' ', 1)
        if s.find(' :') != -1:
            s, trailing = s.split(' :', 1)
            args = s.split()
            args.append(trailing)
        else:
            args = s.split()
        organizeData = {}
        organizeData['prefix'] = prefix
        organizeData['args'] = args
        organizeData['command'] = args.pop(0)
        return organizeData
    except Exception as inst:
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst           # __str__ allows args to printed directly
        return None

def sendData(ircSocket,message,window):
    ircSocket.send(message)

def stripIP(nickAndIP):
    return nickAndIP.split("!")[0]

def stripAuthorities(nick):
    nick = nick.replace('~', '') # owners
    nick = nick.replace('&', '') # admins
    nick = nick.replace('@', '') # ops
    nick = nick.replace('%', '') # half-ops
    nick = nick.replace('+', '') # voiced
    nick = nick.replace(':', '') # just because
    return nick

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def stripNick(nick):
    nick = stripIP(nick)
    nick = stripAuthorities(nick)
    return nick

def listPrint(potentialList):
    if is_string(potentialList):
        return potentialList
    msg = ""
    for entry in potentialList:
        msg += entry
    return msg

class Message(object):
    def __init__(self, message):
        self.message = message+"\r\n"
    def getMessage(self):
        return self.message

def is_string(s):
  return isinstance(s, basestring)

def parseLine(s):
    """Breaks a message from an IRC server into its prefix, command, and arguments.
    """
    prefix = ''
    trailing = []
    if not s:
        return
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


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

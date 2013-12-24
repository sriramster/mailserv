import ConfigParser

class ParseConfig():
    """ Implements, m using microsoft config format. All GNU god's forgive me read config from file """
    path = "config"
    data = {}

    def __init__(self):
        """ Init """
        q = open(self.path ,"r")
        if q is None:
            print 'Error'
            return -1
        self.parse(q)

    def parse(self, instance):
        config = ConfigParser.RawConfigParser()
        c = config.readfp(instance)
        section = config.sections()
        for i in section:
            self.data[i] = config.items(i)

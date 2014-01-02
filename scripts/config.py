# Parse the config file to get data

import ConfigParser

class ParseConfig():
    """ Implements, using microsoft config format. All GNU god's forgive """
    path = "/home/sriram/src/mailserv/conf/config"
    data = {}
    section = {}

    def __init__(self):
        """ Init """
        q = open(self.path ,"r")
        if q is None:
            # Better handling to be written
            return -1
        self.parse(q)

    def parse(self, instance):
        config = ConfigParser.RawConfigParser()
        c = config.readfp(instance)
        self.section = config.sections()
        for i in self.section:
            self.data[i] = config.items(i)
        return self.data

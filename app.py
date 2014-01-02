import logging
from scripts import config
from scripts import imap,pop3,utils

class Application():
    """ The application Init happens here """
    logger = logging.getLogger("MAILSERV")
    
    def __init__(self):
        self.logger.info('Application __init__')
        c = config.ParseConfig()
        if c is None:
            return None
        mdata = c.data
        section = c.section
        
        if mdata is None:
            print 'No Config Data Availabe' 
            return None
        if section is None:
            print 'No Section data available'
            return None
        
        serv = {}
        conndet = []
        cconfig = {}

        for i in section:
            if (i == 'common'):
                cconfig = utils.create_cconfig(mdata[i])
            else:
                serv = utils.create_config(mdata[i])
                conndet.append(serv)

        # create connection for each server read
        for i in range(len(conndet)):
            __conn__ = conndet[i]
            if (__conn__['proto'] == 'pop3'):
                self.con = pop3.Pop3MailQueue(__conn__, cconfig)
            self.con = imap.ImapMailQueue(__conn__, cconfig)

    def poll(self):
        self.con.get_mail(search='UNSEEN')

c = Application()

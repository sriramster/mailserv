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

        for i in section:
            if (i == 'common'):
                return
            serv = utils.create_config(mdata[i])
            if (serv['proto'] == 'pop3'):
                self.con = pop3.Pop3MailQueue(serv)
            self.con = imap.ImapMailQueue(serv)

    def poll(self):
        self.con.get_mail(search='UNSEEN')

c = Application()

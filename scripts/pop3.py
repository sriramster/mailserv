import poplib as pop3
import config

class Pop3MailQueue():
    """ Implement's pop3 version of the mail retrival """

    con = ''
    count = 0
    msg = ''

    def __init__(self, conf):
        if conf is None:
            print 'No config Available'
            return -1
        
        if conf['port'] == '995':
            self.con = pop3.POP3_SSL(conf['server'],conf['port'])
        else:
            self.con = pop3.POP3(conf['server'],conf['port'])
        
        if self.con is None:
            print 'Pop3 connection unabailable'
            return -1
        self.con.user(conf['uname'])
        self.con.pass_(conf['pswd'])
        self.count = len(self.con.list()[1])

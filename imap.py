import imaplib as imap
import config

class ImapMailQueue():
    """ Implement's pop3 version of the mail retrival """

    con = ''
    count = 0
    msg = ''

    def __init__(self, conf):
        if conf is None:
            print 'No config Available'
            return -1
        
        if conf['port'] == '993':
            self.con = imap.IMAP4_SSL(conf['server'],conf['port'])
        else:
            self.con = imap.IMAP4(conf['server'],conf['port'])

        self.con.login(conf['uname'],conf['pswd'])
        if self.con is None:
            print 'Failed to connect'
            return -1
        self.get_all_mail()

    def get_mail_count(self):
        count = self.con.select()
        self.count = count.__getitem__(1)

    def get_all_mail(self):
        if self.con is None:
            print 'Unable to connect'
            return -1
        self.con.select()
        stat, data = self.con.search(None,'ALL')
        if (stat != 'OK'):
            print 'Error'
            return -1

        for i in data[0].split():
            stat, data = self.con.fetch(i, '(RFC822)')
            self.msg = data[0][1]
            if self.msg is None:
                print 'Msg Has No Content'
                return 0
            # do_parse_msg(self.msg)
            print 'Message %s\n%s\n' % (i, self.msg)

    def get_mail_by_idx(self, idx):
        if idx is None:
            print 'No Proper Idx specfied'
            return -1
        self.con.select()
        stat, data = self.con.fetch(idx, '(RFC822)')
        if (stat != 'OK'):
            print 'Error'
            return -1
        self.msg = data[0][1]

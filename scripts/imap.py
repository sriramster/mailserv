# Implementing, a minimal imap server here with python imaplib. 
# None of the search features will be implemeted here, the plan is to make search really quick [No pun intended]
# Search will be handled locally, by some awesome [Pun Inteded] indexing and hashing technology

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
        # Get unseen messages map
        self.get_mail(search='UNSEEN')

    def get_all_count(self, cond=None):
        count = self.con.select()
        self.count = count.__getitem__(1)

    def get_mail(self, search=None,cond=None):
        if self.con is None:
            print 'Unable to connect'
            return -1
        self.con.select()
        stat, data = self.con.search(None,search)
        if (stat != 'OK'):
            print 'Error'
            return -1

        if cond is None:
            cond = '(RFC822)'

        for i in data[0].split():
            stat, data = self.con.fetch(i, cond)
            self.msg = data[0][1]
            if self.msg is None:
                print 'Msg Has No Content'
                return 0
            # do_parse_msg(self.msg)
            print 'Message %s\n%s\n' % (i, self.msg)
        self.mailbox_logout()

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

    def mailbox_logout(self):
        if self.con is None:
            print 'Logged out or Error'
            return -1
        self.con.close()
        self.con.logout()
        return 0

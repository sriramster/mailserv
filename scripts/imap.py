# Implementing, a minimal imap server here with python imaplib.
# None of the search features will be implemeted here, the plan is to make search really quick [No pun intended]
# Search will be handled locally, by some awesome [Pun Inteded] indexing and hashing technology

import imaplib as imap
import config

import email
import smtplib as smtp
from email.mime.text import MIMEText as mimef

class ImapMailQueue():
    """ Implement's imap version of the mail retrival """

    con = None
    count = 0
    msg = ''

    def __init__(self, conf=None):
        if conf is None:
            print 'No config Available'
            return None
        
        if self.con is None:
            if conf['port'] == '993':
                self.con = imap.IMAP4_SSL(conf['server'],conf['port'])
            else:
                self.con = imap.IMAP4(conf['server'],conf['port'])

            self.con.login(conf['uname'],conf['pswd'])
            if self.con is None:
                print 'Failed to connect'
                return None

            self.get_mail(search='ALL')
        else:
            return 

    def get_all_count(self, cond=None):
        count = self.con.select()
        self.count = count.__getitem__(1)

    def get_mail(self, select=None,search=None,cond=None):
        if self.con is None:
            print 'Unable to connect'
            return -1
            
        if select is None:
            select = 'INBOX'

        self.con.select(select)
        stat, data = self.con.search(None,search)
        if (stat != 'OK'):
            print 'Error'
            return -1

        if cond is None:
            cond = '(RFC822)'

        # [::Cleanup::]
        for i in data[0].split():
            stat, data = self.con.fetch(i, cond)
            self.msg = data[0][1]
            if self.msg is None:
                print 'Msg Has No Content'
                return 0
            # do_parse_msg(self.msg)
            # The big technology will come here
            file_name = '/home/sriram/src/python/mail_try/maildir/' + i +'.mime'
            c = open(file_name,'w')
            q = email.message_from_string(self.msg)
            c.write(q.as_string())
            c.close()
        # self.mailbox_logout()

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

    def get_mailbox_list(self):
        if self.con is None:
            return -1
        stat, data =  self.con.list()
        if (stat != 'OK'):
            return -1
        print 'Data',data

    def mailbox_logout(self):
        if self.con is None:
            print 'Logged out or Error'
            return -1
        self.con.close()
        self.con.logout()
        return 0

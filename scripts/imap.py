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

    count = 0
    msg = ''
    conf = {}

    def __init__(self, conf=None):
        if conf is None:
            print 'No config Available'
            return None
        self.conf = conf

        if self.conf['con'] is None:
            if self.conf['port'] == '993':
                self.conf['con'] = imap.IMAP4_SSL(self.conf['server'],self.conf['port'])
            else:
                self.conf['con'] = imap.IMAP4(self.conf['server'],self.conf['port'])

            self.conf['con'].login(self.conf['uname'],self.conf['pswd'])
            if self.conf['con'] is None:
                print 'Failed to connect'
                return None

            self.get_mail(search='ALL')
        else:
            return 

    def get_all_count(self, cond=None):
        count = self.conf.con.select()
        self.count = count.__getitem__(1)

    def get_mail(self, select=None,search=None,cond=None):
        if self.conf['con'] is None:
            print 'Unable to connect'
            return -1
            
        if select is None:
            select = 'INBOX'

        self.conf['con'].select(select)
        stat, data = self.conf['con'].search(None,search)
        if (stat != 'OK'):
            print 'Error'
            return -1

        if cond is None:
            cond = '(RFC822)'

        # [::Cleanup::]
        for i in data[0].split():
            stat, data = self.conf['con'].fetch(i, cond)
            self.msg = data[0][1]
            if self.msg is None:
                print 'Msg Has No Content'
                return 0
            # do_parse_msg(self.msg)
            # The big technology will come here
            file_name = '/home/sriram/src/python/mail_try/maildir/'+ self.conf['mbox'] +'/' + i #+'.mime'
            c = open(file_name,'w')
            c.write(self.msg)
            c.close()
        # self.mailbox_logout()

    def get_mail_by_idx(self, idx):
        if idx is None:
            print 'No Proper Idx specfied'
            return -1
        self.conf['con'].select()
        stat, data = self.conf['con'].fetch(idx, '(RFC822)')
        if (stat != 'OK'):
            print 'Error'
            return -1
        self.msg = data[0][1]

    def get_mailbox_list(self):
        if self.conf['con'] is None:
            return -1
        stat, data =  self.conf['con'].list()
        if (stat != 'OK'):
            return -1
        print 'Data',data

    def mailbox_logout(self):
        if self.conf['con'] is None:
            print 'Logged out or Error'
            return -1
        self.conf['con'].close()
        self.conf['con'].logout()
        return 0

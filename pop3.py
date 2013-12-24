import poplib as pop3
import config

class Pop3MailQueue():
    """ Implement's pop3 version of the mail retrival """
    def __init__(self):
        c = config.ParseConfig()

c = Pop3MailQueue()

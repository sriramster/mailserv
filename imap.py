import imaplib as imap
import config

class ImapMailQueue():
    """ Implement's pop3 version of the mail retrival """
    def __init__(self):
        c = config.ParseConfig()

c = ImapMailQueue()

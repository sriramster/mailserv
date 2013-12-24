import config
import imap,pop3

class Application():
    """ The application Init happens here """
    
    def __init__(self):
        c = config.ParseConfig()
        if c is None:
            return -1
        data = c.data
        section = c.section
        
        if data is None:
            print 'No Config Data Availabe' 
            return -1
        if section is None:
            print 'No Section data available'
            return -1
        
        serv = {}

        for i in section:
            serv['encrypted'] = self.do_parse(data[i][0])
            serv['pollinterval'] = self.do_parse(data[i][1])
            det = self.do_parse(data[i][2])
            q = det.split(' ')
            serv['proto']  = q[0]
            serv['uname']  = q[1]
            serv['pswd']   = q[2]
            serv['server'] = q[3]
            serv['port']   = q[4]
            
            if (serv['proto'] == 'pop3'):
                c = pop3.Pop3MailQueue(serv)
            c = imap.ImapMailQueue(serv)

    def do_parse(self,data):
        if data is None:
            return ''
        return data.__getitem__(1)
        
q = Application()

import logging,time,os
from lib.daemon import runner
from scripts import pop3,imap,config,utils
import app

class App():
    appstate = 0
    app = None

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        try:
            self.pidfile_path =  '/home/sriram/tmp/mailserv/testdaemon.pid'
        except IOError:
            os.mkdir('/home/sriram/tmp/mailserv')
            self.pidfile_path =  '/home/sriram/tmp/mailserv/testdaemon.pid'
        self.pidfile_timeout = 100
           
    def run(self):
        pconfig = config.ParseConfig
        logger.info('Starting mailserv')
        while True:
            self.startApp()
            # This is timeout after which, the next wake up occurs
            poll_interval = pconfig['common'][0]['pollinterval']
            print poll_interval
            time.sleep(poll_interval)

    def stop(self):
        # need to implement logout from multiple servers
        logger.info('Stopping Daemon')

    def wakeup(self):
        self.app.poll()
        logger.info('Polling for new mails')

    def startApp(self):
        if (self.appstate == 0):
            logger.info('Starting MailServ')
            self.app = app.Application()
            self.appstate = 1
        else:
            self.wakeup()


c = App()
# Most of the log generations stuffs [::Cleanup::]
logger = logging.getLogger("MAILSERV")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
try:
    handler = logging.FileHandler("/home/sriram/.mailserv/log/testdaemon.log")
except IOError:
    os.mkdir("/home/sriram/.mailserv/")
    os.mkdir("/home/sriram/.mailserv/log")
    handler = logging.FileHandler("/home/sriram/.mailserv/log/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)
daemon_runner = runner.DaemonRunner(c)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()


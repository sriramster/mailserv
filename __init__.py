import logging,time
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
        self.pidfile_path =  '/home/sriram/tmp/mailserv/testdaemon.pid'
        self.pidfile_timeout = 100
           
    def run(self):
        logger.info('Starting mailserv')
        while True:
            self.startApp()
            # This is timeout after which, the next wake up occurs
            time.sleep(200)

    def stop(self):
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
handler = logging.FileHandler("/home/sriram/tmp/mailserv/log/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(c)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()

import logging,time
from daemon import runner
from scripts import pop3,imap,config
import app

class App():
    appstate = 0

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/home/sriram/tmp/mailserv/testdaemon.pid'
        self.pidfile_timeout = 10
           
    def run(self):
        print 'Start App'
        while True:
            self.startApp()
            # This is timeout after which, the next wake up occurs
            time.sleep(10)

    def wakeup(self):
        logger.info('Wakeup Thread')

    def startApp(self):
        if (self.appstate == 0):
            logger.info('Starting MailServ')
            q = app.Application()
            self.appstate = 1
        else:
            self.wakeup()
        
c = App()

# Most of the log generations stuffs [::Cleanup::]
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/home/sriram/tmp/mailserv/log/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(c)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()


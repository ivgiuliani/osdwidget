import time
import threading
import libgmail

from settings import GMAIL_USER, GMAIL_PASS, GMAIL_CHECK_INTERVAL

class GmailOsd(threading.Thread):
    def __init__(self, osd, *args, **kwargs):
        self.osd = osd

        super(GmailOsd, self).__init__(*args, **kwargs)

    def run(self):
        self.osd.display("Connecting to GMail...")

        self.ga = libgmail.GmailAccount(GMAIL_USER, GMAIL_PASS)

        try:
            self.ga.login()
        except libgmail.GmailLoginFailure:
            self.osd.display("GMail login failure!")

        while True:
            self.gmail_check()
            time.sleep(GMAIL_CHECK_INTERVAL * 60)

    def gmail_check(self):
        unread = self.ga.getUnreadMsgCount()

        self.osd.set_colour("green")
        if unread == 0:
            self.osd.display("No unread emails!")
        else:
            if unread > 30:
                self.osd.set_colour("red")
            elif unread > 15:
                self.osd.set_colour("yellow")

            if unread == 1:
                self.osd.display("You got one unread email")
            else:
                self.osd.display("You got %d unread emails" % self.ga.getUnreadMsgCount())

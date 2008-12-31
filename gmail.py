import time
import threading
import libgmail

from settings import GMAIL_USER, GMAIL_PASS, GMAIL_CHECK_INTERVAL
from base import BaseWidget

class GMailWidget(BaseWidget):
    pass

class GmailOsd(threading.Thread):
    def __init__(self, osd, *args, **kwargs):
        self.osd = osd
        self.msg = ""

        super(GmailOsd, self).__init__(*args, **kwargs)

    def run(self):
        self.msg = "Connecting to GMail..."
        self.osd.display(self.msg)

        self.ga = libgmail.GmailAccount(GMAIL_USER, GMAIL_PASS)

        try:
            self.ga.login()
        except libgmail.GmailLoginFailure:
            self.msg = "GMail login failure!"
            self.osd.display(self.msg)

        while True:
            self.gmail_check()
            time.sleep(GMAIL_CHECK_INTERVAL * 60)

    def refresh(self):
        self.osd.display(self.msg)

    def gmail_check(self):
        unread = self.ga.getUnreadMsgCount()

        self.osd.set_colour("green")
        if unread == 0:
            self.msg = "No unread emails!"
        else:
            if unread > 30:
                self.osd.set_colour("red")
            elif unread > 15:
                self.osd.set_colour("yellow")

            if unread == 1:
                self.msg = "You got one unread email"
            else:
                self.msg = "You got %d unread emails" % self.ga.getUnreadMsgCount()

        self.osd.display(self.msg)

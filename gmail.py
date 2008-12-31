import time
import threading
import libgmail

import settings
from base import BaseWidget

class GMailWidget(BaseWidget):
    def __init__(self):
        super(GMailWidget, self).__init__()
        self.set_horizontal_offset(350)

        self.username = settings.GMAIL_USER
        self.password = settings.GMAIL_PASS

        self.check_thread = GMailCheck(self.username, self.password)
        self.check_thread.start()

    def get_msg(self):
        msg_count = self.check_thread.get_msg_count()

        if msg_count == GMailCheck.CONNECTING:
            return ("Connecting...", "yellow")
        elif msg_count == GMailCheck.CONNECTION_FAILURE:
            return ("Can't connect to GMail!", "red")
        elif msg_count == GMailCheck.LOGIN_FAILURE:
            return ("Can't login in GMail!", "red")
        elif msg_count == 0:
            return ("Empty inbox!", "green")
        elif msg_count == 1:
            return ("Got one unread message", "green")
        elif 1 > msg_count >= 10:
            return ("Got %d unread messages", "green")
        elif 10 > msg_count >= 20:
            return ("Got %d unread messages", "yellow")
        else:
            return ("Got %d unread messages", "red")

class GMailCheck(threading.Thread):
    # various constants
    CONNECTING = -1
    LOGIN_FAILURE = -2
    CONNECTION_FAILURE = -3

    def __init__(self, username, password, *args, **kwargs):
        self.msg_count = self.CONNECTING
        self.username = username
        self.password = password

        super(GMailCheck, self).__init__(*args, **kwargs)

    def get_msg_count(self):
        return self.msg_count

    def gmail_login(self):
        self.ga = libgmail.GmailAccount(self.username, self.password)
        try:
            self.ga.login()
        except libgmail.GmailLoginFailure:
            return False
        return True

    def run(self):
        if not self.gmail_login():
            self.msg_count = self.LOGIN_FAILURE
            return

        while True:
            self.msg_count = self.ga.getUnreadMsgCount()
            time.sleep(settings.GMAIL_CHECK_INTERVAL * 60)

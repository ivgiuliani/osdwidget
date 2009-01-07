import time
import threading
import libgmail
import urllib2

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

        error_messages = {
            GMailCheck.CONNECTING:          ("Connecting...", "yellow"),
            GMailCheck.CONNECTION_FAILURE:  ("Can't connect to GMail!", "red"),
            GMailCheck.LOGIN_FAILURE:       ("Can't login in GMail", "red")
        }

        if msg_count in error_messages.keys():
            return error_messages[msg_count]

        color = "green"
        if msg_count == 0:
            msg = "Empty inbox!"
        elif msg_count == 1:
            msg = "Got one unread message"
        else:
            msg = "Got %d unread messages" % msg_count
            if 10 < msg_count <= 20: color = "yellow"
            elif msg_count > 20: color = "red"

        return (msg, color)

class GMailCheck(threading.Thread):
    # various constants
    CONNECTING          = -1
    LOGIN_FAILURE       = -2
    CONNECTION_FAILURE  = -3

    def __init__(self, username, password, *args, **kwargs):
        self.msg_count = self.CONNECTING
        self.username = username
        self.password = password
        self.logged_in = False
        self.use_proxy = False

        super(GMailCheck, self).__init__(*args, **kwargs)

    def get_msg_count(self):
        return self.msg_count

    def gmail_connect(self):
        "Connect to GMail"
        if settings.FALLBACK_PROXY:
            try:
                self.ga = libgmail.GmailAccount(self.username, self.password)
                return True
            except urllib2.URLError:
                if settings.PROXY_HOST and settings.PROXY_PORT:
                    libgmail.PROXY_URL = "%s:%s" % (settings.PROXY_HOST, settings.PROXY_PORT)
                    self.use_proxy = True
        else:
            if settings.PROXY_HOST and settings.PROXY_PORT:
                libgmail.PROXY_URL = "%s:%s" % (settings.PROXY_HOST, settings.PROXY_PORT)
                self.use_proxy = True

        try:
            self.ga = libgmail.GmailAccount(self.username, self.password)
        except urllib2.URLError:
            return False
        return True


    def gmail_login(self):
        """
        Log into GMail
        """
        try:
            self.ga.login()
        except libgmail.GmailLoginFailure:
            self.logged_in = False
            return False

        self.logged_in = True
        return True

    def run(self):
        """
        Executes the actual email check
        """
        self.gmail_connect()

        while True:
            if not self.logged_in:
                if not self.gmail_login():
                    self.msg_count = self.LOGIN_FAILURE

            # if we logged in correctly or were already logged in
            if self.logged_in:
                try:
                    self.msg_count = self.ga.getUnreadMsgCount()
                except urllib2.URLError:
                    # we may lose the connection, so try to login once
                    # again next time
                    self.logged_in = False
                    self.msg_count = self.CONNECTION_FAILURE

            time.sleep(settings.GMAIL_CHECK_INTERVAL * 60)

import threading
from threading import Thread

from django.core.mail import send_mail

from sn_LifeLine.settings import EMAIL_HOST_USER


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.html_content = html_content
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)


def send_mail_async(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()

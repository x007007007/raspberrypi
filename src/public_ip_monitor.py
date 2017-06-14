#!/usr/bin/env python
import requests
import time
from collections import OrderedDict
import smtplib
from email.mime.text import MIMEText
import os


_ip_checker_list = OrderedDict()
_notifications = set()

def registered_ip_checker(fn):
    _ip_checker_list[fn] = None
    return fn

def registered_notification(fn):
    _notifications.add(fn)
    return fn

@registered_ip_checker
def get_ip_from_ipconfig_dot_me(old):
    try:
        res = requests.get("http://ipconfig.me/ip")
    except:
        return old
    if res.status_code not in (200, 201):
        return old
    return res.text.strip()


@registered_notification
def send_email(new_ip, old_ip):
    from_addr = os.environ.get("NOTIFICATION_EMAIL_FROM")
    to_addr = os.environ.get("NOTIFICATION_EMAIL_TO")
    password = os.environ.get("NOTIFICATION_EMAIL_PASSWD")
    if from_addr and to_addr and password:
        msg = MIMEText("""
            IP Change Form {} to {}
        """.format(new_ip, old_ip))
        msg['Subject'] = 'IP Change Form {} to {}'.format(new_ip, old_ip)
        msg['From'] = from_addr
        msg['To'] = to_addr
        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.set_debuglevel(1)
        server.starttls()
        server.login(from_addr, password)
        server.send(msg.as_string())
        server.close()
    else:
        print("email environ error")

def monitor():
    need_notification = []
    while True:
        for fn, ip in _ip_checker_list.items():
            print(fn)
            n_ip = fn(ip)
            if n_ip != ip and ip is not None:
                need_notification = [(n_ip, ip)]
            _ip_checker_list[fn] = n_ip
        while len(need_notification) > 0:
            n_ip, ip = need_notification.pop()
            try:
                for nfn in _notifications:
                    nfn(n_ip, ip)
            except:
                import traceback
                traceback.print_exc()
                need_notification.append((n_ip, ip))
        time.sleep(10)


if __name__ == "__main__":
    monitor()
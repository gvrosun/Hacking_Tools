#!/usr/bin/env python

import subprocess
import smtplib

command = "dir"


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


subprocess.Popen(command, shell=True)

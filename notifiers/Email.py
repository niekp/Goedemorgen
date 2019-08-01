# -*- coding: utf-8 -*-
import smtplib
import datetime
from lib import Functions as f
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, config_all):
        self.config = config_all
        self.emailadres = config_all["Email"]["emailadres"]

    def Send(self, text):
        # Geheimen inladen
        smtp = self.config["Runtime"]["secrets"]["email_server"]
        user = self.config["Runtime"]["secrets"]["email_username"]
        password = self.config["Runtime"]["secrets"]["email_password"]

        # Verbind met mailserver
        mailserver = smtplib.SMTP(smtp)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(user, password)

        # Mailbericht opbouwen
        message = MIMEMultipart('alternative')

        goede = f.Goede(self.config)

        message['Subject'] = goede
        message['From'] = goede + " <" + user + ">"
        message['To'] = self.emailadres

        html = text
        message.attach(MIMEText(html, "html", "utf-8"))

        # E-mail versturen
        mailserver.sendmail(user, self.emailadres, message.as_string())

        # Verbinding sluiten
        mailserver.close()

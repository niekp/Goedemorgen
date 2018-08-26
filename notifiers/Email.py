# -*- coding: utf-8 -*-
import smtplib, datetime
from lib import Functions as f
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
	def __init__(self, config_all):
		self.config = config_all
		self.emailadres = config_all["Email"]["emailadres"]

	def Send(self, text):
		# Geheimen inladen
		domain = self.config["Runtime"]["secrets"]["email_domain"]
		password = self.config["Runtime"]["secrets"]["email_password"]

		now = f.Now(self.config)

		# Verbind met mailserver
		mailserver = smtplib.SMTP("mail." + domain);
		mailserver.ehlo();
		mailserver.starttls();
		mailserver.ehlo();
		mailserver.login('noreply@'+ domain, password);

		# Mailbericht opbouwen
		message = MIMEMultipart('alternative')

		goede = f.Goede(self.config)
		
		message['Subject'] = goede
		message['From'] = goede + " <noreply@" + domain + ">"
		message['To'] = self.emailadres

		html = text
		message.attach(MIMEText(html, "html", "utf-8"));

		# E-mail versturen
		mailserver.sendmail("noreply@" + domain, self.emailadres, message.as_string())

		# Verbinding sluiten
		mailserver.close();
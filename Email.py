# -*- coding: utf-8 -*-
import smtplib, datetime
import pytz
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

		if 'TZ' in self.config:
			tz = pytz.timezone(self.config["TZ"])
		else:
			tz = pytz.timezone("Europe/Amsterdam")

		# Verbind met mailserver
		mailserver = smtplib.SMTP("mail." + domain);
		mailserver.ehlo();
		mailserver.starttls();
		mailserver.ehlo();
		mailserver.login('noreply@'+ domain, password);

		# Mailbericht opbouwen
		message = MIMEMultipart('alternative')

		if tz.localize(datetime.datetime.now()).hour >= 19:
			message['Subject'] = "Goedenavond"
		elif tz.localize(datetime.datetime.now()).hour >= 12:
			message['Subject'] = "Goedemiddag"
		else:
			message['Subject'] = "Goedemorgen"

		message['Subject'] = "Goedemorgen"
		message['From'] = "Goedemorgen <noreply@" + domain + ">"
		message['To'] = self.emailadres

		html = text
		message.attach(MIMEText(html, "html", "utf-8"));

		# E-mail versturen
		mailserver.sendmail("noreply@" + domain, self.emailadres, message.as_string())

		# Verbinding sluiten
		mailserver.close();
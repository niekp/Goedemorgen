# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
	def __init__(self, config):
		self.emailadres = config["emailadres"]

	def Send(self, text):
		# Geheimen inladen
		domain = open("secrets/email_domain.txt", "r").read()
		password = open("secrets/email_password.txt", "r").read()

		# Verbind met mailserver
		try:
		   mailserver = smtplib.SMTP("mail." + domain);
		   mailserver.ehlo();
		   mailserver.starttls();
		   mailserver.ehlo();
		   mailserver.login('noreply@'+ domain, password);
		except Exception as e:
		   print e;

		# Mailbericht opbouwen
		message = MIMEMultipart('alternative')

		message['Subject'] = "Goedemorgen"
		message['From'] = "Goedemorgen <noreply@" + domain + ">"
		message['To'] = self.emailadres

		html = text
		message.attach(MIMEText(html, "plain", "utf-8"));

		# E-mail versturen
		mailserver.sendmail("noreply@" + domain, self.emailadres, message.as_string())

		# Verbinding sluiten
		mailserver.close();


		print "Goedemorgen verstuurd naar " + self.emailadres
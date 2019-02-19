# -*- coding: utf-8 -*-
import os, datetime, json, locale
import sys, socket
from os import walk
import pytz

from Config import Config

from modules import *
from notifiers import *
from lib import Functions as f

# Cachedir voor vandaag maken indien nodig. Voor het zetten van de locale
datadir = "data/{0}/".format(datetime.datetime.today().strftime('%Y%m%d'))
if not os.path.isdir(datadir):
	os.makedirs(datadir)


# Elke user heeft een config file. Op mijn PC alleen test draaien, op de webserver iedereen (behalve sample en test)
users = []
prod = True
if socket.gethostname() == "Swifty":
	users.append("test")
	prod = False
elif socket.gethostname() == "webserver":
	for (dirpath, dirnames, filenames) in walk("config"):
		for filename in filenames:
			conf_file = filename.replace(".json", "")
			if (conf_file != "test" and conf_file != "sample"):
				users.append(conf_file)


for user in users:
	# Config inlezen
	run = True

	try:
		config = Config(user).GetConfig()
	except Exception as e:
		print("Error: de config van {0} is niet correct.".format(user))
		run = False
		pass


	if run:
		# Set de locale, voor de tijd functies (agenda) en de tijd van de cron
		if 'Locale' in config:
			locale.setlocale(locale.LC_TIME, '{0}.UTF-8'.format(config["Locale"]))

		# Checken of je de notificatie dit uur wilt ontvangen? 
		run = False
		if 'Tijd' in config:
			if f.Now(config).hour in config["Tijd"]:
				run = True

	if run:

		userdir = "data/{0}/".format(user)
		if not os.path.isdir(userdir):
			os.makedirs(userdir)
			
		# Config extenden met runtime variabelen
		with open('secrets/secrets.json') as secrets:    
			config['Runtime'] = { "datadir": datadir, "userdir": userdir, "secrets": json.load(secrets), "production": prod, "user": user }

		# Modules toevoegen
		modules = []

		if "Afval" in config:
			modules.append(Afval(config))

		if "Weer" in config:
			modules.append(Weer(config))

		if "Agenda" in config:
			modules.append(Agenda(config))

		if "MarkdownTodo" in config:
			modules.append(MarkdownTodo(config))

		if "Muspy" in config:
			modules.append(Muspy(config))

		if "Downtime" in config:
			modules.append(Downtime(config))

		if "LastFmDisconnected" in config:
			modules.append(LastFmDisconnected(config))

		if "SociaalWerker" in config:
			modules.append(SociaalWerker(config))

		if "LastFmRecommendation" in config:
			modules.append(LastFmRecommendation(config))

		
		#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
		text = ""
		has_text = False

		# Modules uitvoeren
		for module in modules:
			if (module.HasText()):
				text += module.GetText() + "<br/><br/>";
				has_text = True

		# Onnodige enters aan het eind verwijderen
		text = text.replace("<br />", "<br/>")
		while text[-5:] == "<br/>":
			text = text[:-5]

		print(f.html2plain(text))

		if "Email" in config and has_text:
			email = Email(config)
			email.Send(text)

		if "Pushbullet" in config and has_text:
			pb = PushBullet(config)
			pb.Send(text)

# -*- coding: utf-8 -*-
import os, datetime, json, locale
import sys

from Config import Config
from Email import Email

from modules import *

# Cachedir voor vandaag maken indien nodig.
datadir = "data/{0}/".format(datetime.datetime.today().strftime('%Y%m%d'))
if not os.path.isdir(datadir):
	os.makedirs(datadir)


# Config inlezen
config = Config("niek").GetConfig()

if 'Locale' in config:
	locale.setlocale(locale.LC_TIME, '{0}.UTF-8'.format(config["Locale"]))

# Config extenden met runtime variabelen
with open('secrets/secrets.json') as secrets:    
	config['Runtime'] = { "datadir": datadir, "secrets": json.load(secrets) }

# Modules toevoegen
modules = []

if "Afval" in config:
	modules.append(Afval(config))

if "Downtime" in config:
	modules.append(Downtime(config))

if "Weer" in config:
	modules.append(Weer(config))

if "Agenda" in config:
	modules.append(Agenda(config))


#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
text = "# Goedemorgen\n"

# Modules uitvoeren
for module in modules:
	if (module.HasText()):
		text += module.GetText() + "\n\n";

print(text)

if "Email" in config:
	email = Email(config)

	email.Send(text)

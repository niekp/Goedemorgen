# -*- coding: utf-8 -*-
from Config import Config
from Email import Email

from modules import *

text = "# Goedemorgen\n"

# Config inlezen
config = Config("niek").GetConfig()

# Modules toevoegen
modules = []

if "Afval" in config:
	modules.append(Afval(config["Afval"]))

if "Downtime" in config:
	modules.append(Downtime(config["Downtime"]))

if "Weer" in config:
	modules.append(Weer(config["Weer"]))


# Modules uitvoeren
for module in modules:
	if (module.HasText()):
		text += module.GetText() + "\n\n";

print(text)

if "Email" in config:
	email = Email(config["Email"])

	email.Send(text)

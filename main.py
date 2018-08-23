from Config import Config
from modules import Afval
from modules import Downtime

print "# Goedemorgen"

# Config inlezen
config = Config("niek").GetConfig()

# Modules toevoegen
modules = []

if "Afval" in config:
	modules.append(Afval(config["Afval"]))

if "Downtime" in config:
	modules.append(Downtime(config["Downtime"]))

# Modules uitvoeren
for module in modules:
	if (module.HasText()):
		print module.GetText();

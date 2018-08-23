from Config import Config
from modules import Afval
from modules import DowntimePi

print "# Goedemorgen"


# Config inlezen
config = Config("niek").GetConfig()



# Modules toevoegen
modules = []

if "Afval" in config:
	modules.append(Afval(config["Afval"]))

if "DowntimePi" in config:
	modules.append(DowntimePi(config["DowntimePi"]))

# Modules uitvoeren
for module in modules:
	if (module.HasText()):
		print module.GetText();

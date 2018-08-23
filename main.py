#from modules import Module
from modules import Afval
from modules import DowntimePi

print "# Goedemorgen"

modules = []

modules.append(Afval())
modules.append(DowntimePi())

for module in modules:
	if (module.HasText()):
		print module.GetText();

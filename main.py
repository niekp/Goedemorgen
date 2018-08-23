#from modules import Module
from modules import Afval

print "# Goedemorgen"

modules = []

modules.append(Afval())

for module in modules:
	if (module.HasText()):
		print module.GetText();

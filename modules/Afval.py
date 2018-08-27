import datetime, json
from lib import Functions as f
from modules import _Module

class Afval(_Module):

	def __init__(self, config_full):
		self.hasText = False
		self.text = "";

		config = config_full["Afval"]

		now = f.Now(config_full)

		# Na 11u is het toch al te laat
		if now.hour < 11:
			# Dag van vandaag
			weekday = now.weekday()

			# Staat vandaag in de config file?
			if str(weekday) in config:
				self.hasText = True
				self.text = "Vandaag moet het " + config[str(weekday)] + " bij de weg"

	def HasText(self):
		return super(Afval, self).HasText()

	def GetText(self):
		return super(Afval, self).GetText()

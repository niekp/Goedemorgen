import datetime, json
from lib import Functions as f
from modules import _Module

class Afval(_Module):

	def Run(self):
		now = f.Now(self.config_full)

		# Na 11u is het toch al te laat
		if now.hour < 11:
			# Dag van vandaag
			weekday = now.weekday()

			# Staat vandaag in de config file?
			if str(weekday) in self.config:
				self.hasText = True
				self.text = "Vandaag moet het " + self.config[str(weekday)] + " bij de weg"

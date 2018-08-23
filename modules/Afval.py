import datetime, json
from modules import Module

class Afval(Module):

	def __init__(self, config):
		self.hasText = False
		self.text = "";

		# Dag van vandaag
		weekday = datetime.datetime.today().weekday()

		# Staat vandaag in de config file?
		if str(weekday) in config:
			self.hasText = True
			self.text = "Vandaag moet het " + config[str(weekday)] + " bij de weg"

	def HasText(self):
		return super(Afval, self).HasText()

	def GetText(self):
		return super(Afval, self).GetText()

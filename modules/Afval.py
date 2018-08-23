import datetime
from modules import Module

class Afval(Module):

	def __init__(self):
		self.hasText = False
		self.text = "";

		weekday = datetime.datetime.today().weekday()

		if (weekday == 1):
			self.text = "plastic"
		elif (weekday == 3):
			self.text = "papier"

		if (self.text != ""):
			self.hasText = True
			self.text = "Vandaag moet het " + self.text + " bij de weg"


	def HasText(self):
		return super(Afval, self).HasText()

	def GetText(self):
		return super(Afval, self).GetText()

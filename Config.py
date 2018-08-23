import json

class Config:
	# Config uitlezen aan de hand van gebruikersnaam. Later eventueel username_HASH(password + salt) doen. En niet in de public root zetten.
	def __init__(self, name):
		with open('config/' + name + '.json') as data_file:    
			self.config = json.load(data_file)

	def GetConfig(self):
		return self.config



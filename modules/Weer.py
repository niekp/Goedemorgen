# -*- coding: utf-8 -*-
import datetime, json
from modules import _Module
import urllib, json, time

class Weer(_Module):

	def __init__(self, config):
		self.hasText = True
		self.text = "";

		# Een textfile met de API-key. Met name om de key uit git te houden, en niet te hardcoden.
		apikey = open("secrets/darksky_apikey.txt", "r").read()

		# Bouw de URL voor de API-call op
		url = "https://api.darksky.net/forecast/" + apikey + "/" + str(config["lang"]) + "," + str(config["long"]) + "?units=si"

		response = urllib.urlopen(url);

		# Zet de response om in een JSON object.
		weather = json.loads(response.read());

		# Tekst opbouwen
		self.text = u"Het is nu {0}° en het wordt vandaag tussen de {1}° en {2}°".format(
			weather["currently"]["temperature"], 
			weather["daily"]["data"][0]["temperatureLow"], 
			weather["daily"]["data"][0]["temperatureHigh"])

	def HasText(self):
		return super(Weer, self).HasText()

	def GetText(self):
		return super(Weer, self).GetText()

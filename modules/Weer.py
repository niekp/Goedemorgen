# -*- coding: utf-8 -*-
import datetime, json
import urllib.request

from modules import _Module

class Weer(_Module):

	def __init__(self, config):
		self.hasText = True
		self.text = "";

		# Een textfile met de API-key. Met name om de key uit git te houden, en niet te hardcoden.
		apikey = open("secrets/darksky_apikey.txt", "r").read()

		# Bouw de URL voor de API-call op en maak een weer object

		with urllib.request.urlopen("https://api.darksky.net/forecast/{0}/{1},{2}?units=si".format(apikey, str(config["lang"]), str(config["long"]))) as url:
			weather = json.loads(url.read())

		# Tekst opbouwen
		self.text = u"Het is nu {0}° en het wordt vandaag tussen de {1}° en {2}°".format(
			weather["currently"]["temperature"], 
			weather["daily"]["data"][0]["temperatureLow"], 
			weather["daily"]["data"][0]["temperatureHigh"])

	def HasText(self):
		return super(Weer, self).HasText()

	def GetText(self):
		return super(Weer, self).GetText()

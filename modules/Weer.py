# -*- coding: utf-8 -*-
import datetime, json
import urllib.request
import os.path
from lib import Functions as f

from modules import _Module

class Weer(_Module):

	def __init__(self, config_full):
		self.hasText = True
		self.text = "";
		config = config_full["Weer"]

		# Een textfile met de API-key. Met name om de key uit git te houden, en niet te hardcoden.
		apikey = config_full["Runtime"]["secrets"]["darksky_apikey"]

		temperatureKey = "temperature"
		if 'gevoel' in config:
			if config["gevoel"]:
				temperatureKey = "apparentTemperature"

		# Cache de API verzoeken in een map per dag.
		filename = "{0}/Weer{1}_{2}.json".format(config_full["Runtime"]["datadir"], str(config["lang"]), str(config["long"]))

		now = f.Now(config_full)

		if os.path.exists(filename) and not config_full["Runtime"]["production"]: # Alleen cachen op test verzoeken, ik blijf toch wel onder de max api calls
			data = open(filename).read()

		else:
			# Bouw de URL voor de API-call op en maak een weer object
			with urllib.request.urlopen("https://api.darksky.net/forecast/{0}/{1},{2}?units=si".format(apikey, str(config["lang"]), str(config["long"]))) as url:
				data = url.read()
			
			with open(filename, 'w') as outfile:
				json.dump(json.loads(data), outfile)
			

		weather = json.loads(data)

		# Weerbericht opbouwen op basis van voorkeurs tijden.
		if "tijden" in config:
			text_builder = u"Het is nu {0}°<br/>".format(weather["currently"][temperatureKey]);

			weekday = now.weekday()

			# Wil je vandaag een voorspelling?
			if str(weekday) in config["tijden"]:
				# Voor elk uur de voorspelling opzoeken
				for data in weather["hourly"]["data"]:
					hour = datetime.datetime.utcfromtimestamp(data["time"]).hour
					day = datetime.datetime.utcfromtimestamp(data["time"]).day

					# Alleen de voorspelling van vandaag gebruiken
					if day == now.day:

						# Staat het uur in de gewenste tijden, en na het huidige uur?
						if hour in config["tijden"][str(weekday)] and hour >= now.hour:
							# Text opbouwen per tijd.
							text_builder += "Om {0} uur is het {1}°".format(hour, data[temperatureKey])
							if (data["precipProbability"] >= 0.1):
								perciptype = "regen"
								if data["precipType"] == "snow":
									perciptype = "sneeuw"

								text_builder += " met {0}% kans op {1}".format(round(data["precipProbability"]*100), perciptype)

							text_builder += "<br/>"

				self.text = text_builder

			else:
				self.hasText = False

		else:
			# Standaard tekst
			self.text = u"Het is nu {0}° en het wordt vandaag tussen de {1}° en {2}°".format(
				weather["currently"][temperatureKey], 
				weather["daily"]["data"][0]["temperatureLow"], 
				weather["daily"]["data"][0]["temperatureHigh"])

	def HasText(self):
		return super(Weer, self).HasText()

	def GetText(self):
		return super(Weer, self).GetText()

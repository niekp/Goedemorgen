# -*- coding: utf-8 -*-
import datetime, json
import urllib.request
import os.path
from lib import Functions as f

from modules import _Module

class Weer(_Module):

	def Run(self):
		# Een textfile met de API-key. Met name om de key uit git te houden, en niet te hardcoden.
		apikey = self.config_full["Runtime"]["secrets"]["darksky_apikey"]

		temperatureKey = "temperature"
		if 'gevoel' in self.config:
			if self.config["gevoel"]:
				temperatureKey = "apparentTemperature"

		# Cache de API verzoeken in een map per dag.
		filename = "{0}/Weer{1}_{2}.json".format(self.config_full["Runtime"]["datadir"], str(self.config["lang"]), str(self.config["long"]))

		now = f.Now(self.config_full)

		if os.path.exists(filename) and not self.config_full["Runtime"]["production"]: # Alleen cachen op test verzoeken, ik blijf toch wel onder de max api calls
			data = open(filename).read()

		else:
			# Bouw de URL voor de API-call op en maak een weer object
			with urllib.request.urlopen("https://api.darksky.net/forecast/{0}/{1},{2}?units=si".format(apikey, str(self.config["lang"]), str(self.config["long"]))) as url:
				data = url.read()
			
			with open(filename, 'w') as outfile:
				json.dump(json.loads(data), outfile)
			

		weather = json.loads(data)

		# Weerbericht opbouwen op basis van voorkeurs tijden.
		if "tijden" in self.config:
			text_builder = ""

			weekday = now.weekday()

			# Wil je vandaag een voorspelling?
			if str(weekday) in self.config["tijden"]:

				# Stats voor het advies
				minTemp = 99
				maxTemp = -99
				maxRegen = 0

				# Voor elk uur de voorspelling opzoeken
				for data in weather["hourly"]["data"]:
					hour = datetime.datetime.utcfromtimestamp(data["time"]).hour
					day = datetime.datetime.utcfromtimestamp(data["time"]).day

					# Alleen de voorspelling van vandaag gebruiken
					if day == now.day:
						# Staat het uur in de gewenste tijden, en na het huidige uur?
						if hour in self.config["tijden"][str(weekday)] and hour >= now.hour:
							# Text opbouwen per tijd.
							text_builder += "Om {0} uur is het {1}°".format(hour, data[temperatureKey])
							if (data["precipProbability"] >= 0.1):
								perciptype = "regen"
								if data["precipType"] == "snow":
									perciptype = "sneeuw"

								text_builder += " met {0}% kans op {1}".format(round(data["precipProbability"]*100), perciptype)

							if data[temperatureKey] < minTemp:
								minTemp = data[temperatureKey]
							if data[temperatureKey] > maxTemp:
								maxTemp = data[temperatureKey]

							if (data["precipProbability"] * 100) > maxRegen:
								maxRegen = (data["precipProbability"] * 100)

							text_builder += "<br/>"

				if text_builder != "":
					# Advies opbouwen
					advies = ""
					if "advies" in self.config:
						for key in self.config["advies"]:
							if minTemp >= self.config["advies"][key]["min"] and maxTemp <= self.config["advies"][key]["max"] and maxRegen <= self.config["advies"][key]["regen"]:
								advies = self.config["advies"][key]["advies"]
								break


					# Het instellen van advies op basis van parameters is een onmogelijke taak.
					# Dus of heel veel in de config tweaken en super kleine advies sets maken, of nog iets in code verzinnen.
					# We gaan het meemaken.. ok doei.
					if advies != "":
						text_builder += "Advies: " + advies
				
					self.text = text_builder

				else:
					self.hasText = False

			else:
				self.hasText = False

		else:
			# Standaard tekst
			self.text = u"Het is nu {0}° en het wordt vandaag tussen de {1}° en {2}°".format(
				weather["currently"][temperatureKey], 
				weather["daily"]["data"][0]["temperatureLow"], 
				weather["daily"]["data"][0]["temperatureHigh"])


import datetime
import os.path
import urllib, json, time
from lib import Functions as f
from modules import _Module

class SociaalWerker(_Module):

	def Run(self):
		self.datafile = "{0}/sociaalwerker.json".format(self.config_full["Runtime"]["userdir"])

		# Werk data bij
		self.Update()

		with open(self.datafile) as data_file:
			feitjes = json.load(data_file)

		# Check de personen tegen de config
		for persoon in self.config["personen"]:
			if persoon in feitjes:
				last_message = int(feitjes[persoon])
			else:
				last_message = 0

			# Parse de voorkeur naar een timestamp
			notify_diff = 0
			if self.config["personen"][persoon].find("d") >= 0:
				notify_diff = int(self.config["personen"][persoon].replace("d", ""))
				notify_diff = notify_diff * 60 * 60 * 24
			if self.config["personen"][persoon].find("h") >= 0:
				notify_diff = int(self.config["personen"][persoon].replace("h", ""))
				notify_diff = notify_diff * 60 * 60

			# Bereken het verschil sinds het laatste bericht
			last_message_diff = time.time() - last_message

			# Notify indien nodig
			if last_message_diff > notify_diff:
				self.hasText = True
				self.text += "Al {0} dagen geen contact gehad met {1}\n".format(round(last_message_diff / 60 / 60 / 24, 2), persoon)

		# In productie, verwijder de rauwe notificatie gegevens.
		if self.config_full["Runtime"]["production"]:
			if "clearURL" in self.config:
				with urllib.request.urlopen(self.config["clearURL"]) as url:
					data = url.read()


		
	def Update(self):
		# Maak een nieuwe data file als die nog niet bestaat
		if not os.path.exists(self.datafile):
			with open(self.datafile, 'w') as outfile:  
				json.dump({}, outfile)

		# Open de data file
		with open(self.datafile) as data_file:
			feitjes = json.load(data_file)
		
		# Laad alle notificaties in
		with urllib.request.urlopen(self.config["notificationsURL"]) as url:
			data = url.read()

		notifications = json.loads(data)

		for notification in notifications:
			# Parse alleen whatsapp notificaties
			if notifications[notification]["AppName"] == "WhatsApp" or notifications[notification]["AppName"] == "Signal" or notifications[notification]["AppName"] == "Riot.im":
				name = notifications[notification]["NotificationTitle"]

				if notifications[notification]["AppName"] == "Riot.im":
					name = name.replace(' (WA)', '') # TODO: regex voor `.(..)`

				# Staat de persoon al in de data?
				if name in feitjes:
					# Is de notificatie recenter dan de laatst bekende?
					if int(notification) > int(feitjes[name]):
						# Bijwerken
						feitjes[name] = notification
				else:
					# Notificatie van een onbekende direct toevoegen
					feitjes[notifications[notification]["NotificationTitle"]] = notification

		# Schrijf de datafile weg
		with open(self.datafile, 'w') as outfile:  
			json.dump(feitjes, outfile)

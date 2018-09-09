import datetime
import os.path
import urllib, json, time
from lib import Functions as f
from modules import _Module

class SociaalWerker(_Module):

	def __init__(self, config_full):
		self.hasText = False
		self.text = "";

		self.config = config_full["SociaalWerker"]
		self.datafile = "{0}/sociaalwerker.json".format(config_full["Runtime"]["userdir"])


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
			if notifications[notification]["AppName"] == "WhatsApp":

				# Staat de persoon al in de data?
				if notifications[notification]["NotificationTitle"] in feitjes:
					# Is de notificatie recenter dan de laatst bekende?
					if int(notification) > int(feitjes[notifications[notification]["NotificationTitle"]]):
						# Bijwerken
						feitjes[notifications[notification]["NotificationTitle"]] = notification
						print("Tijd van " + notifications[notification]["NotificationTitle"] + " geupdate")
				else:
					# Notificatie van een onbekende direct toevoegen
					feitjes[notifications[notification]["NotificationTitle"]] = notification
					print("Tijd van " + notifications[notification]["NotificationTitle"] + " toegevoegd")

		# Schrijf de datafile weg
		with open(self.datafile, 'w') as outfile:  
			json.dump(feitjes, outfile)

	def HasText(self):
		return super(SociaalWerker, self).HasText()

	def GetText(self):
		return super(SociaalWerker, self).GetText()

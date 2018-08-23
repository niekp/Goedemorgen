from modules import Module
import urllib, json, time

class Downtime(Module):
	def __init__(self, config):
		self.hasText = False
		self.text = "";

		# Op deze URL verwacht het script een JSON file met minimaal: { "server": { "ping": timestamp } }
		response = urllib.urlopen(config["url"]);
		ping = json.loads(response.read());

		# Pak de laatste ping
		lastPing = ping[config["server"]]["ping"]

		# Vergelijk deze met de timestamp van nu
		now = round(time.time())
		diff = now - lastPing;
		diffHour = (diff / 60 / 60)

		# Is dit langer dan [uur] geleden, signaleren
		if (diffHour >= int(config["uur"])):
			self.hasText = True
			self.text = "De backup raspberry pi is al " + str(round(diffHour, 2)) + " uur offline."


	def HasText(self):
		return super(Downtime, self).HasText()

	def GetText(self):
		return super(Downtime, self).GetText()

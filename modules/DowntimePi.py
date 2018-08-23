from modules import Module
import urllib, json, time

class DowntimePi(Module):
	def __init__(self):
		self.hasText = False
		self.text = "";

		response = urllib.urlopen("https://niekpijp.nl/pingserver/ping.json");
		ping = json.loads(response.read());

		lastPing = ping["backup_pi"]["ping"]
		now = round(time.time())

		diff = now - lastPing;
		diffHour = (diff / 60 / 60)

		if (diffHour >= 3):
			self.hasText = True
			self.text = "De backup raspberry pi is al " + str(round(diffHour, 2)) + " uur offline."


	def HasText(self):
		return super(DowntimePi, self).HasText()

	def GetText(self):
		return super(DowntimePi, self).GetText()

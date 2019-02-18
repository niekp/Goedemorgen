import datetime, json, urllib
from lib import Functions as f
from modules import _Module

class Downtime(_Module):

	def __init__(self, config_full):
		self.hasText = False
		self.text = "";

		config = config_full["Downtime"]

		now = f.Now(config_full)

		with urllib.request.urlopen(config["url"]) as url:
			data = url.read()

		servers = json.loads(data)

		for server in servers:
			if not server in config["servers"]:
				continue

			ping = f.GetDateTimeWithTZ(config_full, (datetime.datetime.fromtimestamp(servers[server]["ping"])))
			diffhour = ((now - ping).total_seconds() / 60 / 60);

			if (diffhour > int(config["servers"][server])):
				self.text = server + " is al " + str(round(diffhour, 2)) + " uur stil.";
				self.hasText = True

	def HasText(self):
		return super(Downtime, self).HasText()

	def GetText(self):
		return super(Downtime, self).GetText()

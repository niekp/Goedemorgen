import datetime, json, urllib
from lib import Functions as f
from modules import _Module

class Downtime(_Module):

	def Run(self):
		now = f.Now(self.config_full)

		with urllib.request.urlopen(self.config["url"]) as url:
			data = url.read()

		servers = json.loads(data)

		for server in servers:
			if not server in self.config["servers"]:
				continue

			ping = f.GetDateTimeWithTZ(self.config_full, (datetime.datetime.fromtimestamp(int(servers[server]["ping"]))))
			diffhour = ((now - ping).total_seconds() / 60 / 60);

			if (diffhour > int(self.config["servers"][server])):
				self.text = server + " is al " + str(round(diffhour, 2)) + " uur stil.";
				self.hasText = True

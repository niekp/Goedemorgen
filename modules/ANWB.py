import datetime, json
import urllib
from lib import Functions as f
from modules import _Module

class ANWB(_Module):

	def Run(self):
		with urllib.request.urlopen("https://www.anwb.nl/feeds/gethf") as url:
			data = json.loads(url.read())

		for entry in data["roadEntries"]:
			if entry["road"] in self.config['roads']:

				for eventType in entry["events"]:
					for event in entry["events"][eventType]:
						if self.hasText:
							self.text += "<br />"

						self.text += "<h3>Verkeersinformatie " + entry["road"] + "</h3>"
						self.text += "{0} - {1}: {2}<br />{3}<br />".format(event["from"], event["to"], event["reason"], event["description"])

						if "events" in event:
							for subevent in event["events"]:
								self.text += "* " + subevent["text"] + "<br />"
								
						self.hasText = True

import pytz, datetime

class Functions:
	
	def html2plain(text):
		text = text.replace("<br />", "\n")
		text = text.replace("<br/>", "\n")
		text = text.replace("<h1>", "*")
		text = text.replace("</h1>", "*\n")
		text = text.replace("<h2>", "_")
		text = text.replace("</h2>", "_\n")
		text = text.replace("<h3>", "_")
		text = text.replace("</h3>", "_\n")
		return text


	def GetTZ(config):
		if 'TZ' in config:
			tz = pytz.timezone(config["TZ"])
		else:
			tz = pytz.timezone("Europe/Amsterdam")

		return tz

	def Now(config):
		return Functions.GetTZ(config).localize(datetime.datetime.now())
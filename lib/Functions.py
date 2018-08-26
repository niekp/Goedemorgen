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
		text = text.replace("<input type='checkbox' />", "[ ]")
		text = text.replace("<input type='checkbox' checked='checked' />", "[x]")
		return text

	def plain2hml(text):
		text = text.replace("\n", "<br/>")
		text = text.replace("- [ ]", "<input type='checkbox' />")
		text = text.replace("- [x]", "<input type='checkbox' checked='checked' />")
		return text


	def GetTZ(config):
		if 'TZ' in config:
			tz = pytz.timezone(config["TZ"])
		else:
			tz = pytz.timezone("Europe/Amsterdam")

		return tz

	def Now(config):
		return datetime.datetime.now().astimezone(Functions.GetTZ(config))

	def Goede(config):
		now = Functions.Now(config)
		goede = ""
		if now.hour >= 19:
			return "Goedenavond"
		elif now.hour >= 12:
			return "Goedemiddag"
		else:
			return "Goedemorgen"


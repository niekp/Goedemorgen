import pytz, datetime, os, sqlite3

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


	def GetTZ(config_full):
		if 'TZ' in config_full:
			tz = pytz.timezone(config_full["TZ"])
		else:
			tz = pytz.timezone("Europe/Amsterdam")

		return tz

	def Now(config_full):
		return datetime.datetime.now().astimezone(Functions.GetTZ(config_full))

	def GetDateTimeWithTZ(config_full, dt):
		return dt.astimezone(Functions.GetTZ(config_full))

	def Goede(config_full):
		now = Functions.Now(config_full)
		goede = ""
		if now.hour >= 19:
			return "Goedenavond"
		elif now.hour >= 12:
			return "Goedemiddag"
		else:
			return "Goedemorgen"


	def getDatabase(config_full, database_name, create_query):
		# Load a database to keep the status
		filename = "{0}/{1}.db".format(config_full["Runtime"]["userdir"], database_name)

		if not os.path.exists(filename):
			conn = sqlite3.connect(filename)
			c = conn.cursor()
			# Bij de eerste connect een table maken
			c.execute(create_query)

			conn.commit()

			return conn
		else:
			return sqlite3.connect(filename)

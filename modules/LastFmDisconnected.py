import urllib, json, time
from modules import _Module

class LastFmDisconnected(_Module):

	def Run(self):
		apikey = self.config_full["Runtime"]["secrets"]["lastfm_apikey"]

		user = self.config["username"]

		hours = 0
		try:
			hours = int(self.config["hours"])
		except Exception as e:
			pass

		# Instelling staat aan
		if hours > 0:
			# Recente tracks ophalen
			with urllib.request.urlopen("https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={0}&api_key={1}&format=json".format(user, apikey)) as url:
				data = url.read()

			scrobbles = json.loads(data)

			now = round(time.time())
			lastscrobble = 0;

			# Recentste scrobble ophalen
			for track in scrobbles["recenttracks"]["track"]:
				dateuts = 0;
				try:
					dateuts = int(track["date"]["uts"]);
				except Exception as e:
					pass
				if dateuts > 0:
					lastscrobble = dateuts;
					# Stop na 1 track
					break;

			# Tijd sinds de laatste scrobble?
			diff = now - lastscrobble;
			diffhour =  (diff / 60 / 60);

			# Geen scrobbles in de afgelopen x uur?
			if (diffhour > hours):
				self.text = user + " heeft al " + str(round(diffhour, 2)) + " uur geen scrobbles.";
				self.hasText = True

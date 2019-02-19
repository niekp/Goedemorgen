import urllib, json, time
from modules import _Module
from random import randint

class LastFmRecommendation(_Module):

	config_full = None

	def __init__(self, config_full):
		self.config_full = config_full

		# If there isn't a preset 'top' then generate it
		if "top" not in config_full["LastFmRecommendation"]:
			# Load the first page to get the pagecount
			totalPages = int(self.GetArtist(1)['@attr']['totalPages'])
			# Get a random artist from the first 25% of top artists.
			pageSet = int(totalPages / 4)

		else:
			pageSet = int(config_full["LastFmRecommendation"]["top"])

		# Generate a random number in the pageset (preset or generated)
		random = randint(1, pageSet)

		# Get the random artist info
		artist = self.GetArtist(random)['artist'][0]

		self.text = artist['name'] + ' (' + artist['playcount'] + ' scrobbles)'
		self.hasText = True

	def GetArtist(self, offset):
		apikey = self.config_full["Runtime"]["secrets"]["lastfm_apikey"]
		user = self.config_full["LastFmRecommendation"]["username"]

		if "period" in self.config_full["LastFmRecommendation"]:
			period = self.config_full["LastFmRecommendation"]["period"]
		else:
			period = "overall"

		# Limit 1 to only get 1 artist
		with urllib.request.urlopen("https://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={0}&api_key={1}&limit=1&period={2}&page={3}&format=json".format(user, apikey, period, offset)) as url:
			data = json.loads(url.read())

		return data['topartists']

	def HasText(self):
		return super(LastFmRecommendation, self).HasText()

	def GetText(self):
		return super(LastFmRecommendation, self).GetText()
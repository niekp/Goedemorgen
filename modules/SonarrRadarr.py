import json
import urllib
from modules import _Module

class SonarrRadarr(_Module):

	def Run(self):
		# Grab 2 pages from sonarr since there is a lot more activity. This should be dynamic but ohwell it works.
		urls = 	[
					"{0}/history?apikey={1}&sortKey=date&sortDir=desc&pageSize=20&page=1".format(self.config["sonarr"]["url"], self.config["sonarr"]["apikey"]),
					"{0}/history?apikey={1}&sortKey=date&sortDir=desc&pageSize=20&page=2".format(self.config["sonarr"]["url"], self.config["sonarr"]["apikey"]),
					"{0}/history?apikey={1}&sortKey=date&sortDir=desc&pageSize=20&page=1".format(self.config["radarr"]["url"], self.config["radarr"]["apikey"])
				]

		# Setup DB to keep the notified history
		self.conn = f.getDatabase(self.config_full, "sonarrradarr", "CREATE TABLE Records (id text, title text)")
		cursor = self.conn.cursor()

		# Download each api result
		for url in urls:
			with urllib.request.urlopen(url) as url:
				data = json.loads(url.read())
				records = data["records"]

				for record in records:
					# Only use the 'import' event so you only get notified if the download was successfull
					if record["eventType"] != "downloadFolderImported":
						continue

					# Generate the 'unique' and 'title' values for episodes or movies
					if "episode" in record:
						unique = "episode_{0}_{1}".format(record["seriesId"], record["episodeId"])
						serieTitle = record["series"]["title"]
						episodeTitle = record["episode"]["title"]
						episodeNumber = "S{:02}E{:02}".format(record["episode"]["seasonNumber"], record["episode"]["episodeNumber"])

						title = "{0}: {1} - {2}".format(episodeNumber, serieTitle, episodeTitle)

					elif "movie" in record:
						unique = "movie_{0}".format(record["movieId"])
						title = record["movie"]["title"]
					else:
						continue
						
					# Check if the episode/movie has already been notified
					cursor.execute("SELECT title FROM Records WHERE id = ?", (unique,))
					result = cursor.fetchone()
					
					# If not, notify.
					if result is None:
						cursor.execute("insert into Records values (?, ?)", (unique, title))

						self.text += ("{0}<br />".format(title))
						self.hasText = True

		cursor.close()

		# Save the history to sqlite
		self.conn.commit()

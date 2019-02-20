from lib import Functions as f
from modules import _Module
from lxml import etree
import requests

class Subsonic(_Module):

	def Run(self):
		# Generate the API URL
		api_url = "{0}/rest/getNewestPodcasts?u={1}&p={2}&v=1.12.0&c=goedemorgen".format(self.config["url"], self.config["user"], self.config["password"])
		
		# Download the API response
		response = requests.get(api_url, stream=True)
		response.raw.decode_content = True

		# Parse the API response
		parser = etree.XMLParser(ns_clean=True, recover=True)
		tree = etree.parse(response.raw, parser)
		root = tree.getroot()

		# Load up the database
		self.conn = f.getDatabase(self.config_full, "subsonic", "CREATE TABLE Subsonic (id text, podcast text, title text)")

		for elem in tree.iter():
			# Filter out the episodes from the result
			if elem.tag.endswith("episode"):
				id = elem.attrib['id']
				podcast = elem.attrib['album']
				title = elem.attrib['title']

				cursor = self.conn.cursor()

				# Check if the episode has already been notified
				cursor.execute("SELECT title FROM Subsonic WHERE id = ?", (id,))
				result = cursor.fetchone()
				
				# If not, notify.
				if result is None:
					cursor.execute("insert into Subsonic values (?, ?, ?)", (id, podcast, title))
					self.text += ("{0} - {1}<br />".format(podcast, title))
					self.hasText = True

				cursor.close()
		
		self.conn.commit()

		if self.hasText:
			self.text = "<h3>Nieuwe podcasts</h3>" + self.text
			
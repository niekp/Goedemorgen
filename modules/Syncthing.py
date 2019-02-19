import datetime, json
from modules import _Module
from syncthing import Syncthing as SyncthingWrapper
import os
import sqlite3

class Syncthing(_Module):

	def __init__(self, config_full):
		self.hasText = False
		self.text = ""

		config = config_full["Syncthing"]

		# Load the syncthing API
		s = SyncthingWrapper(config["apikey"], config["host"], str(config["port"]))

		# Load a database to keep the status
		filename = "{0}/syncthing.db".format(config_full["Runtime"]["userdir"])

		if not os.path.exists(filename):
			self.conn = sqlite3.connect(filename)
			c = self.conn.cursor()

			# Bij de eerste connect een table maken
			c.execute("CREATE TABLE Syncthing (folder text, file text, modified_date text)")

		else:
			self.conn = sqlite3.connect(filename)
			c = self.conn.cursor()

		folders_metadata = s.system.config()["folders"]
		
		for folder_id in config["folders"]:
			# Default label als de folder label niet gevonden kan worden
			label = "Nieuwe bestanden"

			# Find the label
			for metadata in folders_metadata:
				if metadata["id"] == folder_id:
					label = metadata["label"]
			
			# Load all filenames with API
			for file, metadata in s.database.browse(folder_id).items():
				modified_date = metadata[0]

				cursor = self.conn.cursor()

				# Check if the notification for this file has already been sent
				cursor.execute("SELECT file FROM Syncthing WHERE folder = ? AND file = ?", (folder_id, file,))
				result = cursor.fetchone()

				# If not, send the notification and keep history
				if result is None:
					cursor.execute("INSERT INTO Syncthing values (?, ?, ?)", (folder_id, file, modified_date))
					
					if label:
						self.text += "<h3>" + label + "</h3>"
						label = ""

					self.text += (file + "<br />")
					self.hasText = True

				cursor.close()

		# Opslaan
		self.conn.commit()

	def HasText(self):
		return super(Syncthing, self).HasText()

	def GetText(self):
		return super(Syncthing, self).GetText()

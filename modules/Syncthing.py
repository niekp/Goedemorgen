import datetime
import json
from modules import _Module
from syncthing import Syncthing as SyncthingWrapper
from lib import Functions as f
import os
import sqlite3


class Syncthing(_Module):

    def Run(self):
        # Load the syncthing API
        s = SyncthingWrapper(
            self.config["apikey"], self.config["host"], str(self.config["port"]))

        # Load a database to keep the status
        conn = f.getDatabase(self.config_full, "syncthing",
                             "CREATE TABLE Syncthing (folder text, file text, modified_date text)")
        cursor = conn.cursor()

        folders_metadata = s.system.config()["folders"]

        for folder_id in self.config["folders"]:
            # Default label als de folder label niet gevonden kan worden
            label = "Nieuwe bestanden"

            # Find the label
            for metadata in folders_metadata:
                if metadata["id"] == folder_id:
                    label = metadata["label"]

            # Load all filenames with API
            for file, metadata in s.database.browse(folder_id).items():
                modified_date = metadata[0]

                # Check if the notification for this file has already been sent
                cursor.execute(
                    "SELECT file FROM Syncthing WHERE folder = ? AND file = ?", (folder_id, file,))
                result = cursor.fetchone()

                # If not, send the notification and keep history
                if result is None:
                    cursor.execute(
                        "INSERT INTO Syncthing values (?, ?, ?)", (folder_id, file, modified_date))

                    if label:
                        self.text += "<h3>" + label + "</h3>"
                        label = ""

                    self.text += (file + "<br />")
                    self.hasText = True

        cursor.close()

        # Opslaan
        conn.commit()

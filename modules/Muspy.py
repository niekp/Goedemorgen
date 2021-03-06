import datetime
import json
from lib import Functions as f
import sqlite3
import os.path
import feedparser
from dateutil.parser import parse
from modules import _Module


class Muspy(_Module):

    def Run(self):
        # Load the database
        self.conn = f.getDatabase(
            self.config_full, "muspy", "CREATE TABLE Muspy (id text, title text, updated text, notified int)")
        cursor = self.conn.cursor()

        # Haal de feed op
        feed = feedparser.parse(self.config["feed"])
        for item in feed["items"]:
            # Werk database bij
            self.UpdateDB(item["id"], item["title"], item["updated"])

        # Opslaan
        self.conn.commit()

        c_update = self.conn.cursor()
        # Zoek alle ongemelde releases voor vandaag, of het verleden. Sqlite heeft geen date functies, maar zo kan het ook
        results = cursor.execute("SELECT id, title, updated FROM Muspy WHERE substr(updated,0, 5) || substr(updated, 6, 2) || substr(updated, 9, 2) < ? and notified = 0;",
                                 (datetime.datetime.now().strftime("%Y%m%d"),))
        for release in results:
            self.hasText = True
            self.text += release[1] + "<br/>"

            # Opslaan dat de notificatie verstuurd is.
            c_update.execute(
                "UPDATE Muspy SET notified = 1 WHERE id = ?", (release[0],))

        # Header toevoegen
        if self.hasText:
            self.conn.commit()
            self.text = "<h2>Nieuwe releases</h2>" + self.text

        cursor.close()
        c_update.close()
        self.conn.close()

    def UpdateDB(self, id, title, updated):
        cursor = self.conn.cursor()

        # Die feed spoort niet helemaal, als hij vervelend blijft doen op title matchen en hopen dat dat beter gaat.
        # Oke met titel is niet veel beter, de DB heeft vast tijd nodig om op te bouwen. Met titel scheelt in elk geval dubbele records met een andere id.
        # 20190216: Leuke edgecase, Er staan 2 albums 'Weezer - Weezer' in de feed (teal and black) dus op titel switcht hij ze en notified hij elke dag. Toch maar weer op ID dus.
        cursor.execute(
            "SELECT title, updated, notified FROM Muspy WHERE id = ?", (id,))
        #cursor.execute("SELECT title, updated, notified FROM Muspy WHERE id = ? or title = ?", (id, title,))
        result = cursor.fetchone()

        # Is de release al bekend?
        if result is None:
            cursor.execute("insert into Muspy values (?, ?, ?, ?)",
                           (id, title, updated, 0))
        else:
            # Is de releasedatum gewijzigd?
            if updated != result[1] or title != result[0]:
                # Ligt de datum nog in de toekomst, of in het verleden maar is dit nog nooit gemeld?
                if parse(updated).date() >= datetime.date.today() or result[2] == 0:
                    cursor.execute(
                        "update Muspy SET updated = ?, title = ?, notified = ? where id = ? or title = ?", (updated, title, 0, id, title))

        cursor.close()

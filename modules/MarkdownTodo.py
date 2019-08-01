import datetime
import requests
from lib import Functions as f
from modules import _Module


class MarkdownTodo(_Module):

    def Run(self):
        now = f.Now(self.config_full)
        dag = now.strftime("%A").lower()

        # Url checken en eventueel fixen zodat ik folder+file kan doen
        if self.config["folder"][-1:] != "/":
            self.config["folder"] += "/"

        if "weekly" in self.config:
            if self.config["weekly"][:1] == "/":
                self.config["weekly"] = self.config["weekly"][1:]

            weekly_url = self.config["folder"] + self.config["weekly"]

            weekly_url = weekly_url.replace("[year]", "[jaar]")
            weekly_url = weekly_url.replace(
                "[week]", str(now.isocalendar()[1]))
            weekly_url = weekly_url.replace("[jaar]", str(now.year))

            response = requests.get(weekly_url)

            if response.status_code == 200:
                weekly = response.text

                # Zoek op ## Dag
                weeklyDagIndex = weekly.lower().find("## " + dag)
                # index = start van ## Dag t/m eof, GetBlock kapt hem op de volgende ## af
                weeklyDag = self.GetBlock(weekly[weeklyDagIndex:])

                # Filter alle uitgevoerde taken
                weeklyDag = self.FilterDone(weeklyDag)

                # Openstaande punten uit vorige dagen
                laatsteDag = ""
                firstDag = True
                histText = ""
                # DagIndex = index van vandaag, alles daarvoor is al geweest, dus scannen op gemist.
                for regel in weekly[:weeklyDagIndex].split("\n"):
                    if regel.find("## ") >= 0:  # Dag onthouden om in het bericht te zetten
                        laatsteDag = regel
                        firstDag = True
                    if regel.find("[ ]") >= 0:
                        if firstDag:
                            histText += laatsteDag + "\n"
                            firstDag = False

                        histText += regel + "\n"

                histText = histText.rstrip()

                # Openstaande punten in de algemene ## TODO
                # .find = start van ## todo t/m eof, GetBlock kapt hem op de volgende ## af
                weeklyTodo = self.GetBlock(
                    weekly[weekly.lower().find("## todo"):])

                # Todo tekst opbouwen, alleen openstaande vinkjes
                todoText = self.FilterDone(weeklyTodo)

                # *# Tekst opbouwen

                # Gemiste punten van deze week toevoegen
                if histText != "":
                    self.hasText = True
                    self.text += histText + "\n\n"

                # Alle punten van vandaag toevoegen, indien er minimaal 1 openstaande is.
                if weeklyDag.find("[ ]") > 0:
                    self.hasText = True
                    self.text += weeklyDag + "\n\n"

                # Open algemene TODO toevoegen
                if todoText.find("[ ]") > 0:
                    self.hasText = True
                    self.text += todoText + "\n\n"

            # Omzetten naar HTML gezien main dat verwacht.
            self.text = f.plain2hml(self.text).rstrip()

    def FilterDone(self, text):
        textOut = ""
        titleFound = False
        # Elke regel checken op een open taak, zo ja toevoegen
        for regel in text.split("\n"):
            if regel.find("[ ]") >= 0:
                textOut += regel + "\n"
            elif regel.find("-") < 0 and not titleFound:
                # De eerste regel zonder - is de titel
                textOut = regel + "\n" + textOut
                titleFound = True

        textOut = textOut.rstrip()
        return textOut

    def GetBlock(self, text):
        # Zoek op de ## of --- als eindtag, negeer de eerste 2 karakters, die zijn namelijk ##
        textIndex = text[2:].lower().find("##")
        textIndexTmp = text.lower().find("---")

        if textIndexTmp < textIndex and textIndexTmp > 0:
            textIndex = textIndexTmp

        if textIndex >= 0:
            text = text[:textIndex]

        return text


"""
Uitleg: Elke week maak ik een .md bestand als agenda/todo. Deze ziet er zo uit:

# Week 34 - 2018

[Note index](../../index.md)  

## Maandag 20
- [x] Dit wegbrengen
- [ ] Dat doen
- [x] Bellen met

## Dinsdag 21
- [x] 18:30 Afspraak met iemand
- [x] Sporten

## Woensdag 22
- [ ] Dit vervangen

...
...

## TODO
- [x] Iets teruggeven
- [ ] Afspraak maken met die

----------------------------------------------------

In "Weekly" ga ik opzoek naar vandaag, en gemiste punten van vorige dagen. Daarnaast heeft elke week een algemene TODO, openstaande punten hiervan ook meenemen
[ ] = lege checkbox en [x] is uitgevoerd.
"""

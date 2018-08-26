import datetime
import requests
from lib import Functions as f
from modules import _Module

class MarkdownTodo(_Module):

	def __init__(self, config_full):
		self.hasText = False
		self.text = "";

		config = config_full["MarkdownTodo"]
		now = f.Now(config_full)
		dag = now.strftime("%A").lower()

		# Url checken en eventueel fixen zodat ik folder+file kan doen
		if config["folder"][-1:] != "/":
			config["folder"] += "/"

		if "weekly" in config:
			if config["weekly"][:1] == "/":
				config["weekly"] = config["weekly"][1:]

			weekly_url = config["folder"] + config["weekly"]

			weekly_url = weekly_url.replace("[year]", "[jaar]")
			weekly_url = weekly_url.replace("[week]", str(now.isocalendar()[1]))
			weekly_url = weekly_url.replace("[jaar]", str(now.year))

			response = requests.get(weekly_url)

			if response.status_code == 200:
				weekly = response.text

				# Zoek op ## Dag, en dan alles daarvoor negeren
				weeklyDagIndex = weekly.lower().find("## " + dag)
				weeklyHist = weekly[:weeklyDagIndex]
				weeklyDag = weekly[weeklyDagIndex:]

				# Zoek op de ## of --- als eindtag, negeer de eerste 2 karakters, die zijn namelijk ##
				weeklyDagIndex = weeklyDag[2:].lower().find("##")
				weeklyDagIndexTmp = weeklyDag.lower().find("--")

				if weeklyDagIndexTmp < weeklyDagIndex and weeklyDagIndexTmp > 0:
					weeklyDagIndex = weeklyDagIndexTmp

				if weeklyDagIndex >= 0:
					weeklyDag = weeklyDag[:weeklyDagIndex]

				# Newlines van het einde verwijderen
				weeklyDag = weeklyDag.rstrip()

				# Openstaande punten uit vorige dagen
				laatsteDag = ""
				firstDag = True
				histText = ""
				for regel in weeklyHist.split("\n"):
					if regel.find("## ") >= 0: # Dag onthouden om in het bericht te zetten
						laatsteDag = regel
						firstDag = True
					if regel.find("[ ]") >= 0:
						if firstDag:
							histText += laatsteDag + "\n"
							firstDag = False

						histText += regel + "\n"

				histText = histText.rstrip()

				# Openstaande punten in de algemene ## TODO
				weeklyTodoIndex = weekly.lower().find("## todo")
				weeklyTodo = weekly[weeklyTodoIndex:]

				# Zoeken op een break, soms heb ik nog ## Notes onder ## TODO staan
				weeklyTodoIndex = weeklyTodo[2:].lower().find("##")
				weeklyTodoIndexTmp = weeklyTodo.lower().find("--")

				if weeklyTodoIndexTmp < weeklyTodoIndex and weeklyTodoIndexTmp > 0:
					weeklyTodoIndex = weeklyTodoIndexTmp

				if weeklyTodoIndex >= 0:
					weeklyTodo = weeklyTodo[:weeklyTodoIndex]

				# Todo tekst opbouwen, alleen openstaande vinkjes
				todoText = ""
				for regel in weeklyTodo.split("\n"):
					if regel.find("[ ]") >= 0:
						todoText += regel + "\n"


				#*# Tekst opbouwen

				# Gemiste punten van deze week toevoegen
				if histText != "":
					self.hasText = True
					self.text += histText + "\n\n"

				# Alle punten van vandaag toevoegen, indien er minimaal 1 openstaande is.
				if weeklyDag.find("[ ]") > 0:
					self.hasText = True
					self.text += weeklyDag + "\n\n"

				# Open algemene TODO toevoegen
				if todoText != "":
					self.hasText = True
					self.text += "## TODO\n" + todoText + "\n\n"

			# Omzetten naar HTML gezien main dat verwacht.
			self.text = f.plain2hml(self.text).rstrip()

	def HasText(self):
		return super(MarkdownTodo, self).HasText()

	def GetText(self):
		return super(MarkdownTodo, self).GetText()


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
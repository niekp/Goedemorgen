import json
import caldav
import pytz
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse

# Caldav includes
from caldav.davclient import DAVClient
from caldav.objects import Principal, Calendar, Event, DAVObject, CalendarSet, FreeBusy
from caldav.lib.url import URL
from caldav.lib import url
from caldav.lib import error
from caldav.lib.namespace import ns
from caldav.elements import dav, cdav
from caldav.lib.python_utilities import to_local, to_str

from modules import _Module

# Object reference: https://pythonhosted.org/caldav/caldav/objects.html
# Voorbeeld code: https://bitbucket.org/cyrilrbt/caldav/src/default/tests/test_caldav.py?at=default&fileviewer=file-view-default
# vevent = class ContentLine(VBase): https://github.com/eventable/vobject/blob/master/vobject/base.py

class Agenda(_Module):

	def __init__(self, config_full):
		self.hasText = False
		self.text = "";
		
		config = config_full["Agenda"]
		if 'TZ' in config:
			tz = pytz.timezone(config_full["TZ"])
		else:
			tz = pytz.timezone("Europe/Amsterdam")

		# Verbinding maken met CalDav agenda
		client = caldav.DAVClient(config["url"])
		principal = client.principal()
		calendars = principal.calendars()

		first_all = True
		# Lus door de beschikbare agenda's heen
		for calendar in calendars:
			# Zoek de naam hiervan op
			calendar_name = calendar.get_properties([dav.DisplayName(),])["{DAV:}displayname"]

			# Alleen doorgaan indien de agenda in de 'calendars' config regel staat
			if calendar_name in config["calendars"]:
				first = True

				now = tz.localize(datetime.now())

				# Evenementen voor vandaag zoeken, met een beetje buffer terug in de tijd.
				results = calendar.date_search(now - timedelta(hours=2), now + timedelta(days=1))
				for vevent in results:
					event = Event(client=client, url=vevent.url)
					event.load()

					# Oke.. in de documentatie niks over hoe hier een nette string van te maken
					# En in het object zelf zit ook niet echt een functie daarvoor, los van __str()__
					start = event.instance.vevent.dtstart.__str__()
					summary = event.instance.vevent.summary.__str__()
					# Zo kan het ook.
					summary = summary.replace("<SUMMARY{}", "")[:-1]
					# Dit komt binnen: <DTSTART{'X-VOBJ-ORIGINAL-TZID': ['Europe/Amsterdam']}
					# Dus split op } en dan de eerste verwijderen, en het > teken achteraan verwijderen
					start = parse(''.join(start.split("}")[1:])[:-1])

					# Eerste event in deze agenda? Toon de agenda naam
					if first:
						# Niet de eerste agenda? Extra witregel
						if not first_all:
							self.text += "\n"

						self.text += "_" + calendar_name + "_\n"
						first = False
						first_all = False

					# Event samenvatting (tijd + omschijving) toevoegen aan de text
					self.text += "{0} {1}\n".format(start.strftime("%A %H:%M"), summary)


		if not first_all:
			self.hasText = True

	def HasText(self):
		return super(Agenda, self).HasText()

	def GetText(self):
		return super(Agenda, self).GetText()

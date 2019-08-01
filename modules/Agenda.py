import json
import caldav
import pytz
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from lib import Functions as f

# Caldav includes
from caldav.davclient import DAVClient
from caldav.objects import Principal, Calendar, Event, DAVObject, CalendarSet, FreeBusy
from caldav.lib.url import URL
from caldav.lib import url
from caldav.lib import error
from caldav.lib.namespace import ns
from caldav.elements import dav, cdav
from caldav.lib.python_utilities import to_local, to_str

# Google includes
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from modules import _Module

# Object reference: https://pythonhosted.org/caldav/caldav/objects.html
# Voorbeeld code: https://bitbucket.org/cyrilrbt/caldav/src/default/tests/test_caldav.py?at=default&fileviewer=file-view-default
# vevent = class ContentLine(VBase): https://github.com/eventable/vobject/blob/master/vobject/base.py
# Google credentials: https://developers.google.com/calendar/quickstart/python


class Agenda(_Module):

    def Run(self):
        if self.config_full["Agenda"]["credentials.json"]:
            self.Google()
        else:
            self.Caldav()

    def Google(self):
        creds = self.GetGoogleCreds()

        service = build('calendar', 'v3', credentials=creds)

        now = (datetime.utcnow() - timedelta(hours=2)).isoformat() + 'Z'
        tomorrow = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'

        # pylint: disable=no-member
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              timeMax=tomorrow, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if events:
            self.text += "<h3>Agenda</h3>"
            self.hasText = True

            for event in events:
                start = self.convertDate(event['start'].get(
                    'dateTime', event['start'].get('date')))
                self.text += "{0} {1}<br/>".format(start, event['summary'])

    # De datum komt als yyyy-mm-ddThh:mm:ss+hh:mm:ss binnen, maar strftime vind dat niet leuk. Dus sloop de : uit de timezone
    def convertDate(self, dt):
        dt_array = dt.split("+")
        if len(dt_array) == 2:
            if dt_array[1]:
                dt_array[1] = dt_array[1].replace(':', '')

            return datetime.strptime('+'.join(dt_array), "%Y-%m-%dT%H:%M:%S%z").strftime("%A %H:%M")

        return datetime.strptime(dt, "%Y-%m-%d").strftime("%A")

    def GetGoogleCreds(self):
        pickle_filename = "{0}/token.pickle".format(
            self.config_full["Runtime"]["userdir"])
        credentials_filename = "{0}/credentials.json".format(
            self.config_full["Runtime"]["userdir"])

        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        with open(credentials_filename, 'w') as outfile:
            json.dump(self.config["credentials.json"], outfile)

        creds = None
        if os.path.exists(pickle_filename):
            with open(pickle_filename, 'rb') as token:
                creds = pickle.load(token)

        # Eerste run handmatig om de oauth te voltooien.
        # Draai lokaal en kopieer de token handmatig naar de server als de callback niet werkt.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_filename, SCOPES)
                creds = flow.run_local_server()

            # Sla de creds op
            with open(pickle_filename, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def Caldav(self):
        # Verbinding maken met CalDav agenda
        client = caldav.DAVClient(self.config["url"])
        principal = client.principal()
        calendars = principal.calendars()

        first_all = True
        # Lus door de beschikbare agenda's heen
        for calendar in calendars:
            # Zoek de naam hiervan op
            calendar_name = calendar.get_properties([dav.DisplayName(), ])[
                "{DAV:}displayname"]

            # Alleen doorgaan indien de agenda in de 'calendars' config regel staat
            if calendar_name in self.config["calendars"]:
                first = True

                now = f.Now(self.config_full)

                # Evenementen voor vandaag zoeken, met een beetje buffer terug in de tijd.
                results = calendar.date_search(
                    now - timedelta(hours=2), now + timedelta(days=1))
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
                            self.text += "<br/>"

                        self.text += "<h3>" + calendar_name + "</h3>"
                        first = False
                        first_all = False

                    # Event samenvatting (tijd + omschijving) toevoegen aan de text
                    dt = "%A %H:%M"
                    if (calendar_name.lower().find("birthday") >= 0 or calendar_name.lower().find("verjaardag") >= 0):
                        dt = "%A"

                    self.text += "{0} {1}<br/>".format(
                        start.strftime(dt), summary)

        if not first_all:
            self.hasText = True

import datetime
import json
import urllib
from lib import Functions as f
from modules import _Module
from math import sin, cos, sqrt, atan2, radians


class ANWB(_Module):

    def Run(self):
        with urllib.request.urlopen("https://www.anwb.nl/feeds/gethf") as url:
            data = json.loads(url.read())

        for entry in data["roadEntries"]:
            if entry["road"] in self.config['roads']:
                roadSettings = self.config["roads"][entry["road"]]

                checkLocation = (
                    "latitude" in roadSettings and "longitude" in roadSettings and "km" in roadSettings)

                # "loc", "toLoc", "fromLoc"
                for eventType in entry["events"]:
                    for event in entry["events"][eventType]:

                        if checkLocation and not self.validLocation(event, roadSettings):
                            continue

                        if self.hasText:
                            self.text += "<br />"

                        self.text += "<h3>Verkeersinformatie " + \
                            entry["road"] + "</h3>"
                        self.text += "{0} - {1}: {2}<br />{3}<br />".format(
                            event["from"], event["to"], event["reason"], event["description"])

                        if "events" in event:
                            for subevent in event["events"]:
                                self.text += "* " + subevent["text"] + "<br />"

                        self.hasText = True

    def validLocation(self, event, roadSettings):
        locations = []

        # Build up all location data from the event
        if "loc" in event:
            locations.append(event["loc"])
        if "toLoc" in event:
            locations.append(event["toLoc"])
        if "fromLoc" in event:
            locations.append(event["fromLoc"])

        # Check if there is one location within the given range
        for coords in locations:
            if (self.getDistance(coords["lat"], coords["lon"], roadSettings["latitude"], roadSettings["longitude"])) < roadSettings["km"]:
                return True

        return False

    def getDistance(self, latitude1, longitude1, latitude2, longitude2):
        # approximate radius of earth in km
        R = 6373.0

        lat1 = radians(latitude1)
        lon1 = radians(longitude1)
        lat2 = radians(latitude2)
        lon2 = radians(longitude2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance

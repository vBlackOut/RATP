# coding: utf-8
import sys
import requests
import time
import json
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

class RATP():

    def __init__(self, keyapp):
        self.request = requests.session()
        self.token = keyapp
        self.url = "https://apixha.ixxi.net/APIX?"


    def TrafficInformation(self, **kwargs):
        string = ""
        for i, (key, values) in enumerate(kwargs.items()):
            if i == 0:
                string += "{}={}".format(key, values)
            else:
                string += "&{}={}".format(key, values)
        string = "{}{}{}".format(string, "&keyapp=", self.token)

        result = self.request.get("{}{}".format(self.url, string))
        result = result.json()

        for events in result["events"]:
            for incidents in events["incidents"]:
                try:
                    IncidentType = incidents['lines'][0]["incidentSeverity"].encode("utf-8")
                    IncidentLine = incidents['lines'][0]["groupOfLinesName"].encode("utf-8")
                except (KeyError, TypeError):
                    IncidentType = ""
                    IncidentLine = ""

                try:
                    messageIncident = RATP.transforme(incidents['lines'][0]["message"].encode("utf-8"))
                except (KeyError, TypeError):
                    messageIncident = ""

                print("Incident: {}\nType: {}\nInformation: {}\n".format(IncidentType, IncidentLine, messageIncident))

        #return result.json()

    def transforme(self, string):
        string = string.replace("\xc3\x80", "à")
        string = string.replace("\xc3\xa9", "é")
        string = string.replace("\xc3\xa0", "à")
        return string

    def getItinerary(self, **kwargs):
        string = ""
        for i, (key, values) in enumerate(kwargs.items()):
            if i == 0:
                string += "{}={}".format(key, values)
            else:
                string += "&{}={}".format(key, values)
        string = "{}{}{}".format(string, "&keyapp=", self.token)

        result = self.request.get("{}{}".format(self.url, string))
        result = result.json()

        for itineraire in result["itineraries"]:
            numberDirection = len(itineraire["itinerarySegments"])-1
            for i in range(1, numberDirection):
                if i == 1:
                    direction = RATP.transforme(itineraire["itinerarySegments"][i]["details"]["direction"]["name"])
                    itineraireRoute = itineraire["itinerarySegments"][i]["details"]["stopPoints"]
                    groupeLine = itineraire["itinerarySegments"][i]["details"]["groupOfLines"]
                    incidentLine = len(itineraire["itinerarySegments"][i]["trafficEventsRefs"])

                    incidentLine = len(itineraire["itinerarySegments"][i]["trafficEventsRefs"])

                    if incidentLine == 0:
                        print("------\nDirection: {}\nType: {}\nAlert: Pas d'incident.\n------\n".format(direction, groupeLine["name"]))
                    else:
                        print("------\nDirection: {}\nType: {}\nAlert: {}\n------\n".format(direction, groupeLine["name"], incidentLine))

                    for i, station in enumerate(itineraireRoute):
                        s = station["schedule"]
                        f = "%Y-%m-%dT%H:%M:%S+02:00"
                        datetime1 = datetime.datetime.strptime(s, f)
                        datetime2 = datetime.datetime.now()
                        datecalcule = (datetime1 - datetime2)
                        if i == 0:
                            print("Station: {} \n  Zone: {} Départ dans : {} Minutes\n".format(station["name"], station["zone"], datecalcule.seconds/60))
                        else:
                            print("Station: {} \n  Zone: {} Arriver dans : {} Minutes\n".format(station["name"], station["zone"], datecalcule.seconds/60))

                else:
                    try:
                        itineraireRouteStart = itineraire["itinerarySegments"][i]["details"]["endPoint"]["name"]
                        itineraireRouteStartZone = itineraire["itinerarySegments"][i]["details"]["endPoint"]["zone"]
                        itineraireRouteEnd = itineraire["itinerarySegments"][i]["details"]["startPoint"]["name"]
                        itineraireRouteEndZone = itineraire["itinerarySegments"][i]["details"]["endPoint"]["zone"]
                        incidentLine = len(itineraire["itinerarySegments"][i]["trafficEventsRefs"])
                        transportMode = itineraire["itinerarySegments"][i]["transport"]["mode"]

                        s = itineraire["itinerarySegments"][i]["startTime"]
                        s2 = itineraire["itinerarySegments"][i]["endTime"]
                        f = "%Y-%m-%dT%H:%M:%S+02:00"
                        datetime1 = datetime.datetime.strptime(s, f)
                        datetime2 = datetime.datetime.strptime(s2, f)
                        duree = (datetime2 - datetime1)

                        print("------\nStation: {}\ntype: {} \n  Zone: {} Durée: {} Minutes\n------\n".format(itineraireRouteStart, transportMode, itineraireRouteStartZone, duree.seconds/60))

                    except KeyError:
                        incidentLine = len(itineraire["itinerarySegments"][i]["trafficEventsRefs"])
                        direction = RATP.transforme(itineraire["itinerarySegments"][i]["details"]["direction"]["name"])
                        groupeLine = itineraire["itinerarySegments"][i]["details"]["groupOfLines"]
                        incidentLine = len(itineraire["itinerarySegments"][i]["trafficEventsRefs"])
                        itineraireRoute = itineraire["itinerarySegments"][i]["details"]["stopPoints"]
                        line = itineraire["itinerarySegments"][i]["details"]["line"]["code"]

                        if incidentLine == 0:
                            print("Direction: {}\nType: {} {}\nAlert: Pas d'incident.\n".format(direction, groupeLine["name"], line))
                        else:
                            print("Direction: {}\nType: {} {}\nAlert: {}\n".format(direction, groupeLine["name"], line, incidentLine))

                        for i, station in enumerate(itineraireRoute):
                            s = station["schedule"]
                            f = "%Y-%m-%dT%H:%M:%S+02:00"
                            datetime1 = datetime.datetime.strptime(s, f)
                            datetime2 = datetime.datetime.now()
                            datecalcule = (datetime1 - datetime2)
                            if i == 0:
                                print("Station: {} \n  Zone: {} Départ dans : {} Minutes\n".format(station["name"], station["zone"], datecalcule.seconds/60))
                            else:
                                print("Station: {} \n  Zone: {} Arriver dans : {} Minutes\n".format(station["name"], station["zone"], datecalcule.seconds/60))
            print("Temps du trajet: ~{} Minutes (+/-)\n".format(itineraire["duration"]/60))


currentDT = datetime.datetime.now()

timenow = "{}{}".format(currentDT.strftime("%Y-%m-%dT%H:%M:%S"), "%2B0200")

# requests for API google
RATP = RATP(keyapp="FvChCBnSetVgTKk324rO")

req = RATP.TrafficInformation(cmd="getTrafficSituation",
                              withText="true",
                              apixFormat="json",
                              category="all",
                              networkType="all",
                              tmp=time.time())

req = RATP.getItinerary(cmd="getItinerary",
                        withDetails="true",
                        withText="true",
                        withEcoComparator="true",
                        apixFormat="json",
                        apiVersion="2",
                        engine="ratp",
                        leaveTime=timenow,
                        startPointLat="48.9329",
                        startPointLon="2.0412",
                        endPointLat="48.867538",
                        endPointLon="2.36382",
                        prefModes="rail,metro,tram,funicular,bus,bicycle",
                        prefJourney="approachVLS",
                        withMobility="false",
                        withTrafficEvents="true",
                        guidance="bicycle",
                        geometry="bicycle")

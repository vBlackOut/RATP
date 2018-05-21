# coding: utf-8
import requests
import time

class RATP():

    def __init__(self, keyapp):
        self.request = requests.session()
        self.token = keyapp

    def TrafficInformation(self, **kwargs):
        url = "https://apixha.ixxi.net/APIX?"
        string = ""

        for i, (key, values) in enumerate(kwargs.items()):
            if i == 0:
                string += "{}={}".format(key, values)
            else:
                string += "&{}={}".format(key, values)
        string = "{}{}{}".format(string, "&keyapp=", self.token)

        result = self.request.get("{}{}".format(url, string))
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


# requests for API google
RATP = RATP(keyapp="Your_api_key")

req = RATP.TrafficInformation(cmd="getTrafficSituation",
                              withText="true",
                              apixFormat="json",
                              category="all",
                              networkType="all",
                              tmp=time.time())

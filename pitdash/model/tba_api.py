import requests
from IPython.display import Image

class TbaAPI:
    def __init__(self, season, district_code, team_number, event_code) -> None:
        self.season = season
        self.district_code = district_code
        self.team_number = team_number
        self.event_code = event_code
        self.headers = {
            "X-TBA-Auth-Key":"fAxSicPC9UjoF2jgIIPqRIpiHeFU26K6Tzt5NN1RH8e2DWbS53bAjkLr8FBGYOW2",
            "If-Modified-Since":""
        }
    
    def get_from_api(self, endpoint, query):
        url = 'https://www.thebluealliance.com/api/v3/'+ endpoint + query
        print(url)
        r = requests.get(url, headers=self.headers)
        # print(r.json())
        return r.json()

    def get_event_oprs(self, event_key):
        endpoint = 'event/'
        query = event_key+'/oprs'
        json = self.get_from_api(endpoint, query)
        ccwms=json['ccwms']
        oprs=json["oprs"]
        dprs=json["dprs"]
        return ccwms, oprs, dprs    

    def get_event_team_oprs(self, event_code, team_number):
        endpoint = 'event/'
        query = self.season+event_code+'/oprs'
        team_key = 'frc'+team_number
        json = self.get_from_api(endpoint, query)
        if json['ccwms'] != None and json:
            ccwms=round(json['ccwms'][team_key],2)
        if json['oprs'] != None:
            oprs=round(json["oprs"][team_key],2)
        if json['dprs'] != None:
            dprs=round(json["dprs"][team_key],2)
        return ccwms, round(oprs,2), round(dprs,2)    
import requests
from IPython.display import Image
import pandas as pd

tba_auth = "fAxSicPC9UjoF2jgIIPqRIpiHeFU26K6Tzt5NN1RH8e2DWbS53bAjkLr8FBGYOW2"

class TbaAPI:
    def __init__(self, season, district_code) -> None:
        self.season = season
        self.district_code = district_code
        self.headers = {
            "X-TBA-Auth-Key": tba_auth,
            "If-Modified-Since": ""
        }
    
    def get_from_api(self, endpoint, query):
        url = 'https://www.thebluealliance.com/api/v3/'+ endpoint + query
        print(url)
        r = requests.get(url, headers=self.headers)
        # print(r.json())
        return r.json()

    def get_first_event_code(self, event_code):
        endpoint = 'event/'
        query = self.season + event_code
        json = self.get_from_api(endpoint, query)
        frc_event_code=json["first_event_code"]
        return frc_event_code

    def get_event_oprs(self, event_code):
        endpoint = 'event/'
        query = self.season + event_code + '/oprs'
        json = self.get_from_api(endpoint, query)
        ccwms=json['ccwms']
        oprs=json["oprs"]
        dprs=json["dprs"]
        return ccwms, oprs, dprs    

    def get_event_team_oprs(self, event_code, team_number):
        endpoint = 'event/'
        query = self.season + event_code + '/oprs'
        team_key = 'frc' + team_number
        json = self.get_from_api(endpoint, query)
        if json and json['ccwms'] != None:
            ccwms=round(json['ccwms'][team_key],2)
        if json and json['oprs'] != None:
            oprs=round(json["oprs"][team_key],2)
        if json and json['dprs'] != None:
            dprs=round(json["dprs"][team_key],2)
        return ccwms, oprs, dprs   
    
    def get_event_matches(self, event_code, team_number):
        endpoint = 'event/'
        query = self.season + event_code + '/matches'
        team_key = 'frc' + team_number
        json = self.get_from_api(endpoint, query)
        # print(json)
        return json   
    
    def get_event_matches_df(self, event_code, team_number):
        endpoint = 'event/'
        query = self.season + event_code + '/matches'
        team_key = 'frc'+team_number
        json = self.get_from_api(endpoint, query)
        df = pd.DataFrame(json)
        # print(df)
        return json   
import base64
import requests
from IPython.display import Image

class FrcAPI:
    def __init__(self, season, district_code, team_number, event_code) -> None:
        self.season = season
        self.district_code = district_code
        self.team_number = team_number
        self.event_code = event_code
        auth = base64.b64encode(bytes('karlfl:e70b17fc-8e94-4526-b878-101b2d1cc424','utf-8')).decode('utf-8')
        self.headers = {
            "Authorization":"Basic " + str(auth),
            "If-Modified-Since":""
        }
    
    def get_from_api(self, endpoint, query):
        url = 'https://frc-api.firstinspires.org/v3.0/'+self.season+'/'+endpoint+query
        print(url)
        r = requests.get(url, headers=self.headers)
        # print(r.json())
        return r.json()


    def get_avatar_image_encoded(self) -> str:
        endpoint = 'avatars'
        query = '?teamNumber='+self.team_number
        # r = requests.get('https://frc-api.firstinspires.org/v3.0/'+self.season+'/avatars?teamNumber='+self.team_number, headers=self.headers)
        imageJson = self.get_from_api(endpoint, query)
        # print (r.json() )
        if len(imageJson["teams"]) > 0:
            teamJson = imageJson["teams"][0]
            # print(teamJson)
            return teamJson["encodedAvatar"]
        else:
            return None    
        
    def get_team_details(self):
        endpoint = 'teams'
        query = '?teamNumber='+self.team_number
        json = self.get_from_api(endpoint, query)
        # r = requests.get('https://frc-api.firstinspires.org/v3.0/'+self.season+'/avatars?teamNumber='+self.team_number, headers=self.headers)
        return json["teams"][0]    
    
    def get_district_record(self):
        endpoint = 'rankings/district'
        query = '?district='+self.district_code+'&teamNumber='+self.team_number
        r = self.get_from_api(endpoint, query)
        # r = requests.get('https://frc-api.firstinspires.org/v3.0/'+season+'/rankings/district?district='+districtCode+'&teamNumber='+teamNumber, headers=headers)
        distTeam = r.json()['districtRanks'][0]
        # print(eventTeam)
        return distTeam
    
    def get_event_details(self, tournament_level ='qual'):
        endpoint = 'events'
        query = '?eventCode=' + self.event_code
        json = self.get_from_api(endpoint, query)
        # Event Rank/Record
        # r = requests.get('https://frc-api.firstinspires.org/v3.0/'+season+'/rankings/'+eventCode+'?teamNumber='+teamNumber, headers=headers)
        event = json['Events'][0]
        # print (eventTeam)
        # rank = eventTeam["rank"]
        # record = "{}-{}-{}".format(eventTeam["wins"], eventTeam["losses"],eventTeam["ties"])
        # print("Event: {}\t Ranking: {}\t Record: {}".format(eventCode,rank,record))
        return event  
     
    def get_event_ranking(self, tournament_level ='qual'):
        endpoint = 'rankings/'+self.event_code
        query = '?teamNumber=' + self.team_number
        json = self.get_from_api(endpoint, query)
        # Event Rank/Record
        # r = requests.get('https://frc-api.firstinspires.org/v3.0/'+season+'/rankings/'+eventCode+'?teamNumber='+teamNumber, headers=headers)
        if len(json["Rankings"]) > 0:
            eventTeam = json['Rankings'][0]
        else:
            eventTeam = None
        # print (eventTeam)
        # rank = eventTeam["rank"]
        # record = "{}-{}-{}".format(eventTeam["wins"], eventTeam["losses"],eventTeam["ties"])
        # print("Event: {}\t Ranking: {}\t Record: {}".format(eventCode,rank,record))
        return eventTeam
    
    def get_event_matches(self, tournament_level ='qual'):
        endpoint = 'matches/'+self.event_code
        query = '?tournamentLevel=' + tournament_level + '&teamNumber=' + self.team_number
        json = self.get_from_api(endpoint, query)
        # r = requests.get('https://frc-api.firstinspires.org/v3.0/' + season + '/matches/' + eventCode + "?tournamentLevel=" + tournLevel + "&teamNumber=" + teamNumber, headers=headers)
        # print(json["Matches"])
        return json["Matches"]

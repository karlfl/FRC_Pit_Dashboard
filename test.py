import base64
import requests
auth = base64.b64encode(bytes('karlfl:e70b17fc-8e94-4526-b878-101b2d1cc424','utf-8')).decode('utf-8')
headers = {
    "Authorization":"Basic " + str(auth),
    "If-Modified-Since":""
}

endpoint = 'matches/'+self.event_code
query = '?tournamentLevel=' + tournament_level + '&teamNumber=' + self.team_number
json = self.get_from_api(endpoint, query)
# r = requests.get('https://frc-api.firstinspires.org/v3.0/' + season + '/matches/' + eventCode + "?tournamentLevel=" + tournLevel + "&teamNumber=" + teamNumber, headers=headers)
# print(json["Matches"])
print(json["Matches"])


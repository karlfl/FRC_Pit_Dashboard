from model.api.frc_api import FrcAPI
from model.api.tba_api import TbaAPI

class PitData:
    def __init__(self, season, team_number, event_code, district_code='FIM') -> None:
        self.season = season
        self.district_code = district_code
        self.team_number = team_number
        self.tba_event_code = event_code
        self.tba_model = TbaAPI(season, district_code)
        self.first_event_code = self.tba_model.get_first_event_code(self.tba_event_code)
        self.frc_model = FrcAPI(season, district_code)

    def get_event_details(self):
        event_details = self.frc_model.get_event_details(self.first_event_code)
        return {
            "code": self.first_event_code,
            "name": event_details["name"]
        }
    
    def get_team_details(self):
        team_avatar = self.frc_model.get_avatar_image_encoded(self.team_number)
        team_details = self.frc_model.get_team_details(self.team_number)
        return  {
            "number": self.team_number,
            "avatar": team_avatar,
            "name": team_details["nameShort"]
        }
    
    def get_team_stats(self):
        event_ranking = self.frc_model.get_event_ranking(self.first_event_code, self.team_number)
        team_ccwms, team_oprs, team_dprs = self.tba_model.get_event_team_oprs(self.tba_event_code, self.team_number)
        return  {
            "rank": event_ranking["rank"],
            "wins": event_ranking["wins"],
            "losses": event_ranking["losses"],
            "ties": event_ranking["ties"],
            "ccwms": team_ccwms,
            "oprs": team_oprs,
            "dprs": team_dprs,
        }
    
    def get_matches(self):
        qual_matches = self.frc_model.get_event_matches(self.first_event_code, self.team_number, tournament_level='qual')
        playoff_matches = self.frc_model.get_event_matches(self.first_event_code, self.team_number, tournament_level='playoff')
        return {
            "qualification": qual_matches,
            "playoff": playoff_matches
        }

    def get_matches_df(self):
        return self.tba_model.get_event_matches_df(self.tba_event_code, self.team_number)
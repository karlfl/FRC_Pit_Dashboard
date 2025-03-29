from model.api.frc_api import FrcAPI
from model.api.tba_api import TbaAPI


class EventData:
    def __init__(self, season, district_code="FIM"):
        self.season = season
        self.district_code = district_code
        self.tba_model = TbaAPI(season, district_code)
        self.frc_model = FrcAPI(season, district_code)

    def get_event_list_df(self):
        event_list = self.frc_model.get_events_df()
        return event_list


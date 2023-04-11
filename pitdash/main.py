from flask import Flask, render_template, request
from datetime import datetime

from google.appengine.api import memcache, wrap_wsgi_app

from model.frc_api import FrcAPI
from model.tba_api import TbaAPI

from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "MemcachedCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 60
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app)

# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/pitdash/<season>/<eventCode>/<teamNumber>")
@cache.memoize(120)
def pit_dash(season, eventCode, teamNumber):
    model = FrcAPI(season=season, district_code="FIM", team_number=teamNumber,event_code=eventCode)
    team_avatar = model.get_avatar_image_encoded()
    team_details = model.get_team_details()
    event_details = model.get_event_details()
    event_ranking = model.get_event_ranking()
    qual_matches = model.get_event_matches(tournament_level='qual')
    playoff_matches = model.get_event_matches(tournament_level='playoff')
    tba_model = TbaAPI(season=season, district_code="FIM", team_number=teamNumber,event_code=eventCode)
    team_ccwms, team_oprs, team_dprs = tba_model.get_event_team_oprs(eventCode, teamNumber)
    return render_template("pitdash.html", team = team_details, 
                           image = team_avatar, 
                           event_details = event_details, 
                           event_rank = event_ranking, 
                           qual_matches = qual_matches,
                           playoff_matches = playoff_matches,
                           ccwms=team_ccwms,
                           oprs=team_oprs,
                           dprs=team_dprs,
                           event_code = eventCode.upper())

if __name__=='__main__':
    app.run(debug=True)
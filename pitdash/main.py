import os
from flask import Flask, render_template, request
from datetime import datetime

from google.appengine.api import memcache, wrap_wsgi_app

from model.pitdash import PitData
from model.eventdata import EventData

from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "MemcachedCache", 
    "CACHE_DEFAULT_TIMEOUT": 3600
}
if os.environ.get('MEMCACHIER_SERVERS') == None:
    config["CACHE_TYPE"] = "SimpleCache"

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app)

# Replace the existing home function with the one below
@app.route("/")
@cache.memoize()
def home():
    return render_template("home.html")

# New functions
@app.route("/about/")
@cache.memoize()
def about():
    return render_template("about.html")

@app.route("/contact/")
@cache.memoize()
def contact():
    return render_template("contact.html")

@app.route("/pitdash/")
@cache.memoize()
def pit_dash_main():
    season = current_year = datetime.today().year
    pit_model = PitData(str(season), '7491', 'miket')
    match_df = pit_model.get_matches_df()
    return pit_dash(str(season), eventCode='miket', teamNumber='7491')


@app.route("/pitdash/<season>/<eventCode>/<teamNumber>")
@cache.memoize()
def pit_dash(season, eventCode, teamNumber):
    pit_model = PitData(season, teamNumber, eventCode)
    event = pit_model.get_event_details()
    team = pit_model.get_team_details()
    stats = pit_model.get_team_stats()
    matches = pit_model.get_matches()
    return render_template("pitdash.html",
                           season = season, 
                           event = event, 
                           team = team,
                           stats = stats,
                           matches = matches)

@app.route("/events")
@cache.memoize()
def events():
    season = current_year = datetime.today().year
    event_model = EventData(str(season))
    events = event_model.get_event_list_df().sort_values(by=['weekNumber','code'])
    # return events.to_html(header="true", table_id="table")
    return render_template("events.html", events=events)

@app.template_filter('custom_replace')
def custom_replace(s, old, new):
    return s.replace(old, new)

    
if __name__=='__main__':
    app.run(debug=True)
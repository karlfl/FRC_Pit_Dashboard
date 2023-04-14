import os
from flask import Flask, render_template, request
from datetime import datetime

from google.appengine.api import memcache, wrap_wsgi_app

from model.pitdash import PitData

from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "MemcachedCache",  # Flask-Caching related configs
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

@app.route("/pitdash/<season>/<eventCode>/<teamNumber>")
@cache.memoize(120)
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

if __name__=='__main__':
    app.run(debug=True)
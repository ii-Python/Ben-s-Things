# Modules
from app import app
from os import getenv

from requests import get
from flask import render_template, request

# Routes
@app.route("/")
def index():

    return render_template("index.html"), 200

@app.route("/about")
def about():

    return render_template("pages/about.html"), 200

@app.route("/generate")
def gentext():

    return render_template("generators/text.html"), 200

@app.route("/paint")
def paint():

    return render_template("pages/paint.html"), 200

@app.route("/start")
def startpage():

    # Load our IPInfo statistics
    resp = get(f"https://ipinfo.io/{request.headers.get('X-Forwarded-For')}/json?token={getenv('IPINFO')}").json()

    # Approximate our weather
    weather = None

    if "loc" in resp:

        location = resp["loc"].split(',')

        lat = location[0]
        lon = location[1]

        weather = app.core.get_weather(lon, lat)

    # Render the template :)
    return render_template(
        "pages/start.html",
        weather = weather,
        ip = resp
    ), 200

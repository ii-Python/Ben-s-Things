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

@app.route("/sitemap")
def sitemap():

    def empty_url(rule):

        # taken from https://stackoverflow.com/questions/13317536/get-list-of-all-routes-defined-in-the-flask-app
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()

        return len(defaults) >= len(arguments)

    sitemap = ""
    inlist = 0

    maxsize = 4

    for endpoint in app.url_map.iter_rules():

        if "GET" in endpoint.methods and empty_url(endpoint) and not "api" in str(endpoint):

            url = f"<a href = \"{ endpoint }\">{ endpoint }</a> "

            if inlist == maxsize:

                sitemap += f"{url} <br>"

                inlist = 0

            else:

                sitemap += url

            inlist += 1

    return render_template(
        "pages/sitemap.html",
        sitemap = sitemap
    ), 200

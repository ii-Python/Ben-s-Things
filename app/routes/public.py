# Modules
import json
import random

import string
from app import app

from os import getenv
from requests import get

from werkzeug.urls import url_parse
from flask import render_template, request, abort, redirect, url_for

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

@app.route("/writer")
def writer():
    return render_template("pages/writer.html"), 200

@app.route("/sprint")
def sprint():
    return render_template("pages/sprint.html"), 200

@app.route("/shortener", methods = ["GET", "POST"])
def shortener():

    # Render our shortener page
    if request.method == "GET":
        return render_template("pages/shortener.html"), 200

    # Let's do some shortening
    url = request.form.get("url")

    if not url:
        return abort(400)  # haha loSER

    # URL Shortener
    def shorten_url(url):

        # Check protocol
        if "://" not in url:
            url = "http://" + url

        # Load our current URLs
        with open("data/urls.json", "r") as f:
            urls = json.loads(f.read())

        # Check if we already shortened this URL
        code = None

        for _ in urls:
            if urls[_] == url:
                code = _

        # Nope, we need to make a code
        if not code:

            while True:
                code = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

                # Ensure we don't reassign a code
                if code not in urls:
                    break

        # Save our URL
        urls[code] = url

        with open("data/urls.json", "w") as f:
            f.write(json.dumps(urls, indent = 4))

        # Return code
        return code

    code = shorten_url(url)

    # Redirect to our homepage
    return redirect(url_for("index", message = f"URL Shortened! New URL: https://{url_parse(request.url).host}/{code}"))

@app.route("/<string:url>")
def shorturl(url):

    # Load our current URLs
    with open("data/urls.json", "r") as f:
        urls = json.loads(f.read())

    # Nope, not a valid url
    if url not in urls:
        return abort(404)

    # It's valid, so redirect us
    return render_template("pages/redirect.html", url = urls[url]), 200

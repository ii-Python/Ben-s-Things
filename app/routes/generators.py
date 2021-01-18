# Modules
import io
import sys

from app import app
from os import listdir

from requests import get
from flask import make_response, request, abort, render_template

try:
    from PIL import Image, ImageDraw, ImageFont

except ModuleNotFoundError:
    pass

# Routes
@app.route("/text")
def genImage():

    query = request.args.get("text", "None")
    font = request.args.get("font", "regular")

    try:
        r = int(request.args.get("r", 255))
        g = int(request.args.get("g", 255))
        b = int(request.args.get("b", 255))

    except ValueError:
        return "Invalid RGB value.", 400

    for file in listdir("assets/fonts"):
        if font in file.lower():
            font = file

    if font not in listdir("assets/fonts"):
        return "Invalid font.", 404

    fontsize = 60

    if len(query) > 30:

        excess = len(query) - 30

        if excess > 300:
            return "Payload too large, must be at most 360 characters.", 400

        fontsize -= excess

    # Image drawing
    image = Image.new("RGBA", (1366, 80), color = (0, 0, 0, 0))
    d = ImageDraw.Draw(image)

    try:
        d.text((10, 10), query, font = ImageFont.truetype(f"assets/fonts/{font}", fontsize), fill = (r, g, b))
    except OSError:

        # Caused by spamming
        return abort(400)

    # Image saving
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format = "PNG")

    # Returning
    response = make_response(imgByteArr.getvalue())
    response.headers.set("Content-Type", "image/png")

    return response, 200

@app.route("/badge")
def genBadge():

    title = request.args.get("title")
    description = request.args.get("description")
    color = request.args.get("color", "000000")

    # Color hex removing
    if color[0] == "#":
        color = color[1:]

    # Returning badge
    response = make_response(get(f"https://raster.shields.io/badge/{title}-{description}-{color}.png", allow_redirects = True).content)
    response.headers.set("Content-Type", "image/png")

    return response, 200

@app.route("/badge/generate", methods = ["GET"])
def badgePage():
    return render_template("generators/badge.html"), 200

@app.route("/embed", methods = ["GET"])
def generateEmbed():
    return render_template("api/ext/embed.html"), 200

@app.route("/embed/generate", methods = ["GET"])
def embedPage():
    return render_template("generators/embed.html"), 200

@app.route("/oembed", methods = ["GET"])
def generateOEmbed():

    author = request.args.get("author")

    if not author:
        return abort(400)

    response = '{{"type":"photo","author_name":"{}"}}'
    return response.format(author), 200

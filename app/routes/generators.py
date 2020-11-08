# Modules
import io
from app import app

from os import listdir
from requests import get

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from PIL import Image, ImageDraw, ImageFont
from flask import make_response, request, abort, render_template

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

    fontsize = 45

    if len(query) > 60:

        excess = len(query) - 60

        if excess > 300:

            return "Payload too large, must be at most 360 characters.", 400

        fontsize -= excess

    image = Image.new("RGBA", (1366, 70), color = (0, 0, 0, 0))

    d = ImageDraw.Draw(image)

    d.text((10, 10), query, font = ImageFont.truetype(f"assets/fonts/{font}", fontsize), fill = (r, g, b))

    imgByteArr = io.BytesIO()

    image.save(imgByteArr, format = "PNG")

    response = make_response(imgByteArr.getvalue())

    response.headers.set("Content-Type", "image/png")

    return response, 200

@app.route("/badge")
def genBadge():

    beginning = request.args.get("b", "None")

    end = request.args.get("e", "None")

    color = request.args.get("color", "<COLOR>")

    imgByteArr = io.BytesIO()

    render = svg2rlg(io.BytesIO(get(f"https://img.shields.io/badge/{beginning}-{end}-{color}.svg", allow_redirects = True).content))

    renderPM.drawToFile(render, imgByteArr, fmt = "PNG")

    response = make_response(imgByteArr.getvalue())

    response.headers.set("Content-Type", "image/png")

    return response, 200

@app.route("/embed", methods = ["GET"])
def generateEmbed():

    return render_template("api/embed.html"), 200

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

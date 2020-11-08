# Modules
import string
from app import app

from requests import get
from random import choice

from app.database import DB
from json import loads, dumps

from os import getenv, listdir
from urllib.parse import urlparse

from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, jsonify, request, abort, session, send_from_directory

# Return
def return_data(code, data):

    return jsonify(code = code, data = data)

# Routes
@app.route("/api/<string:version>", methods = ["GET"])
def redir(version):

    return redirect(url_for("fetchdocs", version = version))

@app.route("/api/<string:version>/docs", methods = ["GET"])
def fetchdocs(version):

    try:

        return render_template(f"api/{version}.html"), 200

    except FileNotFoundError:

        return return_data(404, {"message": "The specified API version does not exist."}), 404

@app.route("/upload", methods = ["GET", "POST"])
def upload_image():

    if request.method == "GET":

        return render_template("pages/upload.html"), 200

    elif not request.files:

        return abort(400)  # haha boomer

    try:

        image = request.files["image"]

    except KeyError:

        return abort(400)

    is_valid = False

    for ext in ["png", "jpeg", "jpg", "webp"]:

        if image.filename.endswith(ext):

            is_valid = True

    if not is_valid:

        return render_template("pages/upload.html", error = "Please only upload image files."), 200

    id = "".join(choice(string.ascii_lowercase + string.digits) for _ in range(6))

    image.save(f"data/images/{id}.{image.filename.split('.')[-1]}")

    return redirect(url_for("image", i = id))

@app.route("/image", methods = ["GET"])
def image():

    id = request.args.get("i")

    if not id:

        return abort(400)  # haha you still cant use my website properly

    filename = ""

    for file in listdir("data/images"):

        if file.split(".")[0] == id:

            filename = file

    if not filename:

        return abort(404)  # image doesnt exist

    return send_from_directory("data/images", filename), 200

# URL Shortener
@app.route("/shortener", methods = ["GET", "POST"])
def shortener():

    # Render our shortener page
    if request.method == "GET":

        return render_template("pages/shortener.html"), 200

    # Let's do some shortening
    url = request.form.get("url")

    if not url:

        return abort(400)  # haha loSER

    # Load our current URLs
    with open("data/urls.json", "r") as f:

        urls = loads(f.read())

    # Check if we already shortened this URL
    code = None

    for _ in urls:

        if urls[_] == url:

            code = _

    # Nope, we need to make a code
    if not code:

        code = "".join(choice(string.ascii_lowercase + string.digits) for _ in range(6))

    # Save our URL
    urls[code] = url

    with open("data/urls.json", "w") as f:

        f.write(dumps(urls, indent = 4))

    # Redirect to our homepage
    return redirect(url_for("index", message = f"URL Shortened! New URL: https://{url_parse(request.url).host}/{code}"))

@app.route("/<string:url>")
def shorturl(url):

    # Load our current URLs
    with open("data/urls.json", "r") as f:

        urls = loads(f.read())

    # Nope, not a valid url
    if url not in urls:

        return abort(404)

    # It's valid, so redirect us
    return render_template("pages/redirect.html", url = urls[url]), 200

# API Routes
@app.route("/api/v1/oauth", methods = ["GET"])
def login_api():

    redir = request.args.get("redir")

    if not redir:

        abort(400)

    elif "username" not in session:

        app.core.set_redirect("login_api", args = {"redir": redir})

        return redirect(url_for("login"))

    db = DB()

    code = db.get_token(session["username"])

    return render_template(
        "api/redirect.html",
        url = redir,
        code = code
    ), 200

@app.route("/api/v1/user", methods = ["GET"])
def userInformation():

    auth = request.args.get("auth", request.args.get("code"))

    if not auth:

        return return_data(403, {"message": "No authorization provided."}), 403

    db = DB()

    user = db.get_user_by_token(auth)

    if not user:

        return return_data(403, {"message": "Invalid authorization."}), 403

    return jsonify(username = user[0], signupDate = user[2])

@app.route("/api/v1/authenticate", methods = ["POST"])
def authenticateUser():

    username = request.form.get("username")

    password = request.form.get("password")

    if not username or not password:

        return return_data(400, {"message": "Username/password missing from request."}), 400

    db = DB()

    if not db.user_exists(username):

        return return_data(403, {"message": "The specified username does not exist."}), 403

    elif not db.checkpw(username, password):

        return return_data(403, {"message": "The specified password is invalid."}), 403

    return return_data(200, {"message": "200 OK"}), 200

@app.route("/api/v1/generate", methods = ["POST"])
def generateImage():

    text = request.form.get("text")

    font = request.form.get("font")

    if not text:

        return return_data(400, {"message": "No text was specified."}), 400

    for char in text:

        if char in ["!", "*", "'", "(", ")", ",", ":", "@", "&", "=", "+", "$", ",", "/", "?", "#", "[", "]"]:

            return return_data(400, {"message": "The specified text contains invalid characters."}), 400

    url = f"/text?text={text}"

    if font:

        if font not in ["thin", "bold", "italic", "regular", "black", "light", "medium"]:

            return return_data(400, {"message": "The specified font does not exist."}), 400

        url = url + "&font=" + font

    url = "https://" + urlparse(request.base_url).hostname + url

    return return_data(200, {"url": url}), 200

@app.route("/api/v1/badge", methods = ["POST"])
def generateBadge():

    begin = request.form.get("begin")

    ending = request.form.get("end")

    color = request.form.get("color")

    if not begin or not ending:

        return return_data(400, {"message": "No text was specified."}), 400

    for char in begin:

        if char in ["!", "*", "'", "(", ")", ",", ":", "@", "&", "=", "+", "$", ",", "/", "?", "#", "[", "]"]:

            return return_data(400, {"message": "The specified text contains invalid characters."}), 400

    for char in ending:

        if char in ["!", "*", "'", "(", ")", ",", ":", "@", "&", "=", "+", "$", ",", "/", "?", "#", "[", "]"]:

            return return_data(400, {"message": "The specified text contains invalid characters."}), 400

    if color.startswith("#"):

        color = color[1:]

    for char in color:

        if char in ["!", "*", "'", "(", ")", ",", ":", "@", "&", "=", "+", "$", ",", "/", "?", "#", "[", "]"]:

            return return_data(400, {"message": "The specified color contains invalid characters."}), 400

    url = f"/badge?b={begin}&e={ending}&color={color}"

    url = "https://" + urlparse(request.base_url).hostname + url

    return return_data(200, {"url": url}), 200

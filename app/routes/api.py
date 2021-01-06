# Modules
import string
import youtube_dl

from app import app
from requests import get

from random import choice
from fnmatch import fnmatch

from json import loads, dumps
from os import getenv, listdir

from werkzeug.urls import url_parse
from ..utils.youtube import YoutubeSearch

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
def upload_file():

    if request.method == "GET":
        return render_template("pages/upload.html"), 200

    elif not request.files:
        return abort(400)  # haha boomer

    try:
        file = request.files["uploadfile"]

    except KeyError:
        return abort(400)

    # Check our maximum upload size without reading into RAM
    size = app.core.locate_size(file)
    if size > (20 * (1024 ** 2)):
        return render_template("pages/upload.html", error = "Maximum upload size is 20MB."), 200

    id = "".join(choice(string.ascii_lowercase + string.digits) for _ in range(6))
    file.save(f"data/files/{id}.{file.filename.split('.')[-1]}")

    # Redirect to our homepage
    return redirect(url_for("index", message = f"File saved, permanent link: https://{url_parse(request.url).host}/file?i={id}"))

@app.route("/file", methods = ["GET"])
def view_file():

    id = request.args.get("i")

    if not id:
        return abort(400)  # haha you still cant use my website properly

    # Locate filename
    filename = ""
    for file in listdir("data/files"):
        if file.split(".")[0] == id:
            filename = file

    if not filename:
        return abort(404)  # file doesnt exist

    # Send content
    return send_from_directory("data/files", filename, conditional = True), 200

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

    elif "://" not in url:
        url = "http://" + url

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

        while True:
            code = "".join(choice(string.ascii_lowercase + string.digits) for _ in range(6))

            # Ensure we don't reassign a code
            if code not in urls:
                break

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
        return abort(400)

    elif "username" not in session:
        app.core.set_redirect("login_api", args = {"redir": redir})
        return redirect(url_for("login"))

    code = app.db.get_token(session["username"])
    return render_template(
        "api/oauth.html",
        url = redir,
        code = code
    ), 200

@app.route("/api/v1/user", methods = ["GET"])
def userInformation():

    auth = request.args.get("auth", request.args.get("code"))

    if not auth:
        return return_data(403, {"message": "No authorization provided."}), 403

    user = app.db.get_user_by_token(auth)
    if not user:
        return return_data(403, {"message": "Invalid authorization."}), 403

    return jsonify(username = user[0], signupDate = user[2]), 200

@app.route("/api/v1/authenticate", methods = ["POST"])
def authenticateUser():

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return return_data(400, {"message": "Username/password missing from request."}), 400

    elif not app.db.user_exists(username):
        return return_data(403, {"message": "The specified username does not exist."}), 403

    elif not app.db.checkpw(username, password):
        return return_data(403, {"message": "The specified password is invalid."}), 403

    return return_data(200, {"message": "200 OK"}), 200

@app.route("/api/v1/yt", methods = ["GET"])
def search_youtube():

    # Locate query
    query = request.args.get("query")
    if query is None:
        return return_data(400, "No query was specified to search for.")

    # Locate our count
    count = request.args.get("count", 10)
    try:
        count = int(count)
        if count > 100:
            return return_data(400, "The count value cannot be larger than 100.")

        elif count < 1:
            return return_data(400, "The count value needs to be at least 1.")

    except ValueError:
        return return_data(400, "The specified count value is invalid.")

    # Fetch our page as well
    page = request.args.get("page", 1)
    try:
        page = int(page)

        if page < 1:
            return return_data(400, "Page must at least be 1.")

    except ValueError:
        return return_data(400, "Specified page number is invalid.")

    # Check for a playlist
    results = None
    if fnmatch(query, "*://www.youtube.com/playlist?list=*"):

        # Extract videos
        videos = []
        with youtube_dl.YoutubeDL({}) as ytdl:
            info = ytdl.extract_info(query, download = False)

        for vid in info["entries"]:
            videos.append({"title": vid["title"], "id": vid["id"], "url": vid["webpage_url"]})

        results = videos

    # Search youtube
    if results is None:
        resp = YoutubeSearch(query, max_results = count, page = page).to_dict()
        results = []

        for r in resp:
            results.append({"title": r["title"], "id": r["id"], "url": "https://youtube.com" + r["url_suffix"]})

    # Format response
    data = {
        "results": results
    }

    return dumps(data), 200

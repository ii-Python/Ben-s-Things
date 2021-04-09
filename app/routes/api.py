# Modules
import time
import emoji

import requests
from app import app

from fnmatch import fnmatch
from datetime import datetime

from json import dumps, loads
from ..utils.youtube import YoutubeSearch

from flask import render_template, redirect, url_for, jsonify, request, session, Response

# Load API keys
with open("data/keys.json", "r") as file:
    API_KEYS = loads(file.read())

# Routes
@app.route("/api", methods = ["GET"])
def documentation():
    return redirect(url_for("api_intro"))

@app.route("/api/intro", methods = ["GET"])
def api_intro():
    return render_template("api/pages/intro.html"), 200

@app.route("/api/generation", methods = ["GET"])
def api_generation():
    return render_template("api/pages/generation.html"), 200

@app.route("/api/oauth2", methods = ["GET"])
def api_oauth2():
    return render_template("api/pages/oauth2.html"), 200

@app.route("/api/keys", methods = ["GET"])
def api_keys():
    return render_template("api/pages/keys.html"), 200

@app.route("/api/misc", methods = ["GET"])
def api_misc():
    return render_template("api/pages/misc.html"), 200

# API Routes
@app.route("/api/oauth", methods = ["GET"])
def login_api():

    redir = request.args.get("redir")

    if not redir:
        return jsonify(
            code = 400,
            data = {"message": "No redirection URL specified."}
        ), 400

    elif "username" not in session:
        app.core.set_redirect("login_api", args = {"redir": redir})
        return redirect(url_for("login"))

    code = app.db.get_token(session["username"])
    return render_template(
        "api/ext/oauth.html",
        url = redir,
        code = code
    ), 200

@app.route("/api/user", methods = ["GET"])
def userInformation():

    auth = request.args.get("auth", request.args.get("code"))

    if not auth:
        return jsonify(
            code = 400,
            data = {"message": "No authorization code provided with request."}
        ), 400

    user = app.db.get_user_by_token(auth)
    if not user:
        return jsonify(
            code = 403,
            data = {"message": "The provided authorization is invalid."}
        ), 403

    return jsonify(
        code = 200,
        data = {
            "username": user[0],
            "signupDate": user[2]
        }
    ), 200

@app.route("/api/auth", methods = ["POST"])
def authenticateUser():

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify(code = 400, data = {"message": "Username/password missing from request."}), 400

    elif not app.db.user_exists(username):
        return jsonify(code = 403, data = {"message": "The specified username does not exist."}), 403

    elif not app.db.checkpw(username, password):
        return jsonify(code = 403, data = {"message": "The specified password is invalid."}), 403

    return jsonify(code = 200, data = {"message": "200 OK"}), 200

@app.route("/api/search", methods = ["GET"])
def search_youtube():

    # API key
    key = request.args.get("key")
    if key not in API_KEYS:
        return jsonify(code = 403, data = {"message": "Invalid API key provided."}), 403

    # Locate query
    query = request.args.get("query")
    if query is None:
        return jsonify(code = 400, data = {"message": "No query was specified to search for."}), 400

    # Locate our count
    count = request.args.get("count", 10)
    try:
        count = int(count)
        if count > 100:
            return jsonify(code = 400, data = {"message": "Maximum result size is 100."}), 400

        elif count < 1:
            return jsonify(code = 400, data = {"message": "The provided count must be at least 1."}), 400

    except ValueError:
        return jsonify(code = 400, data = {"message": "The provided count is invalid."}), 400

    # Fetch our page as well
    page = request.args.get("page", 1)
    try:
        page = int(page)

        if page < 1:
            return jsonify(code = 400, data = {"message": "Page number should be at least 1."}), 400

    except ValueError:
        return jsonify(code = 400, data = {"message": "Provded page number is not a valid integer."}), 400

    start = datetime.now()

    # Check for a playlist
    results = None
    if fnmatch(query, "*://www.youtube.com/playlist?list=*"):\

        playlist_id = query.split("?list=")[1]
        if "&" in playlist_id:
            playlist_id = playlist_id.split("&")[0]

        results = [{"url": query, "id": playlist_id, "isPlaylist": True}]

    # Search youtube
    if results is None:
        resp = YoutubeSearch(query, max_results = count, page = page).to_dict()
        results = []

        for r in resp:
            results.append({"title": r["title"], "id": r["id"], "url": "https://youtube.com" + r["url_suffix"], "isPlaylist": False})

    # Format response
    data = {
        "results": results,
        "elapsed": round((datetime.now() - start).total_seconds() * 1000)
    }

    return dumps(data), 200

@app.route("/api/emoji", methods = ["GET"])
def convert_emoji():

    # Find emoji
    emoji_ = request.args.get("emoji")
    if emoji_ is None:
        return jsonify(code = 400, data = {"message": "No emoji was specified."}), 400

    # Grab unicode format
    try:
        emoji_ = emoji.emojize(emoji.demojize(emoji_), use_aliases = True)  # Basically a triple check

        # Grab unicode
        unicode = emoji_.encode("unicode_escape").decode("utf-8").lower()
        unicode = unicode[2:]

        unicode = unicode.replace("000", "")

        # Make request
        url = f"https://twemoji.maxcdn.com/v/12.1.4/72x72/{unicode}.png"
        r = requests.get(url)
        if r.status_code != 200:
            raise ValueError  # No such emoji

    except (ValueError, IndexError, UnicodeError):
        return jsonify(code = 400, data = {"message": "Invalid emoji provided."}), 400

    # Return response
    return Response(r.content, mimetype = "image/png"), 200


# CLI routes
@app.route("/api/cli/heartbeat", methods = ["GET"])
def cli_heartbeat():

    # Grab UTC timestamp
    ts = request.args.get("ts")
    if ts is None:
        return jsonify(code = 400, data = {"message": "No timestamp provided."})

    # Check timestamp
    try:
        ts = float(ts)

    except ValueError:
        return jsonify(code = 400, data = {"message": "Invalid UTC timestamp provided."})

    # Grab difference
    current_utc = time.time()
    ts_diff = round((current_utc - ts) * 1000, 2)

    return jsonify(code = 200, ping = ts_diff), 200

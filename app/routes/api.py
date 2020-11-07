# Modules
from app import app
from os import getenv

from requests import get
from app.database import DB

from urllib.parse import urlparse
from flask import render_template, redirect, url_for, jsonify, request, abort, session

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

# API Routes
@app.route("/api/v1/weather", methods = ["GET"])
def getweather():

  lon = request.args.get("lon")

  lat = request.args.get("lat")

  if not lon or not lat:

    abort(400)

  w = get_weather(lon, lat)

  return str(w), 200 if "code" not in dict(w) else dict(w)["code"]

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

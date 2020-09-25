# Modules
from app import app
from flask import render_template, request, abort

# Routes
@app.route("/upload", methods = ["GET"])
def upload():

  return render_template(
    "uploading/dashboard.html",
    request = request
  ), 200

@app.route("/upload/cli/ping", methods = ["GET"])
def cli_ping():

  return "200 OK", 200

@app.route("/upload/cli/project", methods = ["POST"])
def cli_getproject():

  username = request.form.get("username")

  project = request.form.get("name")

  if not username or not project:

    return abort(400)

  return abort(403)  # temporary

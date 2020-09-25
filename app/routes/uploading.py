# Modules
from app import app
from flask import render_template, request

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

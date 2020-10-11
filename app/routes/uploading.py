# Modules
from app import app
from flask import render_template, request, abort

# Routes
@app.route("/cli/download", methods = ["GET"])
def download():

  file_paths = {
    "windows": "iipython_win64.exe"
  }

  icons = {
    "windows": "fab fa-windows"
  }

  filepath = file_paths[request.user_agent.platform] if request.user_agent.platform in file_paths else file_paths["windows"]
  icon = icons[request.user_agent.platform] if request.user_agent.platform in icons else icons["windows"]

  return render_template("pages/download.html", path = filepath, icon = icon), 200

@app.route("/cli/ping", methods = ["GET"])
def cli_ping():

  return "200 OK", 200

# Modules
from app import app
from flask import render_template

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

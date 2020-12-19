# Modules
from app import app
from flask import send_from_directory

# Routes
@app.route("/s/<path:path>")
def staticfile(path):
    return send_from_directory("app/static", path, conditional = True)

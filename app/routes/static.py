# Modules
from app import app
from os import listdir
from flask import send_from_directory, abort

# Routes
@app.route("/s/<string:file>")
def staticfile(file):

    if file not in listdir("app/static"):

        return abort(400)

    return send_from_directory("app/static", file)

@app.route("/s/<string:dir>/<string:file>")
def staticfilefromdir(dir, file):

    if dir not in listdir("app/static"):

        return abort(400)

    elif file not in listdir(f"app/static/{dir}"):

        return abort(400)

    return send_from_directory(f"app/static/{dir}", file)

@app.route("/s/<string:dir>/<string:dir2>/<string:file>")
def staticfilefromtwodirs(dir, dir2, file):

    if dir not in listdir("app/static"):

        return abort(400)

    elif dir2 not in listdir(f"app/static/{dir}"):

        return abort(400)

    elif file not in listdir(f"app/static/{dir}/{dir2}"):

        return abort(400)

    return send_from_directory(f"app/static/{dir}/{dir2}", file)

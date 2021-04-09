# Modules
import string
import random

from app import app
from os import listdir

from werkzeug.urls import url_parse
from flask import (
    send_from_directory, render_template, abort, request,
    redirect, url_for
)

# Routes
@app.route("/s/<path:path>")
def staticfile(path):
    return send_from_directory("app/static", path, conditional = True)

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

    ext = file.filename.split(".")[-1]
    if "." not in file.filename:
        ext = "png"

    id = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    file.save(f"data/files/{id}.{ext}")

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

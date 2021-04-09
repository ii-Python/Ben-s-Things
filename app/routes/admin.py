# Modules
import psutil
import platform

import subprocess
from app import app

from getpass import getuser
from datetime import datetime

from flask import render_template, session, redirect, url_for, request, abort, jsonify

# Shutdown server
def shutdown_server():

    # taken from https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug server")

    func()

# Routes
@app.route("/admin")
def admin_page():

    if "username" not in session or not app.db.is_admin(session["username"]):
        return redirect(url_for("index"))

    # Grab OS info
    memory = psutil.virtual_memory()
    memory = {
        "used": round(memory.used / 1073741824, 2),
        "max": round(memory.total / 1073741824, 2),
        "percent": round(memory.percent)
    }

    cpu_percents = psutil.cpu_percent(percpu = True)

    # Grab git version
    try:
        git_version = subprocess.run(["git", "--version"], stdout = subprocess.PIPE).stdout.decode("utf-8")

    except OSError:
        git_version = "not installed"

    return render_template(
        "admin/index.html",

        # System stats
        ram = memory,
        cpu_percent = round(psutil.cpu_percent()),
        cpu_length = 100 / len(cpu_percents),
        cpu_percents = cpu_percents,

        # Misc information
        python_version = platform.python_version(),
        git_version = git_version,
        current_user = getuser(),
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%D %I:%M:%S %p")
    ), 200

@app.route("/admin/update")
def git_pull():

    if "username" not in session or not app.db.is_admin(session["username"]):
        return redirect(url_for("index"))

    subprocess.run(["git", "pull", "origin", "master"])

    return redirect(url_for("admin_page"))

@app.route("/admin/shutdown")
def shutdown():

    if "username" not in session or not app.db.is_admin(session["username"]):
        return redirect(url_for("index"))

    shutdown_server()

    return "Server is shutting down.", 200

@app.route("/admin/terminal")
def open_terminal():

    if "username" not in session or not app.db.is_admin(session["username"]):
        return redirect(url_for("index"))

    return render_template(
        "admin/terminal.html",
        user = getuser(),
        host = platform.node()
    ), 200

@app.route("/admin/execute", methods = ["POST"])
def execute_command():

    if "username" not in session or not app.db.is_admin(session["username"]):
        return redirect(url_for("index"))

    command = request.form.get("command")
    output = ""

    if command:
        try:
            out = subprocess.run(command.split(" "), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            if out.stdout:
                output += out.stdout.decode("utf-8")

            if out.stderr:
                if output:
                    output += "\n"
                output += out.stderr.decode("utf-8")

        except FileNotFoundError:
            output = f"bash: {command.split(' ')[0]}: command not found"  # Just like the old days

    # Formatting
    formats = {
        "\n": "<br>",
        "\t": "    "
    }
    for format in formats:
        output = output.replace(format, formats[format])

    # Send back to terminal
    return jsonify(output = output), 200

# Modules
import subprocess
from app import app
from flask import render_template, session, redirect, url_for, request

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

    return render_template("admin/index.html"), 200

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

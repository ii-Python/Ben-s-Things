# Modules
import secrets
from app import app

from app.database import DB
from flask import render_template, session, request, abort, redirect, url_for, make_response

# Routes
@app.route("/account")
@app.route("/account/")
def account():

    if "username" not in session:
        app.core.set_redirect("account")
        return redirect(url_for("login"))

    return render_template("account/account.html"), 200

@app.route("/login", methods = ["GET", "POST"])
def login():

    if request.method == "GET":

        if "username" in session:
            return redirect(url_for("index"))

        return render_template("pages/login.html"), 200

    username = request.form.get("id")
    password = request.form.get("password")

    if not username or not password:
        return render_template(
            "pages/login.html",
            error = "Please fill out all fields."
        ), 400

    db = DB()

    if not db.user_exists(username):

        return render_template(
            "pages/login.html",
            error = "No records match that username."
        ), 400

    elif not db.checkpw(username, password):

        return render_template(
            "pages/login.html",
            error = "Invalid password."
        ), 403

    db.close()

    session["username"] = username

    if "redirect" in session:
        redir = session["redirect"]
        del session["redirect"]
        return redirect(url_for(redir["endpoint"], **redir["args"]))

    return redirect(url_for("index"))

@app.route("/register", methods = ["GET", "POST"])
def register():

    if request.method == "GET":

        if "username" in session:

            return redirect(url_for("index"))

        return render_template("pages/register.html"), 200

    username = request.form.get("id")
    password = request.form.get("password")

    if request.args.get("redir"):
        session["redir"] = request.args.get("redir")

    if not username or not password:

        return render_template(
            "pages/register.html",
            error = "Please fill out all fields."
        ), 400

    elif len(password) < 6:

        return render_template(
            "pages/register.html",
            error = "Password needs to be at least 6 characters."
        ), 400

    db = DB()

    if db.user_exists(username):

        return render_template(
            "pages/register.html",
            error = "The specified username is already taken."
        ), 400

    db.register(username, password)
    db.close()

    session["username"] = username
    return redirect(url_for("index"))

@app.route("/logout")
def logout():

    if "username" in session:
        del session["username"]

    return redirect(url_for("index"))

@app.route("/account/delete", methods = ["GET", "POST"])
def delete_account():

    if "username" not in session:
        return redirect(url_for("login"))

    elif request.method == "POST":

        db = DB()
        db.delete_user(session["username"])
        db.close()

        return redirect(url_for("logout"))

    return render_template("account/delete.html"), 200

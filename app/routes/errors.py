# Modules
from app import app
from flask import render_template

# Errors
@app.errorhandler(400)
def error400(e):
    return render_template("errors/400.html"), 400

@app.errorhandler(403)
def error403(e):
    return render_template("errors/403.html"), 403

@app.errorhandler(404)
def error404(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def error500(e):
    return render_template("errors/500.html"), 500

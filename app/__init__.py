# Modules
import psutil
import logging

from os import getenv
from .core import Core

from flask import Flask
from .database import DB

from flask_gzip import Gzip
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Initialization
app = Flask(
    "Ben's Things",
    template_folder = "app/templates"
)

app.secret_key = getenv("SECRET_KEY")

app.db = DB()
app.core = Core()

# Global app context for Jinja
@app.context_processor
def inject_globals():

    globals = {
        "app": app,
        "db": app.db,
        "core": app.core,
        "psutil": psutil
    }
    return globals

# Compressing / GZip
Gzip(app)

# Gunicorn / WSGI Initialization
application = app

# Logging
logging.getLogger("werkzeug").setLevel(logging.ERROR)

# Routes
from app.routes import (
    public, static, generators,
    api, account, errors, admin
)

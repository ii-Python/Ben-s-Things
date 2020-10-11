# Modules
from os import getenv
from flask import Flask

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

# Compressing / GZip
Gzip(app)

# Gunicorn / WSGI Initialization
application = app

# Routes
from app.routes import public, static, generators, api, account, errors, uploading

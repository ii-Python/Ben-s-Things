# Modules
from os import urandom
from flask import Flask

from dotenv import load_dotenv
from flask_compress import Compress

# Load .env
load_dotenv()

# Initialization
app = Flask(
  "Ben's Things",
  template_folder = "app/templates"
)

app.secret_key = urandom(26)

# Compressing / GZip
Compress(app)

# Gunicorn / WSGI Initialization
application = app

# Routes
from app.routes import public, static, generators, api, account, errors

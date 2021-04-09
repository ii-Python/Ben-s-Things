# Modules
import string
import random

import sqlite3
import hashlib

from os import mkdir
from os.path import exists

# Initialization
if not exists("data"):
    mkdir("data")

if not exists("data/files"):
    mkdir("data/files")

conn = sqlite3.connect("data/login.db")
cursor = conn.cursor()

# Setup tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username text,
    password text,
    signup text,
    token text,
    admin bool,
    userid long
)
""")

# Save
conn.commit()
conn.close()

# Create our URL database too
open("data/urls.json", "w+").write("{}")
open("data/keys.json", "w+").write("[]")

# Setup our .env file
ip_info = input("IPInfo.io API Key: ")
openweather = input("OWM API Key: ")

secret_key = hashlib.sha256("".join(random.choice(string.ascii_letters) for _ in range(24)).encode("UTF-8")).hexdigest()

open(".env", "w+").write(f"""IPINFO = "{ip_info}"
OPENWEATHER = "{openweather}"
SECRET_KEY = "{secret_key}"
""")

# Just a quick program I made to setup the database
# This helps if I want to wipe the database

# Modules
import sqlite3
from os import mkdir
from os.path import exists

# Initialization
if not exists("data"):

    mkdir("data")

if not exists("data/images"):

    mkdir("data/images")

conn = sqlite3.connect("data/login.db")
cursor = conn.cursor()

# Setup tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username text,
    password text,
    email text,
    signup text,
    token text
)
""")

# Save
conn.commit()

conn.close()

# Create our URL database too
open("data/urls.json", "w+").write("{}")

# Just a quick program I made to setup the database
# This helps if I want to wipe the database

# Modules
import sqlite3

# Initialization
conn = sqlite3.connect("login.db")
cursor = conn.cursor()

# Setup tables
cursor.execute("CREATE TABLE users (username text, password text, signup text)")

# Save
conn.commit()

conn.close()

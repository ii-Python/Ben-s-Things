# Modules
import bcrypt
import secrets

import sqlite3
from hashlib import sha256

from datetime import datetime

# Class
class DB():

    def __init__(self):

        self.conn = sqlite3.connect("data/login.db")
        self.cursor = self.conn.cursor()

    def user_exists(self, username):

        for row in self.cursor.execute("SELECT * FROM users"):

            if row[0].lower() == username.lower():

                return True

        return False

    def get_user_by_token(self, cipher):

        for row in self.cursor.execute("SELECT * FROM users"):

            if row[3] == cipher:

                return row

        return None

    def delete_user(self, username):

        self.cursor.execute("DELETE FROM users WHERE username=?", (username,))

    def register(self, username, password):

        hashed = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())

        token = secrets.token_urlsafe(75)

        self.cursor.execute("INSERT INTO users VALUES (?,?,?,?)", (username, hashed.decode("UTF-8"), datetime.now().strftime("%D"), token))

    def checkpw(self, username, password):

        for row in self.cursor.execute("SELECT * FROM users"):

            if row[0].lower() == username.lower():

                act_pw = row[1].encode("UTF-8")

                password = password.encode("UTF-8")

                if bcrypt.checkpw(password, act_pw):

                    return True

                break

        return False

    def gethash(self, username):

        for row in self.cursor.execute("SELECT * FROM users"):

            if row[0].lower() == username.lower():

                return row[1]

        return None

    def get_token(self, username):

        for row in self.cursor.execute("SELECT * FROM users"):

            if row[0].lower() == username.lower():

                return row[3]

        return None

    def close(self):

        self.conn.commit()

        self.conn.close()

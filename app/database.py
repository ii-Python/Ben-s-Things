# Modules
import bcrypt
import secrets

import sqlite3
from hashlib import sha256

from datetime import datetime

# Class
class DB():

    def __init__(self):
        self.load_db()

    def load_db(self):
        self.conn = sqlite3.connect("data/login.db", check_same_thread = False)
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

    def get_users(self):

        users = []
        for row in self.cursor.execute("SELECT * FROM users"):
            users.append(row)

        return users

    def delete_user(self, username):

        self.cursor.execute("DELETE FROM users WHERE username=?", (username,))
        self.save()

    def register(self, username, password):

        hashed = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
        token = secrets.token_urlsafe(75)

        admin = False
        if not self.get_users():
            admin = True

        self.cursor.execute("INSERT INTO users VALUES (?,?,?,?,?)", (username, hashed.decode("UTF-8"), datetime.now().strftime("%D"), token, admin))
        self.save()

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

    def is_admin(self, username):

        for row in self.cursor.execute("SELECT * FROM users"):
            if row[0] == username:
                return row[4] == 1

        return False  # Fallback

    def save(self):
        self.close()
        self.load_db()

    def close(self):
        self.conn.commit()
        self.conn.close()

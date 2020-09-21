# Modules
import bcrypt
import sqlite3

from hashlib import sha256
from datetime import datetime

# Class
class DB():

    def __init__(self):

        self.conn = sqlite3.connect("login.db")
        self.cursor = self.conn.cursor()

    def user_exists(self, username):

        for row in self.cursor.execute("SELECT * FROM users"):

            if row[0].lower() == username.lower():

                return True

        return False

    def get_user_by_sha256(self, cipher):

        for row in self.cursor.execute("SELECT * FROM users"):

            realcipher = sha256(row[1].encode("UTF-8")).hexdigest()

            if realcipher == cipher:

                return row

        return None

    def delete_user(self, username):

        self.cursor.execute("DELETE FROM users WHERE username=?", (username,))

    def register(self, username, password):

        hashed = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())

        self.cursor.execute("INSERT INTO users VALUES (?,?,?)", (username, hashed.decode("UTF-8"), datetime.now().strftime("%D")))

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

    def close(self):

        self.conn.commit()

        self.conn.close()

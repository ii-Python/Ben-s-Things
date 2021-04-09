# Modules
import secrets
import sqlite3
from hashlib import sha512
from datetime import datetime

# Main database class
class DB(object):

    def __init__(self) -> None:
        self.conn = None
        self.cursor = None

        self.load_db()

    def load_db(self) -> None:
        self.conn = sqlite3.connect("data/login.db", check_same_thread = False)
        self.cursor = self.conn.cursor()

    def user_exists(self, username) -> bool:
        for row in self.cursor.execute("SELECT * FROM users"):
            if row[0].lower() == username.lower():
                return True

        return False  # Fallback

    def get_user_by_token(self, cipher):
        for row in self.cursor.execute("SELECT * FROM users"):
            if row[3] == cipher:
                return row

        return None  # Fallback

    def get_user_by_username(self, username):
        for row in self.cursor.execute("SELECT * FROM users"):
            if row[0] == username:
                return row

        return None  # Fallback

    def get_users(self) -> list:
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def delete_user(self, username) -> None:
        self.cursor.execute("DELETE FROM users WHERE username=?", (username,))
        self.save()

    def register(self, username, password) -> None:

        # Create some data
        hashed = sha512(password.encode("UTF-8")).hexdigest()
        token = secrets.token_urlsafe(75)

        # Create user
        self.cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", (username, hashed, datetime.now(), token, False, len(self.get_users()) + 1))
        self.save()

    def checkpw(self, username, password) -> bool:
        for row in self.cursor.execute("SELECT * FROM users"):
            if row[0] == username:

                act_pw = row[1]
                password = sha512(password.encode("UTF-8")).hexdigest()

                if password == act_pw:
                    return True  # Correct password

                break

        return False  # Fallback

    def get_pw_hash(self, username):
        for row in self.cursor.execute("SELECT * FROM users"):
            if row[0] == username:
                return row[1]  # SHA512 hashed password string

        return None  # No such user

    def get_token(self, username):
        for row in self.cursor.execute("SELECT * FROM users"):
            if row[0] == username:
                return row[3]  # secrets.url_safe token

        return None  # No such user

    def is_admin(self, username) -> bool:
        for row in self.cursor.execute("SELECT * FROM users"):
            if row[0] == username:
                return row[4] == 1

        return False  # Fallback

    def save(self) -> None:
        self.close()
        self.load_db()

    def close(self) -> None:
        self.conn.commit()
        self.conn.close()

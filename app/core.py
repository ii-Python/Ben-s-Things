# Modules
from os import getenv
from requests import get
from flask import session

# Master class
class Core(object):

    def __init__(self):
        self.weather = "https://api.openweathermap.org/data/2.5/onecall?"

    def get_weather(self, lon, lat):

        """Fetches current weather information"""

        resp = get(f"{self.weather}lat={lat}&lon={lon}&exclude=hourly,daily&appid={getenv('OPENWEATHER')}").json()

        if "current" not in resp:

            return None

        current = resp["current"]

        return current

    def set_redirect(self, endpoint, args = {}):

        """Sets a system redirect for a user, redirecting them after authentication"""

        if "redirect" in session:

            del session["redirect"]

        session["redirect"] = {
            "endpoint": endpoint,
            "args": args
        }

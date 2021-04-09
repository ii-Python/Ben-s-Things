# Modules
from app import app
from sys import argv

try:
    from waitress import serve

except ImportError:
    print("Missing waitress, falling back to flask server.")
    serve = None

# Run
opts = {
    "host": "0.0.0.0",
    "port": 5000
}
if serve is not None and "--debug" not in argv:
    serve(app, **opts)

else:
    app.run(**opts, debug = True)

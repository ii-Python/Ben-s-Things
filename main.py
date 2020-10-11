# Modules
from app import app
from sys import argv
from waitress import serve

# Run
if "--debug" in argv:

    app.run(host = "0.0.0.0", port = 5000, debug = True)

else:

    serve(app, host = "0.0.0.0", port = 5000)

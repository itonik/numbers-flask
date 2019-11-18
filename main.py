#!/usr/bin/env python3
from flask import Flask
from view import view
from api import api
from static import static
import webbrowser

app = Flask(__name__)

# Blueprints
app.register_blueprint(view)
app.register_blueprint(api)
app.register_blueprint(static)

if (__name__) == "__main__":
    # webbrowser.open_new('localhost:5000')
    app.run(host="0.0.0.0", port=5000, debug=True)
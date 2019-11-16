#!/usr/bin/env python3
from flask import Flask
from view import view
from api import api
from static import static

app = Flask(__name__)

# Blueprints
app.register_blueprint(view)
app.register_blueprint(api)
app.register_blueprint(static)

if (__name__) == "__main__":
    app.run(debug=True)
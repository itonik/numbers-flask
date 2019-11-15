#!/usr/bin/env python3
from flask import Flask
from index import index_page
from api import api_blueprint

app = Flask(__name__)

# Blueprints
app.register_blueprint(index_page)
app.register_blueprint(api_blueprint)

if (__name__) == "__main__":
    app.run()
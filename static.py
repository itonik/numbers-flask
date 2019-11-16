from flask import Blueprint, send_from_directory

static = Blueprint('static', __name__)

@static.route('/uploads/<file>')
def uploads(file):
    return send_from_directory('uploads', file)

@static.route('/intermediate/<file>')
def intermediate(file):
    return send_from_directory('intermediate', file)
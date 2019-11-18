from flask import Blueprint, send_from_directory, send_file
from api_utils import make_qr

static = Blueprint('static', __name__)

@static.route('/uploads/<file>')
def uploads(file):
    return send_from_directory('uploads', file)

@static.route('/intermediate/<file>')
def intermediate(file):
    return send_from_directory('intermediate', file)

@static.route('/qr.png')
def qr():
    make_qr()
    return send_file('qr_last.png')
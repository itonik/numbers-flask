from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# This file contains frontend templates logi

index_page = Blueprint('static', __name__, template_folder='templates')

@index_page.route('/')
def index():
    return render_template('index.html')
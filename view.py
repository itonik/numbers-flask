from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from api_utils import get_files_in_directory
from model import process_image

# This file contains frontend templates logiс

view = Blueprint('view', __name__, template_folder='templates')

@view.route('/')
def index():
    return render_template('index.html',files=get_files_in_directory())

@view.route('/file/<filename>')
def file_processor(filename):
    filtered_image_name, segment_image_names, recognition_results = process_image(filename)
    # TODO: Debug is here!
    return render_template(
        'processor.html',
        filename=filename,
        filtered_image_name=filename,
        #segments_and_results=zip(segment_image_names, recognition_results)
        segments_and_results=zip([filename] * 7, list(range(7)))
    )
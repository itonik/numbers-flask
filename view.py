from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from api_utils import get_files_in_directory
from model import process_image
from api_utils import get_local_ip

# This file contains frontend templates logiс

view = Blueprint('view', __name__, template_folder='templates')

@view.route('/')
def index():
    return render_template('index.html',files=get_files_in_directory())

@view.route('/file/<filename>')
def file_processor(filename):
    res = process_image(filename)
    # TODO: Debug is here!
    return render_template(
        'processor.html',
        filename=res.source,
        filtered_image_name=res.filter,
        contours_image_name=res.contour,
        #segments_and_results=zip(segment_image_names, recognition_results)
        segments_and_results=zip(res.segments, res.recognition)
    )
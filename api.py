import os
from flask import Blueprint, flash, request, redirect, url_for
from api_utils import fancy_filename

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/file', methods=['POST'])
def file_receiver():
    # Checking if file is attached
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    # Making file object
    file = request.files['file']
    # Extra check
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    filename = fancy_filename(file.filename)
    file.save(os.path.join('uploads', filename))

    # In the future should return redirect
    return 'OK', 200

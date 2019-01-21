from os import listdir, remove
from os.path import join
from flask import url_for, current_app
from modules import app
from werkzeug.utils import secure_filename



uploadpath = app.config['UPLOAD_FOLDER']


def save_file(fileobject):
    filename = fileobject.filename
    ext = filename.split('.')[-1]
    filename_without = filename.split('.')[0]
    if filename in listdir(app.config['UPLOAD_FOLDER']):
        filename_without += "_copy"
    newname = secure_filename(filename_without + "." + ext)
    fileobject.save(join(app.config['UPLOAD_FOLDER'], newname))
    return newname


def delete_file(filename):
    remove(join(app.config['UPLOAD_FOLDER'], filename))

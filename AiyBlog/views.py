import os

from flask import Blueprint,send_file,safe_join,abort,render_template
from flask import current_app as app
views = Blueprint("views",__name__)

'''
This is user interface

'''

@views.route('/index')
@views.route('/')
def index():
    """

    """
    return render_template('test.html')




@views.route('/themes/<theme>/static/<path:path>')
def themes_handler(theme, path):
    filename = safe_join(app.root_path, 'themes', theme, 'static', path)
    if os.path.isfile(filename):
        return send_file(filename)
    else:
        abort(404)

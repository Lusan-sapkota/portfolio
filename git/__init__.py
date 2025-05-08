from flask import Blueprint

git_bp = Blueprint('git', __name__, template_folder='templates', 
                   static_folder='static', static_url_path='/git/static')

from . import routes
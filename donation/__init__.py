from flask import Blueprint

git_bp = Blueprint('donation', __name__, template_folder='templates', 
                   static_folder='static', static_url_path='/donation/static')

from . import routes
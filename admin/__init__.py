from flask import Blueprint

# Define the blueprint and its URL prefix
admin_bp = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin', static_folder='static', static_url_path='/admin/static')

# Import routes to associate them with this blueprint
from . import routes
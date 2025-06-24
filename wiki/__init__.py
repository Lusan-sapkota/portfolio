from flask import Blueprint

# Define the blueprint
wiki_bp = Blueprint('wiki', __name__, template_folder='templates',
                    static_folder='static')

# Import routes to associate them with this blueprint
from . import routes
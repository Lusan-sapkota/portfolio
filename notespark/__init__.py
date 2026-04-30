from flask import Blueprint

notespark_bp = Blueprint('notespark', __name__, template_folder='templates', 
                   static_folder='static')

from . import routes
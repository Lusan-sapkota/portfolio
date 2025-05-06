from flask import Blueprint, render_template

wiki_bp = Blueprint('wiki', __name__, template_folder='templates')

@wiki_bp.route('/')
def index():
    return render_template('wiki/index.html')
from flask import Blueprint, render_template, redirect

gitea_bp = Blueprint('gitea', __name__, template_folder='templates')

@gitea_bp.route('/')
def index():
    # For now, just show a placeholder page
    # Later you might integrate with Gitea API or proxy to a Gitea instance
    return render_template('gitea/index.html')
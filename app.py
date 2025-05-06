import os
from flask import Flask, render_template
from admin.routes import admin_bp
from wiki.routes import wiki_bp
from gitea.routes import gitea_bp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure app
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
if os.getenv('SERVER_NAME'):
    app.config['SERVER_NAME'] = os.getenv('SERVER_NAME')  # For subdomain support
debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'

# Register blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
if os.getenv('SERVER_NAME'):
    app.register_blueprint(wiki_bp, subdomain='wiki')
    app.register_blueprint(gitea_bp, subdomain='git')
else:
    # For local development without subdomains
    app.register_blueprint(wiki_bp, url_prefix='/wiki')
    app.register_blueprint(gitea_bp, url_prefix='/git')

# Main routes
@app.route('/')
def index():
    return render_template('index.html')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Use environment variable for host and port if provided
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port, debug=debug_mode)

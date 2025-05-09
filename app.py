import os
from flask import Flask, render_template, jsonify 
from dotenv import load_dotenv
from database import db
import commands
from flask_login import LoginManager
from models import User
from flask_jwt_extended import JWTManager 
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure app
app.secret_key = os.getenv('SECRET_KEY') # Used by Flask-Login, can also be JWT_SECRET_KEY
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', app.secret_key) # Added: Use a dedicated JWT secret key
jwt = JWTManager(app) # Added

if os.getenv('SERVER_NAME'):
    app.config['SERVER_NAME'] = os.getenv('SERVER_NAME')  

# Database configuration
database_url = os.getenv('DATABASE_URL')
if database_url:
    # Fix any potentially escaped characters in the URL
    database_url = database_url.replace('\\x3a', ':')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'  # Fallback to SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# Setup Flask-Login (can co-exist if other parts of app use it)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
print(f"DEBUG env var: {os.getenv('DEBUG')}") 
print(f"debug_mode value: {debug_mode}")

# Import blueprints - AFTER app creation and extension initialization
from admin import admin_bp
from wiki import wiki_bp
from git import git_bp

# Register blueprints
app.register_blueprint(admin_bp) # url_prefix is set in admin_bp definition

server_name_env = os.getenv('SERVER_NAME')
print(f"DEBUG: SERVER_NAME environment variable is: '{server_name_env}'") # Crucial check

if server_name_env:
    print("DEBUG: Registering wiki and git with subdomains.")
    app.register_blueprint(wiki_bp, subdomain='wiki')
    app.register_blueprint(git_bp, subdomain='git')
else:
    print("DEBUG: Registering wiki and git with URL prefixes for local development.")
    app.register_blueprint(wiki_bp, url_prefix='/wiki')
    app.register_blueprint(git_bp, url_prefix='/git')

# Import models here (after db initialization)
from models import *

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

commands.register_commands(app)

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        
    # Use environment variable for host and port if provided
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port, debug=debug_mode)

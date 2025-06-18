import os
from flask import Flask, render_template, jsonify, abort, request
from dotenv import load_dotenv
from database import db
import commands
from flask_login import LoginManager
from models import User
from flask_jwt_extended import JWTManager 
from flask_migrate import Migrate
from config import SUBDOMAINS, THEME_CONFIG, SEO_CONFIG, CONTACT_INFO, FEATURES
from datetime import datetime
from github_service import github_service
import traceback

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

# Initialize GitHub service with caching
github_service.init_cache(app)

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
from donation import donation_bp

# Register blueprints
app.register_blueprint(admin_bp) # url_prefix is set in admin_bp definition

server_name_env = os.getenv('SERVER_NAME')
print(f"DEBUG: SERVER_NAME environment variable is: '{server_name_env}'") # Crucial check

if server_name_env:
    print("DEBUG: Registering wiki, git, and donation with subdomains.")
    app.register_blueprint(wiki_bp, subdomain='wiki')
    app.register_blueprint(git_bp, subdomain='git')
    app.register_blueprint(donation_bp, subdomain='donation')
else:
    print("DEBUG: Registering wiki, git, and donation with URL prefixes for local development.")
    app.register_blueprint(wiki_bp, url_prefix='/wiki')
    app.register_blueprint(git_bp, url_prefix='/git')
    app.register_blueprint(donation_bp, url_prefix='/donation')

# Import models here (after db initialization)
from models import *

# Main routes
@app.route('/')
def index():
    # Pass configuration data to template
    template_data = {
        'subdomains': {k: v for k, v in SUBDOMAINS.items() if v.get('enabled', True)},
        'theme_config': THEME_CONFIG,
        'seo_config': SEO_CONFIG,
        'contact_info': CONTACT_INFO,
        'features': FEATURES
    }
    return render_template('index.html', **template_data, current_year=datetime.now().year)

@app.route('/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    """Handle newsletter subscription from the main site"""
    try:
        from models import NewsletterSubscriber
        from email_service import email_service
        
        email = request.form.get('email', '').strip().lower()
        interests = request.form.get('interests', '').strip()
        
        if not email:
            return jsonify({'status': 'error', 'message': 'Please provide a valid email address.'})
        
        # Check if already subscribed
        existing = NewsletterSubscriber.query.filter_by(email=email).first()
        if existing:
            if existing.is_active:
                return jsonify({'status': 'info', 'message': 'You are already subscribed to our newsletter.'})
            else:
                existing.is_active = True
                existing.interests = interests or existing.interests
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Your newsletter subscription has been reactivated.'})
        else:
            subscriber = NewsletterSubscriber(
                email=email,
                interests=interests or 'General Updates'
            )
            db.session.add(subscriber)
            db.session.commit()
              # Send welcome email
            try:
                welcome_subject = "Welcome to Lusan's Newsletter!"
                welcome_message = f"""
Hello!

Thank you for subscribing to my newsletter. You'll now receive updates about:
- New projects and open source contributions
- Technical tutorials and insights
- Development tips and best practices
- Community events and opportunities

I'm excited to share my journey with you!

Best regards,
Lusan Sapkota
Full Stack Developer
"""
                
                email_service.send_email(
                    [email], 
                    welcome_subject, 
                    welcome_message
                )
            except Exception as e:
                print(f"Failed to send welcome email: {e}")
            
            return jsonify({'status': 'success', 'message': 'Thank you for subscribing! Check your email for confirmation.'})
        
    except Exception as e:
        print(f"Newsletter subscription error: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while subscribing. Please try again.'})

@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html')

@app.route('/simulate-error/<int:code>')
def simulate_error(code):
    """
    Route to simulate various HTTP error codes for testing
    Accessible only in development mode
    """
    if not app.debug:
        abort(404)  # Only allow in debug mode
        
    valid_codes = [400, 401, 403, 404, 418, 429, 500, 502, 503]
    
    if code in valid_codes:
        abort(code)
    else:
        return f"<h1>Invalid error code</h1><p>Please use one of these: {', '.join(map(str, valid_codes))}</p>"

# Error handlers
@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html', current_year=datetime.now().year), 400

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html', current_year=datetime.now().year), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', current_year=datetime.now().year), 404

@app.errorhandler(429)
def too_many_requests(e):
    return render_template('429.html', current_year=datetime.now().year), 429

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', current_year=datetime.now().year), 500

@app.errorhandler(502)
def bad_gateway(e):
    return render_template('502.html', current_year=datetime.now().year, current_time=datetime.now().strftime('%H:%M:%S')), 502

@app.errorhandler(503)
def service_unavailable(e):
    return render_template('503.html', current_year=datetime.now().year), 503

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html', current_year=datetime.now().year), 403

@app.errorhandler(418)
def im_a_teapot(e):
    return render_template('418.html', current_year=datetime.now().year), 418

# Add this new handler for general exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all unhandled exceptions"""
    # Log the exception for debugging
    app.logger.error(f'Unhandled exception: {str(e)}', exc_info=True)
    
    # Pass through HTTP exceptions to their specific handlers
    if hasattr(e, 'code'):
        return e
    
    # For development, show the actual error
    if app.debug:
        # Return a simple HTML response with error details
        return f"""
        <h1>Unhandled Exception</h1>
        <h2>{type(e).__name__}: {str(e)}</h2>
        <pre>{traceback.format_exc()}</pre>
        <a href="{url_for('index')}">Return to Home</a>
        """, 500
    
    # For production, show generic 500 error
    return render_template('500.html', current_year=datetime.now().year), 500

commands.register_commands(app)

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        
    # Use environment variable for host and port if provided
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port, debug=debug_mode)

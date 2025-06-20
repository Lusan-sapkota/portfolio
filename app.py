import os
from flask import Flask, render_template, jsonify, abort, request
from dotenv import load_dotenv
from database import db
import commands
from flask_login import LoginManager
from models import User
from flask_jwt_extended import JWTManager 
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import SUBDOMAINS, THEME_CONFIG, SEO_CONFIG, CONTACT_INFO, FEATURES
from datetime import datetime
from github_service import github_service
import traceback
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Add custom Jinja2 filters
@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convert newlines to <br> tags"""
    if not text:
        return text
    from markupsafe import Markup
    return Markup(text.replace('\n', '<br>\n'))

# Configure rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["1000 per hour"]
)

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
    try:
        # Fetch portfolio data from database
        from models import (Project, ProjectCategory, SeoSettings, PersonalInfo, 
                          SocialLink, Skill, Experience, Education, Testimonial)        # Get projects for homepage and all categories
        homepage_projects = Project.query.filter_by(show_on_homepage=True).order_by(Project.created_at.desc()).limit(9).all()
        featured_projects = Project.query.filter_by(is_featured=True).order_by(Project.created_at.desc()).limit(9).all()
        all_projects = Project.query.order_by(Project.created_at.desc()).all()
        project_categories = ProjectCategory.query.all()
        
        # Use homepage projects as primary, fall back to featured, then to first 9
        display_projects = homepage_projects or featured_projects or all_projects[:9]
        
        # Get CMS data
        seo = SeoSettings.query.filter_by(page_name='home').first() or SeoSettings.query.first()
        personal = PersonalInfo.query.first()
        social_links = SocialLink.query.filter_by(is_active=True).order_by(SocialLink.sort_order).all()
        skills = Skill.query.filter_by(is_featured=True).order_by(Skill.sort_order).all()
        experience = Experience.query.order_by(Experience.start_date.desc()).limit(3).all()
        education = Education.query.order_by(Education.start_date.desc()).limit(3).all()
        testimonials = Testimonial.query.filter_by(is_featured=True).order_by(Testimonial.sort_order, Testimonial.created_at.desc()).limit(25).all()
        
        # Pass configuration data to template
        template_data = {
            'subdomains': {k: v for k, v in SUBDOMAINS.items() if v.get('enabled', True)},
            'theme_config': THEME_CONFIG,
            'seo_config': SEO_CONFIG,
            'contact_info': CONTACT_INFO,
            'features': FEATURES,
            'portfolio_projects': display_projects,
            'project_categories': project_categories,
            # CMS data
            'seo': seo,
            'personal': personal,
            'social_links': social_links,
            'skills': skills,
            'experience': experience,
            'education': education,
            'testimonials': testimonials
        }
        return render_template('index.html', **template_data, current_year=datetime.now().year)
    except Exception as e:
        print(f"Error loading portfolio data: {e}")
        # Fallback to template without portfolio data
        template_data = {
            'subdomains': {k: v for k, v in SUBDOMAINS.items() if v.get('enabled', True)},
            'theme_config': THEME_CONFIG,
            'seo_config': SEO_CONFIG,
            'contact_info': CONTACT_INFO,
            'features': FEATURES,
            'portfolio_projects': [],
            'project_categories': []
        }
        return render_template('index.html', **template_data, current_year=datetime.now().year)

@app.route('/newsletter/subscribe', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit: 5 submissions per minute per IP
def newsletter_subscribe():
    """Handle newsletter subscription from the main site with bot protection"""
    try:
        from models import NewsletterSubscriber
        from email_service import email_service
        
        # Get form data
        email = request.form.get('email', '').strip().lower()
        interests = request.form.get('interests', '').strip()
        
        # Basic bot verification - check for honeypot field
        honeypot = request.form.get('website', '')  # Honeypot field
        if honeypot:
            # Bot detected - pretend success but don't actually subscribe
            return jsonify({'status': 'success', 'message': 'Thank you for subscribing!'})
        
        # Enhanced validation
        if not email:
            return jsonify({'status': 'error', 'message': 'Please provide a valid email address.'})
        
        # Email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'status': 'error', 'message': 'Please provide a valid email address.'})
        
        # Check for suspicious patterns (very basic)
        suspicious_patterns = [
            r'test@test\.com',
            r'admin@',
            r'noreply@',
            r'@mailinator\.',
            r'@10minutemail\.',
            r'@guerrillamail\.'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, email, re.IGNORECASE):
                return jsonify({'status': 'error', 'message': 'Please use a valid personal email address.'})
        
        # Check if already subscribed
        existing = NewsletterSubscriber.query.filter_by(email=email).first()
        if existing:
            if existing.is_active:
                return jsonify({'status': 'info', 'message': 'You are already subscribed to my newsletter.'})
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
                welcome_subject = "🌟 Welcome to Lusan's Newsletter!"
                welcome_message = f"""
Dear {email.split('@')[0].capitalize()},

Thanks a lot for signing up — I truly appreciate it!

This newsletter is my little corner of the web where I share what I’ve been working on, what I’m learning, and anything I think might be helpful or interesting to fellow developers like you.

Here’s a quick peek at what you can expect:

🔥 Behind-the-Scenes Project Updates
Get a first look at my latest builds, experiments, and open-source work.

🧠 Practical Tutorials & Dev Notes
I’ll share what I’ve learned — patterns, tips, and real-world lessons that have helped me improve as a developer.

💡 Workflow & Productivity Tips
Occasionally, I’ll drop a few things that have made coding or managing projects smoother for me.

🌱 A Growing Developer Community
You’ll be part of a small but growing space where devs help each other grow — no noise, just value.

🎁 Extra Stuff (When I Can)
From snippets to articles, case studies, or templates — if I build something useful, you’ll get it here first.

That’s it — nothing fancy, no pressure. Just useful, honest content for devs who love to build.

If you ever want to say hi, ask something, or share what you’re working on, feel free to reply — I read every message.

Talk soon,
Lusan
Just a developer, trying to build good things.

https://lusansapkota.com.np
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
        if "rate limit exceeded" in str(e).lower():
            return jsonify({'status': 'error', 'message': 'Too many requests. Please try again in a few minutes.'})
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

@app.route('/contact/submit', methods=['POST'])
@limiter.limit("3 per minute")  # Rate limit: 3 contact form submissions per minute per IP
def contact_submit():
    """Handle contact form submission with auto-reply"""
    try:
        from models import ContactSubmission
        from email_service import email_service
        
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Bot verification - check for honeypot field
        honeypot = request.form.get('botcheck', '')
        if honeypot:
            # Bot detected - pretend success but don't actually process
            return jsonify({'status': 'success', 'message': 'Thank you for your message. I will get back to you soon!'})
        
        # Enhanced validation
        if not name or len(name) < 2:
            return jsonify({'status': 'error', 'message': 'Please provide a valid name.'})
        
        if not email:
            return jsonify({'status': 'error', 'message': 'Please provide a valid email address.'})
        
        if not message or len(message) < 10:
            return jsonify({'status': 'error', 'message': 'Please provide a message with at least 10 characters.'})
        
        # Email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'status': 'error', 'message': 'Please provide a valid email address.'})
        
        # Check for suspicious patterns and spam
        suspicious_patterns = [
            r'viagra|cialis|pharmacy|casino|lottery|winner|congratulations',
            r'crypto|bitcoin|investment|loan|mortgage',
            r'click here|visit now|act now|limited time',
            r'free money|make money|earn \$|guaranteed'
        ]
        
        is_spam = False
        combined_text = f"{name} {email} {subject} {message}".lower()
        
        for pattern in suspicious_patterns:
            if re.search(pattern, combined_text, re.IGNORECASE):
                is_spam = True
                break
        
        # Get client info
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        user_agent = request.headers.get('User-Agent', '')
        
        # Save to database
        contact_submission = ContactSubmission(
            name=name,
            email=email,
            subject=subject or 'Contact Form Submission',
            message=message,
            ip_address=ip_address,
            user_agent=user_agent,
            is_spam=is_spam
        )
        
        db.session.add(contact_submission)
        db.session.commit()
        
        # Send emails only if not spam
        if not is_spam:
            try:
                # Send notification to admin
                email_service.send_contact_notification(name, email, subject, message)
                
                # Send auto-reply to user
                email_service.send_contact_auto_reply(name, email, subject)
                
                # Mark as replied
                contact_submission.is_replied = True
                contact_submission.replied_at = datetime.now()
                db.session.commit()
                
            except Exception as e:
                print(f"Failed to send contact emails: {e}")
        
        return jsonify({
            'status': 'success', 
            'message': 'Thank you for your message! I will get back to you within 24-48 hours.'
        })
        
    except Exception as e:
        print(f"Contact form submission error: {e}")
        if "rate limit exceeded" in str(e).lower():
            return jsonify({'status': 'error', 'message': 'Too many requests. Please try again in a few minutes.'})
        return jsonify({'status': 'error', 'message': 'An error occurred while sending your message. Please try again.'})

@app.route('/newsletter/unsubscribe')
def newsletter_unsubscribe_page():
    """Newsletter unsubscribe page"""
    return render_template('unsubscribe.html', current_year=datetime.now().year)

@app.route('/newsletter/unsubscribe/<token>')
def newsletter_unsubscribe_token(token):
    """Handle newsletter unsubscribe via token"""
    try:
        from models import NewsletterSubscriber
        
        # Decode the token (simple base64 for now, could use JWT for more security)
        import base64
        try:
            email = base64.b64decode(token.encode()).decode()
        except:
            return render_template('unsubscribe.html', 
                                 error="Invalid unsubscribe link", 
                                 current_year=datetime.now().year)
        
        # Find and deactivate subscriber
        subscriber = NewsletterSubscriber.query.filter_by(email=email).first()
        if subscriber:
            subscriber.is_active = False
            db.session.commit()
            return render_template('unsubscribe.html', 
                                 success=f"You have been successfully unsubscribed from the newsletter.", 
                                 current_year=datetime.now().year)
        else:
            return render_template('unsubscribe.html', 
                                 error="Email not found in our subscription list", 
                                 current_year=datetime.now().year)
            
    except Exception as e:
        print(f"Unsubscribe error: {e}")
        return render_template('unsubscribe.html', 
                             error="An error occurred. Please try again.", 
                             current_year=datetime.now().year)

@app.route('/newsletter/unsubscribe/confirm', methods=['POST'])
def newsletter_unsubscribe_confirm():
    """Handle newsletter unsubscribe form submission"""
    try:
        from models import NewsletterSubscriber
        
        email = request.form.get('email', '').strip().lower()
        
        if not email:
            return render_template('unsubscribe.html', 
                                 error="Please provide a valid email address", 
                                 current_year=datetime.now().year)
        
        # Find and deactivate subscriber
        subscriber = NewsletterSubscriber.query.filter_by(email=email).first()
        if subscriber:
            subscriber.is_active = False
            db.session.commit()
            return render_template('unsubscribe.html', 
                                 success=f"You have been successfully unsubscribed from the newsletter.", 
                                 current_year=datetime.now().year)
        else:
            return render_template('unsubscribe.html', 
                                 error="Email not found in our subscription list", 
                                 current_year=datetime.now().year)
            
    except Exception as e:
        print(f"Unsubscribe confirmation error: {e}")
        return render_template('unsubscribe.html', 
                             error="An error occurred. Please try again.", 
                             current_year=datetime.now().year)

commands.register_commands(app)

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        
    # Use environment variable for host and port if provided
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port, debug=debug_mode)

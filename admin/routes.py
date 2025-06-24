from flask import render_template, request, redirect, url_for, flash, jsonify, session, current_app, send_file, make_response
from functools import wraps
from models import (User, Project, ProjectCategory, ContactSubmission, NewsletterSubscriber, 
                   SeoSettings, PersonalInfo, SocialLink, Skill, Experience, Education, Testimonial,
                   DonationProject, Donation, PaymentMethod, ThanksgivingSettings, DonationSettings,
                   WikiArticle, WikiCategory)
from . import admin_bp
from database import db
from datetime import datetime, timedelta
from sqlalchemy import desc
import os
import time
import re
import logging
import json
import csv
import io
import zipfile
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Set up logging
logger = logging.getLogger(__name__)

# Rate limiter for admin routes (use Flask-Limiter decorators)
import time 

def validate_strong_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength with detailed requirements
    Returns (is_valid, error_message)
    """
    if len(password) < 20:
        return False, "Password must be at least 20 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        return False, "Password must contain at least one special character (!@#$%^&*)"
    
    # Check for common patterns
    common_patterns = [
        r'(.)\1{2,}',  # Same character repeated 3+ times
        r'123456789',
        r'abcdefghij',
        r'qwertyuiop',
        r'password',
        r'admin',
        r'lusan',
        r'sapkota'
    ]
    
    for pattern in common_patterns:
        if re.search(pattern, password.lower()):
            return False, "Password contains common patterns or words. Please use a more unique password"
    
    return True, "" 

# Admin required decorator with enhanced security
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        login_time_str = session.get('login_time')
        
        if not user_id or not login_time_str:
            flash('Please log in to access admin area.', 'warning')
            return redirect(url_for('admin.login'))
        
        # Check session timeout (2 hours)
        try:
            login_time = datetime.fromisoformat(login_time_str)
            if datetime.utcnow() - login_time > timedelta(hours=2):
                session.clear()
                flash('Session expired. Please log in again.', 'warning')
                return redirect(url_for('admin.login'))
        except (ValueError, TypeError):
            session.clear()
            flash('Invalid session. Please log in again.', 'warning')
            return redirect(url_for('admin.login'))
        
        # Verify user still exists and is admin
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            session.clear()
            flash('Admin access required.', 'error')
            return redirect(url_for('admin.login'))
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard with overview statistics"""
    stats = {
        'projects': Project.query.count(),
        'categories': ProjectCategory.query.count(),
        'contact_submissions': ContactSubmission.query.count(),
        'newsletter_subscribers': NewsletterSubscriber.query.filter_by(is_active=True).count(),
        'skills': Skill.query.count(),
        'testimonials': Testimonial.query.count(),
        'donation_projects': DonationProject.query.count(),
        'donations': Donation.query.count(),
        'total_donations_usd': sum((d.verified_amount or d.amount) for d in Donation.query.filter_by(status='completed', currency='USD').all()),
        'total_donations_npr': sum((d.verified_amount or d.amount) for d in Donation.query.filter_by(status='completed', currency='NPR').all()),
        'recent_contacts': ContactSubmission.query.filter_by(is_spam=False).order_by(desc(ContactSubmission.submitted_at)).limit(5).all(),
        'recent_subscribers': NewsletterSubscriber.query.order_by(desc(NewsletterSubscriber.subscribed_at)).limit(5).all(),
        'recent_donations': Donation.query.order_by(desc(Donation.created_at)).limit(5).all()
    }
    return render_template('admin/dashboard.html', stats=stats)

# ============ PROJECTS MANAGEMENT ============
@admin_bp.route('/projects')
@admin_required
def projects():
    """List all projects"""
    # Get filter parameters
    category_id = request.args.get('category', type=int)
    status = request.args.get('status')
    search = request.args.get('search')
    
    # Build query
    query = Project.query
    
    if category_id:
        query = query.filter(Project.category_id == category_id)
    
    if status:
        query = query.filter(Project.status == status)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Project.title.ilike(search_term) | 
            Project.description.ilike(search_term) |
            Project.technologies.ilike(search_term)
        )
    
    projects = query.order_by(desc(Project.created_at)).all()
    categories = ProjectCategory.query.order_by(ProjectCategory.name).all()
    
    return render_template('admin/projects/list.html', projects=projects, categories=categories)

@admin_bp.route('/projects/create', methods=['GET', 'POST'])
@admin_required
def projects_create():
    """Create new project"""
    if request.method == 'GET':
        categories = ProjectCategory.query.order_by(ProjectCategory.name).all()
        return render_template('admin/projects/form.html', categories=categories)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        project = Project(
            title=data.get('title'),
            description=data.get('description'),
            image_url=data.get('image_url'),
            github_url=data.get('github_url'),
            live_url=data.get('live_url'),
            commercial_url=data.get('commercial_url'),
            technologies=data.get('technologies'),
            category_id=data.get('category_id') if data.get('category_id') else None,
            is_featured=bool(data.get('is_featured')),
            is_opensource=bool(data.get('is_opensource', True)),
            show_on_homepage=bool(data.get('show_on_homepage')),
            status=data.get('status', 'completed')
        )
        
        db.session.add(project)
        db.session.commit()
        
        # Try to fetch GitHub data if URL provided
        if project.github_url:
            project.fetch_github_data()
            db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'Project created successfully!'})
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error creating project: {str(e)}'}), 400
        flash(f'Error creating project: {str(e)}', 'danger')
        categories = ProjectCategory.query.order_by(ProjectCategory.name).all()
        return render_template('admin/projects/form.html', categories=categories)

@admin_bp.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def projects_edit(id):
    """Edit project"""
    project = Project.query.get_or_404(id)
    
    if request.method == 'GET':
        categories = ProjectCategory.query.order_by(ProjectCategory.name).all()
        return render_template('admin/projects/form.html', project=project, categories=categories)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        project.title = data.get('title', project.title)
        project.description = data.get('description', project.description)
        project.image_url = data.get('image_url', project.image_url)
        project.github_url = data.get('github_url', project.github_url)
        project.live_url = data.get('live_url', project.live_url)
        project.commercial_url = data.get('commercial_url', project.commercial_url)
        project.technologies = data.get('technologies', project.technologies)
        project.category_id = data.get('category_id') if data.get('category_id') else None
        project.is_featured = bool(data.get('is_featured'))
        project.is_opensource = bool(data.get('is_opensource'))
        project.show_on_homepage = bool(data.get('show_on_homepage'))
        project.status = data.get('status', project.status)
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'Project updated successfully!'})
        
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error updating project: {str(e)}'}), 400
        flash(f'Error updating project: {str(e)}', 'danger')
        categories = ProjectCategory.query.order_by(ProjectCategory.name).all()
        return render_template('admin/projects/form.html', project=project, categories=categories)

@admin_bp.route('/projects/<int:id>/delete', methods=['POST'])
@admin_required
def projects_delete(id):
    """Delete project"""
    try:
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'Project deleted successfully!'})
        
        flash('Project deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error deleting project: {str(e)}'}), 400
        flash(f'Error deleting project: {str(e)}', 'danger')
    
    return redirect(url_for('admin.projects'))

@admin_bp.route('/projects/<int:id>/refresh-github', methods=['POST'])
@admin_required
def projects_refresh_github(id):
    """Refresh GitHub data for project"""
    try:
        project = Project.query.get_or_404(id)
        
        if not project.github_url:
            return jsonify({'status': 'error', 'message': 'No GitHub URL set for this project'}), 400
        
        success = project.fetch_github_data()
        db.session.commit()
        
        if success:
            return jsonify({'status': 'success', 'message': 'GitHub data refreshed successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to fetch GitHub data'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Error refreshing GitHub data: {str(e)}'}), 400

# ============ CATEGORIES MANAGEMENT ============
@admin_bp.route('/categories')
@admin_required
def categories():
    """List all categories"""
    categories = ProjectCategory.query.order_by(ProjectCategory.name).all()
    return render_template('admin/categories/list.html', categories=categories)

@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@admin_required
def categories_create():
    """Create new category"""
    if request.method == 'GET':
        return render_template('admin/categories/form.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        category = ProjectCategory(
            name=data.get('name'),
            description=data.get('description'),
            icon=data.get('icon'),
            color=data.get('color')
        )
        
        db.session.add(category)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'Category created successfully!'})
        
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin.categories'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error creating category: {str(e)}'}), 400
        flash(f'Error creating category: {str(e)}', 'danger')
        return render_template('admin/categories/form.html')

@admin_bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def categories_edit(id):
    """Edit category"""
    category = ProjectCategory.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/categories/form.html', category=category)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        category.icon = data.get('icon', category.icon)
        category.color = data.get('color', category.color)
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'Category updated successfully!'})
        
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin.categories'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error updating category: {str(e)}'}), 400
        flash(f'Error updating category: {str(e)}', 'danger')
        return render_template('admin/categories/form.html', category=category)

@admin_bp.route('/categories/<int:id>/delete', methods=['POST'])
@admin_required
def categories_delete(id):
    """Delete category"""
    try:
        category = ProjectCategory.query.get_or_404(id)
        
        # Check if category has projects
        if category.projects.count() > 0:
            if request.is_json:
                return jsonify({'status': 'error', 'message': 'Cannot delete category with projects'}), 400
            flash('Cannot delete category that has projects assigned to it.', 'danger')
            return redirect(url_for('admin.categories'))
        
        db.session.delete(category)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'Category deleted successfully!'})
        
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error deleting category: {str(e)}'}), 400
        flash(f'Error deleting category: {str(e)}', 'danger')
    
    return redirect(url_for('admin.categories'))

# ============ SKILLS MANAGEMENT ============
@admin_bp.route('/skills')
@admin_required
def skills():
    """List all skills"""
    # Get filter parameters
    category = request.args.get('category')
    featured = request.args.get('featured')
    search = request.args.get('search')
    
    # Build query
    query = Skill.query
    
    if category:
        query = query.filter(Skill.category == category)
    
    if featured is not None:
        query = query.filter(Skill.is_featured == (featured == '1'))
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Skill.name.ilike(search_term) | 
            Skill.description.ilike(search_term)
        )
    
    skills = query.order_by(Skill.sort_order, Skill.name).all()
    
    return render_template('admin/skills/list.html', skills=skills)

@admin_bp.route('/skills/create', methods=['GET', 'POST'])
@admin_required
def skills_create():
    """Create new skill"""
    if request.method == 'GET':
        return render_template('admin/skills/form.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        skill = Skill(
            name=data.get('name'),
            category=data.get('category'),
            proficiency=int(data.get('proficiency', 50)) if data.get('proficiency') else None,
            icon=data.get('icon'),
            description=data.get('description'),
            years_experience=float(data.get('years_experience')) if data.get('years_experience') else None,
            is_featured=bool(data.get('is_featured')),
            sort_order=int(data.get('sort_order', 0)) if data.get('sort_order') else 0
        )
        
        db.session.add(skill)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'Skill created successfully!'})
        
        flash('Skill created successfully!', 'success')
        return redirect(url_for('admin.skills'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error creating skill: {str(e)}'}), 400
        flash(f'Error creating skill: {str(e)}', 'danger')
        return render_template('admin/skills/form.html')

@admin_bp.route('/skills/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def skills_edit(id):
    """Edit skill"""
    skill = Skill.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/skills/form.html', skill=skill)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        skill.name = data.get('name', skill.name)
        skill.category = data.get('category', skill.category)
        skill.proficiency = int(data.get('proficiency')) if data.get('proficiency') else skill.proficiency
        skill.icon = data.get('icon', skill.icon)
        skill.description = data.get('description', skill.description)
        skill.years_experience = float(data.get('years_experience')) if data.get('years_experience') else skill.years_experience
        skill.is_featured = bool(data.get('is_featured'))
        skill.sort_order = int(data.get('sort_order', 0)) if data.get('sort_order') else skill.sort_order
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'Skill updated successfully!'})
        
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('admin.skills'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error updating skill: {str(e)}'}), 400
        flash(f'Error updating skill: {str(e)}', 'danger')
        return render_template('admin/skills/form.html', skill=skill)

@admin_bp.route('/skills/<int:id>/delete', methods=['POST'])
@admin_required
def skills_delete(id):
    """Delete skill"""
    try:
        skill = Skill.query.get_or_404(id)
        db.session.delete(skill)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'Skill deleted successfully!'})
        
        flash('Skill deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error deleting skill: {str(e)}'}), 400
        flash(f'Error deleting skill: {str(e)}', 'danger')
    
    return redirect(url_for('admin.skills'))

# ============ SEO SETTINGS MANAGEMENT ============
@admin_bp.route('/seo')
@admin_required
def seo_settings():
    """List all SEO settings"""
    seo_settings = SeoSettings.query.order_by(SeoSettings.page_name).all()
    return render_template('admin/seo/list.html', seo_settings=seo_settings)

@admin_bp.route('/seo/create', methods=['GET', 'POST'])
@admin_required
def seo_create():
    """Create new SEO settings"""
    if request.method == 'GET':
        return render_template('admin/seo/form.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        # Check if page already has SEO settings
        existing = SeoSettings.query.filter_by(page_name=data.get('page_name')).first()
        if existing:
            if request.is_json:
                return jsonify({'status': 'error', 'message': 'SEO settings for this page already exist'}), 400
            flash('SEO settings for this page already exist. Edit the existing settings instead.', 'danger')
            return render_template('admin/seo/form.html')
        
        seo = SeoSettings(
            page_name=data.get('page_name'),
            title=data.get('title'),
            meta_description=data.get('meta_description'),
            meta_keywords=data.get('meta_keywords'),
            og_title=data.get('og_title'),
            og_description=data.get('og_description'),
            og_image=data.get('og_image'),
            canonical_url=data.get('canonical_url'),
            robots=data.get('robots', 'index, follow'),
            schema_markup=data.get('schema_markup'),
            is_active=bool(data.get('is_active', True))
        )
        
        db.session.add(seo)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'SEO settings created successfully!'})
        
        flash('SEO settings created successfully!', 'success')
        return redirect(url_for('admin.seo_settings'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error creating SEO settings: {str(e)}'}), 400
        flash(f'Error creating SEO settings: {str(e)}', 'danger')
        return render_template('admin/seo/form.html')

@admin_bp.route('/seo/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def seo_edit(id):
    """Edit SEO settings"""
    seo = SeoSettings.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/seo/form.html', seo=seo)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        seo.title = data.get('title', seo.title)
        seo.meta_description = data.get('meta_description', seo.meta_description)
        seo.meta_keywords = data.get('meta_keywords', seo.meta_keywords)
        seo.og_title = data.get('og_title', seo.og_title)
        seo.og_description = data.get('og_description', seo.og_description)
        seo.og_image = data.get('og_image', seo.og_image)
        seo.canonical_url = data.get('canonical_url', seo.canonical_url)
        seo.robots = data.get('robots', seo.robots)
        seo.schema_markup = data.get('schema_markup', seo.schema_markup)
        seo.is_active = bool(data.get('is_active'))
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'SEO settings updated successfully!'})
        
        flash('SEO settings updated successfully!', 'success')
        return redirect(url_for('admin.seo_settings'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error updating SEO settings: {str(e)}'}), 400
        flash(f'Error updating SEO settings: {str(e)}', 'danger')
        return render_template('admin/seo/form.html', seo=seo)

@admin_bp.route('/seo/<int:id>/delete', methods=['POST'])
@admin_required
def seo_delete(id):
    """Delete SEO settings"""
    try:
        seo = SeoSettings.query.get_or_404(id)
        db.session.delete(seo)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'SEO settings deleted successfully!'})
        
        flash('SEO settings deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error deleting SEO settings: {str(e)}'}), 400
        flash(f'Error deleting SEO settings: {str(e)}', 'danger')
    
    return redirect(url_for('admin.seo_settings'))

@admin_bp.route('/api/seo/<int:id>/preview')
@admin_required
def seo_preview(id):
    """Get SEO preview data"""
    try:
        seo = SeoSettings.query.get_or_404(id)
        return jsonify({
            'page_name': seo.page_name,
            'title': seo.title,
            'meta_description': seo.meta_description,
            'meta_keywords': seo.meta_keywords,
            'og_title': seo.og_title,
            'og_description': seo.og_description,
            'og_image': seo.og_image,
            'canonical_url': seo.canonical_url,
            'robots': seo.robots,
            'schema_markup': seo.schema_markup,
            'is_active': seo.is_active
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============ LOGIN/LOGOUT ============
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login with enhanced security"""
    if request.method == 'GET':
        # Check if already logged in
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user and user.is_admin:
                return redirect(url_for('admin.dashboard'))
        return render_template('admin/login.html')
    
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Input validation
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            time.sleep(1)  # Delay to prevent timing attacks
            return render_template('admin/login.html')
        
        # Additional security: limit username length to prevent potential attacks
        if len(username) > 50 or len(password) > 200:
            flash('Invalid credentials.', 'error')
            time.sleep(2)  # Longer delay for suspicious input
            return render_template('admin/login.html')
        
        # Query user
        user = User.query.filter_by(username=username).first()
        
        # Check credentials and admin status
        if user and user.check_password(password) and user.is_admin:
            # Successful login
            session['user_id'] = user.id
            session['username'] = user.username
            session['login_time'] = datetime.utcnow().isoformat()
            
            # Log successful login
            current_app.logger.info(f'Admin login successful: {username} from IP: {get_remote_address()}')
            
            # Send admin login notification email
            try:
                from email_service import email_service
                login_time = datetime.utcnow()
                email_service.send_admin_login_notification(
                    username=username,
                    ip_address=get_remote_address(),
                    timestamp=login_time
                )
                current_app.logger.info(f'Admin login notification sent for: {username}')
            except Exception as e:
                current_app.logger.error(f'Failed to send admin login notification: {e}')
            
            flash('Welcome to admin dashboard!', 'success')
            
            # Redirect to next page if specified, otherwise dashboard
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/admin/'):
                return redirect(next_page)
            return redirect(url_for('admin.dashboard'))
        else:
            # Failed login
            current_app.logger.warning(f'Admin login failed: {username} from IP: {get_remote_address()}')
            flash('Invalid credentials or insufficient permissions.', 'error')
            time.sleep(2)  # Delay to prevent brute force attacks
            return render_template('admin/login.html')
            
    except Exception as e:
        current_app.logger.error(f'Admin login error: {str(e)} from IP: {get_remote_address()}')
        flash('Login error occurred. Please try again.', 'error')
        time.sleep(1)
        return render_template('admin/login.html')

@admin_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Admin logout with security logging"""
    username = session.get('username', 'Unknown')
    
    # Log logout
    current_app.logger.info(f'Admin logout: {username} from IP: {get_remote_address()}')
    
    # Clear session
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('admin.login'))

# ============ API ROUTES FOR AJAX ============
@admin_bp.route('/api/projects/<int:id>/toggle-featured', methods=['POST'])
@admin_required
def toggle_project_featured(id):
    """Toggle project featured status"""
    try:
        project = Project.query.get_or_404(id)
        data = request.get_json()
        project.is_featured = data.get('featured', False)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@admin_bp.route('/api/projects/<int:id>/toggle-homepage', methods=['POST'])
@admin_required
def toggle_project_homepage(id):
    """Toggle project homepage display status"""
    try:
        project = Project.query.get_or_404(id)
        data = request.get_json()
        project.show_on_homepage = data.get('show_on_homepage', False)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@admin_bp.route('/api/skills/<int:id>/toggle-featured', methods=['POST'])
@admin_required
def toggle_skill_featured(id):
    """Toggle skill featured status"""
    try:
        skill = Skill.query.get_or_404(id)
        data = request.get_json()
        skill.is_featured = data.get('featured', False)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@admin_bp.route('/api/contacts/<int:id>/mark-spam', methods=['POST'])
@admin_required
def mark_contact_spam(id):
    """Mark contact as spam"""
    try:
        contact = ContactSubmission.query.get_or_404(id)
        contact.is_spam = True
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@admin_bp.route('/api/newsletter/<int:id>/toggle-active', methods=['POST'])
@admin_required
def toggle_newsletter_active(id):
    """Toggle newsletter subscriber active status"""
    try:
        subscriber = NewsletterSubscriber.query.get_or_404(id)
        data = request.get_json()
        subscriber.is_active = data.get('active', False)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@admin_bp.route('/api/projects/bulk-action', methods=['POST'])
@admin_required
def projects_bulk_action():
    """Handle bulk actions on projects"""
    try:
        data = request.get_json()
        action = data.get('action')
        project_ids = data.get('project_ids', [])
        
        if not action or not project_ids:
            return jsonify({'status': 'error', 'message': 'Invalid request'}), 400
        
        projects = Project.query.filter(Project.id.in_(project_ids)).all()
        
        if action == 'feature':
            for project in projects:
                project.is_featured = True
        elif action == 'unfeature':
            for project in projects:
                project.is_featured = False
        elif action == 'show_homepage':
            for project in projects:
                project.show_on_homepage = True
        elif action == 'hide_homepage':
            for project in projects:
                project.show_on_homepage = False
        elif action.startswith('status_'):
            status = action.replace('status_', '')
            for project in projects:
                project.status = status
        elif action == 'delete':
            for project in projects:
                db.session.delete(project)
        
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'Bulk action completed on {len(projects)} projects'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ============ CONTACT SUBMISSIONS MANAGEMENT ============
@admin_bp.route('/contacts')
@admin_required
def contacts():
    """List all contact submissions"""
    # Get filter parameters
    status = request.args.get('status')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    search = request.args.get('search')
    
    # Build query
    query = ContactSubmission.query
    
    if status == 'unread':
        query = query.filter(ContactSubmission.is_read == False, ContactSubmission.is_spam == False)
    elif status == 'read':
        query = query.filter(ContactSubmission.is_read == True, ContactSubmission.is_spam == False)
    elif status == 'spam':
        query = query.filter(ContactSubmission.is_spam == True)
    else:
        query = query.filter(ContactSubmission.is_spam == False)
    
    if date_from:
        from datetime import datetime
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(ContactSubmission.submitted_at >= date_from)
    
    if date_to:
        from datetime import datetime
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        query = query.filter(ContactSubmission.submitted_at <= date_to)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            ContactSubmission.name.ilike(search_term) |
            ContactSubmission.email.ilike(search_term) |
            ContactSubmission.subject.ilike(search_term) |
            ContactSubmission.message.ilike(search_term)
        )
    
    contacts = query.order_by(desc(ContactSubmission.submitted_at)).all()
    
    return render_template('admin/contacts/list.html', contacts=contacts)

@admin_bp.route('/contacts/<int:id>')
@admin_required
def contacts_view(id):
    """View contact submission details"""
    contact = ContactSubmission.query.get_or_404(id)
    
    # Get previous and next contacts for navigation
    prev_contact = ContactSubmission.query.filter(
        ContactSubmission.id < id,
        ContactSubmission.is_spam == False
    ).order_by(ContactSubmission.id.desc()).first()
    
    next_contact = ContactSubmission.query.filter(
        ContactSubmission.id > id,
        ContactSubmission.is_spam == False
    ).order_by(ContactSubmission.id.asc()).first()
    
    return render_template('admin/contacts/view.html', 
                         contact=contact, 
                         prev_contact=prev_contact, 
                         next_contact=next_contact)

@admin_bp.route('/contacts/<int:id>/reply', methods=['POST'])
@admin_required
def reply_contact(id):
    """Mark contact as replied"""
    try:
        contact = ContactSubmission.query.get_or_404(id)
        contact.is_replied = True
        contact.replied_at = datetime.utcnow()
        db.session.commit()
        flash('Contact marked as replied!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating contact: {str(e)}', 'danger')
    
    return redirect(url_for('admin.view_contact', id=id))

# ============ NEWSLETTER SUBSCRIBERS MANAGEMENT ============
@admin_bp.route('/newsletter')
@admin_required
def newsletter():
    """List all newsletter subscribers"""
    # Get filter parameters
    status = request.args.get('status')
    date_from = request.args.get('date_from')
    search = request.args.get('search')
    
    # Build query
    query = NewsletterSubscriber.query
    
    if status == 'active':
        query = query.filter(NewsletterSubscriber.is_active == True)
    elif status == 'inactive':
        query = query.filter(NewsletterSubscriber.is_active == False)
    
    if date_from:
        from datetime import datetime
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(NewsletterSubscriber.subscribed_at >= date_from)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(NewsletterSubscriber.email.ilike(search_term))
    
    subscribers = query.order_by(desc(NewsletterSubscriber.subscribed_at)).all()
    
    # Calculate statistics
    total_subscribers = NewsletterSubscriber.query.count()
    active_subscribers = NewsletterSubscriber.query.filter_by(is_active=True).count()
    inactive_subscribers = total_subscribers - active_subscribers
    
    from datetime import datetime, timedelta
    this_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month_subscribers = NewsletterSubscriber.query.filter(
        NewsletterSubscriber.subscribed_at >= this_month_start
    ).count()
    
    return render_template('admin/newsletter/list.html', 
                         subscribers=subscribers,
                         total_subscribers=total_subscribers,
                         active_subscribers=active_subscribers,
                         inactive_subscribers=inactive_subscribers,
                         this_month_subscribers=this_month_subscribers)
    
    return render_template('admin/newsletter/list.html', subscribers=subscribers)

@admin_bp.route('/newsletter/export')
@admin_required
def export_newsletter():
    """Export newsletter subscribers to CSV"""
    import csv
    from io import StringIO
    from flask import Response
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Email', 'Name', 'Interests', 'Status', 'Subscribed At'])
    
    # Write data
    subscribers = NewsletterSubscriber.query.all()
    for sub in subscribers:
        writer.writerow([
            sub.email,
            sub.name or '',
            sub.interests or '',
            'Active' if sub.is_active else 'Inactive',
            sub.subscribed_at.strftime('%Y-%m-%d %H:%M:%S') if sub.subscribed_at else ''
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=newsletter_subscribers.csv'}
    )

# ============ PERSONAL INFO MANAGEMENT ============
@admin_bp.route('/personal-info', methods=['GET', 'POST'])
@admin_required
def personal_info():
    """Manage personal information"""
    info = PersonalInfo.query.first()
    
    if request.method == 'GET':
        return render_template('admin/personal_info.html', info=info)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        if not info:
            info = PersonalInfo()
            db.session.add(info)
        
        info.name = data.get('name', info.name if info else '')
        info.title = data.get('title', info.title if info else '')
        info.bio = data.get('bio', info.bio if info else '')
        info.email = data.get('email', info.email if info else '')
        info.phone = data.get('phone', info.phone if info else '')
        info.address = data.get('address', info.address if info else '')
        info.profile_image = data.get('profile_image', info.profile_image if info else '')
        info.resume_url = data.get('resume_url', info.resume_url if info else '')
        info.location = data.get('location', info.location if info else '')
        info.tagline = data.get('tagline', info.tagline if info else '')
        info.years_experience = int(data.get('years_experience', 0)) if data.get('years_experience') else (info.years_experience if info else 0)
        info.projects_completed = int(data.get('projects_completed', 0)) if data.get('projects_completed') else (info.projects_completed if info else 0)
        info.clients_served = int(data.get('clients_served', 0)) if data.get('clients_served') else (info.clients_served if info else 0)
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'status': 'success', 'message': 'Personal information updated successfully!'})
        
        flash('Personal information updated successfully!', 'success')
        return redirect(url_for('admin.personal_info'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'status': 'error', 'message': f'Error updating personal information: {str(e)}'}), 400
        flash(f'Error updating personal information: {str(e)}', 'danger')
        return render_template('admin/personal_info.html', info=info)

# ============ EXPERIENCE MANAGEMENT ============
@admin_bp.route('/experience')
@admin_required
def experience():
    """List all experience entries"""
    experiences = Experience.query.order_by(desc(Experience.start_date)).all()
    return render_template('admin/experience/list.html', experiences=experiences)

@admin_bp.route('/experience/create', methods=['GET', 'POST'])
@admin_required
def experience_create():
    """Create new experience"""
    if request.method == 'GET':
        return render_template('admin/experience/form.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        experience = Experience(
            title=data.get('title'),
            company=data.get('company'),
            location=data.get('location'),
            description=data.get('description'),
            start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d').date() if data.get('start_date') else None,
            end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d').date() if data.get('end_date') else None,
            is_current=bool(data.get('is_current')),
            company_url=data.get('company_url'),
            technologies=data.get('technologies')
        )
        
        db.session.add(experience)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Experience created successfully!'})
        
        flash('Experience created successfully!', 'success')
        return redirect(url_for('admin.experience'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error creating experience: {str(e)}', 'danger')
        return render_template('admin/experience/form.html')

@admin_bp.route('/experience/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def experience_edit(id):
    """Edit experience"""
    experience = Experience.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/experience/form.html', experience=experience)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        experience.title = data.get('title')
        experience.company = data.get('company')
        experience.location = data.get('location')
        experience.description = data.get('description')
        experience.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date() if data.get('start_date') else None
        experience.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date() if data.get('end_date') else None
        experience.is_current = bool(data.get('is_current'))
        experience.company_url = data.get('company_url')
        experience.technologies = data.get('technologies')
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Experience updated successfully!'})
        
        flash('Experience updated successfully!', 'success')
        return redirect(url_for('admin.experience'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error updating experience: {str(e)}', 'danger')
        return render_template('admin/experience/form.html', experience=experience)

@admin_bp.route('/experience/<int:id>/delete', methods=['POST'])
@admin_required
def experience_delete(id):
    """Delete experience"""
    try:
        experience = Experience.query.get_or_404(id)
        db.session.delete(experience)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Experience deleted successfully!'})
        
        flash('Experience deleted successfully!', 'success')
        return redirect(url_for('admin.experience'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error deleting experience: {str(e)}', 'danger')
        return redirect(url_for('admin.experience'))

# ============ EDUCATION MANAGEMENT ============
@admin_bp.route('/education')
@admin_required
def education():
    """List all education entries"""
    educations = Education.query.order_by(desc(Education.start_date)).all()
    return render_template('admin/education/list.html', educations=educations)

@admin_bp.route('/education/create', methods=['GET', 'POST'])
@admin_required
def education_create():
    """Create new education"""
    if request.method == 'GET':
        return render_template('admin/education/form.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        education = Education(
            degree=data.get('degree'),
            field_of_study=data.get('field_of_study'),
            institution=data.get('institution'),
            location=data.get('location'),
            description=data.get('description'),
            start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d').date() if data.get('start_date') else None,
            end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d').date() if data.get('end_date') else None,
            is_current=bool(data.get('is_current')),
            gpa=float(data.get('gpa')) if data.get('gpa') else None,
            institution_url=data.get('institution_url')
        )
        
        db.session.add(education)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Education created successfully!'})
        
        flash('Education created successfully!', 'success')
        return redirect(url_for('admin.education'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error creating education: {str(e)}', 'danger')
        return render_template('admin/education/form.html')

@admin_bp.route('/education/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def education_edit(id):
    """Edit education"""
    education = Education.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/education/form.html', education=education)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        education.degree = data.get('degree')
        education.field_of_study = data.get('field_of_study')
        education.institution = data.get('institution')
        education.location = data.get('location')
        education.description = data.get('description')
        education.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date() if data.get('start_date') else None
        education.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date() if data.get('end_date') else None
        education.is_current = bool(data.get('is_current'))
        education.gpa = float(data.get('gpa')) if data.get('gpa') else None
        education.institution_url = data.get('institution_url')
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Education updated successfully!'})
        
        flash('Education updated successfully!', 'success')
        return redirect(url_for('admin.education'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error updating education: {str(e)}', 'danger')
        return render_template('admin/education/form.html', education=education)

@admin_bp.route('/education/<int:id>/delete', methods=['POST'])
@admin_required
def education_delete(id):
    """Delete education"""
    try:
        education = Education.query.get_or_404(id)
        db.session.delete(education)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Education deleted successfully!'})
        
        flash('Education deleted successfully!', 'success')
        return redirect(url_for('admin.education'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error deleting education: {str(e)}', 'danger')
        return redirect(url_for('admin.education'))

# ============ SOCIAL LINKS MANAGEMENT ============
@admin_bp.route('/social-links')
@admin_required
def social_links():
    """List all social links"""
    links = SocialLink.query.order_by(SocialLink.sort_order, SocialLink.platform).all()
    return render_template('admin/social/list.html', links=links)

@admin_bp.route('/social-links/create', methods=['GET', 'POST'])
@admin_required
def social_links_create():
    """Create new social link"""
    if request.method == 'GET':
        return render_template('admin/social/form.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        link = SocialLink(
            platform=data.get('platform'),
            url=data.get('url'),
            username=data.get('username'),
            icon_class=data.get('icon_class'),
            is_active=bool(data.get('is_active', True)),
            sort_order=int(data.get('sort_order', 0)) if data.get('sort_order') else 0
        )
        
        db.session.add(link)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Social link created successfully!'})
        
        flash('Social link created successfully!', 'success')
        return redirect(url_for('admin.social_links'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error creating social link: {str(e)}', 'danger')
        return render_template('admin/social/form.html')

@admin_bp.route('/social-links/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def social_links_edit(id):
    """Edit social link"""
    link = SocialLink.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/social/form.html', link=link)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        link.platform = data.get('platform')
        link.url = data.get('url')
        link.username = data.get('username')
        link.icon_class = data.get('icon_class')
        link.is_active = bool(data.get('is_active'))
        link.sort_order = int(data.get('sort_order', 0)) if data.get('sort_order') else 0
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Social link updated successfully!'})
        
        flash('Social link updated successfully!', 'success')
        return redirect(url_for('admin.social_links'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error updating social link: {str(e)}', 'danger')
        return render_template('admin/social/form.html', link=link)

@admin_bp.route('/social-links/<int:id>/delete', methods=['POST'])
@admin_required
def social_links_delete(id):
    """Delete social link"""
    try:
        link = SocialLink.query.get_or_404(id)
        db.session.delete(link)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Social link deleted successfully!'})
        
        flash('Social link deleted successfully!', 'success')
        return redirect(url_for('admin.social_links'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error deleting social link: {str(e)}', 'danger')
        return redirect(url_for('admin.social_links'))

# ============ TESTIMONIALS MANAGEMENT ============
@admin_bp.route('/testimonials')
@admin_required
def testimonials():
    """List all testimonials"""
    testimonials = Testimonial.query.order_by(desc(Testimonial.created_at)).all()
    return render_template('admin/testimonials/list.html', testimonials=testimonials)

@admin_bp.route('/testimonials/create', methods=['GET', 'POST'])
@admin_required
def testimonials_create():
    """Create new testimonial"""
    if request.method == 'GET':
        return render_template('admin/testimonials/form.html')
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        testimonial = Testimonial(
            client_name=data.get('client_name'),
            client_title=data.get('client_title'),
            client_company=data.get('client_company'),
            testimonial_text=data.get('testimonial_text'),
            client_image=data.get('client_image'),
            rating=int(data.get('rating', 5)) if data.get('rating') else 5,
            is_featured=bool(data.get('is_featured')),
            project_related=data.get('project_related'),
            sort_order=int(data.get('sort_order', 0)) if data.get('sort_order') else 0
        )
        
        db.session.add(testimonial)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Testimonial created successfully!'})
        
        flash('Testimonial created successfully!', 'success')
        return redirect(url_for('admin.testimonials'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error creating testimonial: {str(e)}', 'danger')
        return render_template('admin/testimonials/form.html')

@admin_bp.route('/testimonials/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def testimonials_edit(id):
    """Edit testimonial"""
    testimonial = Testimonial.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/testimonials/form.html', testimonial=testimonial)
    
    try:
        data = request.get_json() if request.is_json else request.form
        
        testimonial.client_name = data.get('client_name')
        testimonial.client_title = data.get('client_title')
        testimonial.client_company = data.get('client_company')
        testimonial.testimonial_text = data.get('testimonial_text')
        testimonial.client_image = data.get('client_image')
        testimonial.rating = int(data.get('rating', 5)) if data.get('rating') else 5
        testimonial.is_featured = bool(data.get('is_featured'))
        testimonial.project_related = data.get('project_related')
        testimonial.sort_order = int(data.get('sort_order', 0)) if data.get('sort_order') else 0
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Testimonial updated successfully!'})
        
        flash('Testimonial updated successfully!', 'success')
        return redirect(url_for('admin.testimonials'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error updating testimonial: {str(e)}', 'danger')
        return render_template('admin/testimonials/form.html', testimonial=testimonial)

@admin_bp.route('/testimonials/<int:id>/delete', methods=['POST'])
@admin_required
def testimonials_delete(id):
    """Delete testimonial"""
    try:
        testimonial = Testimonial.query.get_or_404(id)
        db.session.delete(testimonial)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Testimonial deleted successfully!'})
        
        flash('Testimonial deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error deleting testimonial: {str(e)}', 'danger')
    return redirect(url_for('admin.testimonials'))

@admin_bp.route('/api/testimonials/<int:id>/toggle-featured', methods=['POST'])
@admin_required
def api_testimonials_toggle_featured(id):
    """Toggle testimonial featured status"""
    try:
        testimonial = Testimonial.query.get_or_404(id)
        testimonial.is_featured = not testimonial.is_featured
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Testimonial {"featured" if testimonial.is_featured else "unfeatured"} successfully!',
            'is_featured': testimonial.is_featured
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400

# ============ DONATION PROJECTS MANAGEMENT ============
@admin_bp.route('/donation-projects')
@admin_required
def donation_projects():
    """List all donation projects"""
    # Get filter parameters
    status = request.args.get('status')
    featured = request.args.get('featured')
    
    # Base query
    query = DonationProject.query
    
    # Apply filters
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    
    if featured == 'true':
        query = query.filter_by(is_featured=True)
    elif featured == 'false':
        query = query.filter_by(is_featured=False)
    
    # Execute query
    projects = query.order_by(desc(DonationProject.created_at)).all()
    
    return render_template('admin/donation_projects/list.html', 
                         projects=projects,
                         current_status=status,
                         current_featured=featured)

@admin_bp.route('/donation-projects/new')
@admin_required
def donation_project_new():
    """Show form to create new donation project"""
    return render_template('admin/donation_projects/form.html')

@admin_bp.route('/donation-projects/create', methods=['POST'])
@admin_required
def donation_project_create():
    """Create new donation project"""
    try:
        project = DonationProject(
            title=request.form['title'],
            description=request.form['description'],
            short_description=request.form.get('short_description', ''),
            goal_amount=float(request.form.get('goal_amount', 0)),
            image_url=request.form.get('image_url', ''),
            github_url=request.form.get('github_url', ''),
            demo_url=request.form.get('demo_url', ''),
            is_active=bool(request.form.get('is_active')),
            is_featured=bool(request.form.get('is_featured'))
        )
        
        db.session.add(project)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Donation project created successfully'})
        
        flash('Donation project created successfully!', 'success')
        return redirect(url_for('admin.donation_projects'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error creating donation project: {str(e)}', 'danger')
        return redirect(url_for('admin.donation_project_new'))

@admin_bp.route('/donation-projects/<int:project_id>/edit')
@admin_required
def donation_project_edit(project_id):
    """Show form to edit donation project"""
    project = DonationProject.query.get_or_404(project_id)
    return render_template('admin/donation_projects/form.html', project=project)

@admin_bp.route('/donation-projects/<int:project_id>/update', methods=['POST'])
@admin_required
def donation_project_update(project_id):
    """Update donation project"""
    try:
        project = DonationProject.query.get_or_404(project_id)
        
        project.title = request.form['title']
        project.description = request.form['description']
        project.short_description = request.form.get('short_description', '')
        project.goal_amount = float(request.form.get('goal_amount', 0))
        project.image_url = request.form.get('image_url', '')
        project.github_url = request.form.get('github_url', '')
        project.demo_url = request.form.get('demo_url', '')
        project.is_active = bool(request.form.get('is_active'))
        project.is_featured = bool(request.form.get('is_featured'))
        project.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Donation project updated successfully'})
        
        flash('Donation project updated successfully!', 'success')
        return redirect(url_for('admin.donation_projects'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error updating donation project: {str(e)}', 'danger')
        return redirect(url_for('admin.donation_project_edit', project_id=project_id))

@admin_bp.route('/donation-projects/<int:project_id>/delete', methods=['POST'])
@admin_required
def donation_project_delete(project_id):
    """Delete donation project"""
    try:
        project = DonationProject.query.get_or_404(project_id)
        
        # Check if project has donations
        if project.donations.count() > 0:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Cannot delete project with existing donations'}), 400
            flash('Cannot delete project with existing donations', 'danger')
            return redirect(url_for('admin.donation_projects'))
        
        db.session.delete(project)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Donation project deleted successfully'})
        
        flash('Donation project deleted successfully!', 'success')
        return redirect(url_for('admin.donation_projects'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
        flash(f'Error deleting donation project: {str(e)}', 'danger')
        return redirect(url_for('admin.donation_projects'))

# ============ DONATIONS MANAGEMENT ============
@admin_bp.route('/donations')
@admin_required
def donations():
    """List all donations"""
    # Get filter parameters
    status = request.args.get('status')
    currency = request.args.get('currency')
    anonymous = request.args.get('anonymous')
    
    # Base query
    query = Donation.query
    
    # Apply filters
    if status:
        query = query.filter_by(status=status)
    if currency:
        query = query.filter_by(currency=currency)
    if anonymous == 'true':
        query = query.filter_by(is_anonymous=True)
    elif anonymous == 'false':
        query = query.filter_by(is_anonymous=False)
    
    # Execute query with pagination
    page = request.args.get('page', 1, type=int)
    donations_paginated = query.order_by(desc(Donation.created_at)).paginate(
        page=page, per_page=25, error_out=False)
    
    # Calculate totals by currency
    completed_donations = Donation.query.filter_by(status='completed').all()
    total_usd = sum((d.verified_amount or d.amount) for d in completed_donations if d.currency == 'USD')
    total_npr = sum((d.verified_amount or d.amount) for d in completed_donations if d.currency == 'NPR')
    
    return render_template('admin/donations/list.html', 
                         donations=donations_paginated,
                         current_status=status,
                         current_currency=currency,
                         current_anonymous=anonymous,
                         total_usd=total_usd,
                         total_npr=total_npr)

@admin_bp.route('/donations/<int:id>')
@admin_required
def donations_view(id):
    """View donation details"""
    donation = Donation.query.get_or_404(id)
    return render_template('admin/donations/view.html', donation=donation)

@admin_bp.route('/donations/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def donations_edit(id):
    """Edit donation (mainly for admin verification)"""
    donation = Donation.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/donations/form.html', donation=donation)
    
    try:
        # Store old status to check if it changed
        old_status = donation.status
        
        # Admin can update status, verified amount, notes, and anonymous status
        donation.status = request.form.get('status', donation.status)
        donation.verified_amount = float(request.form.get('verified_amount', 0)) or donation.amount
        donation.admin_notes = request.form.get('admin_notes', donation.admin_notes)
        donation.is_anonymous = request.form.get('is_anonymous') == 'on'
        
        # Get email amount for confirmation (optional, defaults to verified amount)
        email_amount = request.form.get('email_amount')
        send_confirmation = request.form.get('send_confirmation') == 'on'
        
        # If status changed to completed, update project amount
        if donation.status == 'completed' and donation.project:
            # Calculate difference and update project current_amount
            old_verified = donation.verified_amount or 0
            new_verified = donation.verified_amount
            if old_verified != new_verified:
                donation.project.current_amount += (new_verified - old_verified)
        
        db.session.commit()
        
        # Send confirmation email if status changed to completed and checkbox is checked
        if old_status != 'completed' and donation.status == 'completed' and send_confirmation:
            try:
                from email_service import email_service
                if email_service:
                    # Use custom email amount if provided, otherwise use verified amount
                    display_amount = float(email_amount) if email_amount else donation.verified_amount
                    email_service.send_donation_confirmation(
                        donation,
                        donation.project.title,
                        display_amount
                    )
                    flash('Donation updated and confirmation email sent!', 'success')
                else:
                    flash('Donation updated but email service not available.', 'warning')
            except Exception as e:
                logger.error(f"Failed to send donation confirmation email: {e}")
                flash('Donation updated but failed to send confirmation email.', 'warning')
        else:
            flash('Donation updated successfully!', 'success')
        
        return redirect(url_for('admin.donations'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating donation: {str(e)}', 'danger')
        return render_template('admin/donations/form.html', donation=donation)

@admin_bp.route('/donations/<int:id>/delete', methods=['POST'])
@admin_required
def donations_delete(id):
    """Delete donation"""
    try:
        donation = Donation.query.get_or_404(id)
        
        # If donation was completed, subtract from project total
        if donation.status == 'completed' and donation.project:
            verified_amount = donation.verified_amount or donation.amount
            donation.project.current_amount -= verified_amount
        
        db.session.delete(donation)
        db.session.commit()
        
        flash('Donation deleted successfully!', 'success')
        return redirect(url_for('admin.donations'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting donation: {str(e)}', 'danger')
        return redirect(url_for('admin.donations'))

@admin_bp.route('/donations/<int:id>/update-status', methods=['POST'])
@admin_required
def donations_update_status(id):
    """Update donation status (quick status update from list page)"""
    try:
        donation = Donation.query.get_or_404(id)
        old_status = donation.status
        new_status = request.form.get('status')
        
        if new_status not in ['pending', 'completed', 'failed']:
            flash('Invalid status provided', 'danger')
            return redirect(url_for('admin.donations'))
            
        donation.status = new_status
        
        # If status changed to completed, update project amount
        if old_status != 'completed' and new_status == 'completed' and donation.project:
            verified_amount = donation.verified_amount or donation.amount
            donation.project.current_amount += verified_amount
            
        # If status changed from completed to something else, subtract from project
        elif old_status == 'completed' and new_status != 'completed' and donation.project:
            verified_amount = donation.verified_amount or donation.amount
            donation.project.current_amount -= verified_amount
        
        db.session.commit()
        
        # Send confirmation email if status changed to completed
        if old_status != 'completed' and new_status == 'completed':
            try:
                from email_service import email_service
                if email_service:
                    email_service.send_donation_confirmation(
                        donation,
                        donation.project.title,
                        donation.verified_amount or donation.amount
                    )
            except Exception as e:
                logger.error(f"Failed to send donation confirmation email: {e}")
        
        flash(f'Donation status updated to {new_status.title()}!', 'success')
        return redirect(url_for('admin.donations'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating donation status: {str(e)}', 'danger')
        return redirect(url_for('admin.donations'))

@admin_bp.route('/donations/<int:id>/update-anonymous', methods=['POST'])
@admin_required
def donations_update_anonymous(id):
    """Update donation anonymous status"""
    try:
        donation = Donation.query.get_or_404(id)
        
        # Update anonymous status
        donation.is_anonymous = request.form.get('is_anonymous') == 'on'
        
        db.session.commit()
        
        status = 'anonymous' if donation.is_anonymous else 'public'
        flash(f'Donation anonymity status updated to {status}!', 'success')
        return redirect(url_for('admin.donations_view', id=donation.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating donation anonymity: {str(e)}', 'danger')
        return redirect(url_for('admin.donations_view', id=id))

@admin_bp.route('/donations/<int:id>/update-amount', methods=['POST'])
@admin_required
def donations_update_amount(id):
    """Update donation amount (original or verified)"""
    try:
        donation = Donation.query.get_or_404(id)
        
        # Check which amount is being updated
        original_amount = request.form.get('original_amount')
        verified_amount = request.form.get('verified_amount')
        
        if original_amount:
            old_amount = donation.amount
            donation.amount = float(original_amount)
            
            # If this donation is completed and affects project totals
            if donation.status == 'completed' and donation.project:
                # Adjust project total based on the change in original amount
                verified_amount_used = donation.verified_amount or old_amount
                new_verified_amount = donation.verified_amount or donation.amount
                donation.project.current_amount += (new_verified_amount - verified_amount_used)
            
            flash('Original donation amount updated successfully!', 'success')
            
        elif verified_amount:
            old_verified = donation.verified_amount or donation.amount
            donation.verified_amount = float(verified_amount)
            
            # If this donation is completed, update project total
            if donation.status == 'completed' and donation.project:
                donation.project.current_amount += (donation.verified_amount - old_verified)
            
            flash('Verified donation amount updated successfully!', 'success')
        
        db.session.commit()
        return redirect(url_for('admin.donations_view', id=donation.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating donation amount: {str(e)}', 'danger')
        return redirect(url_for('admin.donations_view', id=id))

# ============ PAYMENT METHODS MANAGEMENT ============
@admin_bp.route('/payment-methods')
@admin_required
def payment_methods():
    """List all payment methods"""
    currency = request.args.get('currency')
    query = PaymentMethod.query
    
    if currency:
        query = query.filter_by(currency=currency)
    
    methods = query.order_by(PaymentMethod.currency, PaymentMethod.sort_order).all()
    return render_template('admin/payment_methods/list.html', methods=methods, current_currency=currency)

@admin_bp.route('/payment-methods/create', methods=['GET', 'POST'])
@admin_required
def payment_methods_create():
    """Create new payment method"""
    if request.method == 'GET':
        return render_template('admin/payment_methods/form.html')
    
    try:
        method = PaymentMethod(
            currency=request.form['currency'],
            method_name=request.form['method_name'],
            display_name=request.form['display_name'],
            account_info=request.form.get('account_info', ''),
            swift_code=request.form.get('swift_code', ''),
            qr_code_url=request.form.get('qr_code_url', ''),
            instructions=request.form.get('instructions', ''),
            is_active=bool(request.form.get('is_active')),
            is_verification_pending=bool(request.form.get('is_verification_pending')),
            sort_order=int(request.form.get('sort_order', 0))
        )
        
        db.session.add(method)
        db.session.commit()
        
        flash('Payment method created successfully!', 'success')
        return redirect(url_for('admin.payment_methods'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating payment method: {str(e)}', 'danger')
        return render_template('admin/payment_methods/form.html')

@admin_bp.route('/payment-methods/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def payment_methods_edit(id):
    """Edit payment method"""
    method = PaymentMethod.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/payment_methods/form.html', method=method)
    
    try:
        method.currency = request.form['currency']
        method.method_name = request.form['method_name']
        method.display_name = request.form['display_name']
        method.account_info = request.form.get('account_info', '')
        method.swift_code = request.form.get('swift_code', '')
        method.qr_code_url = request.form.get('qr_code_url', '')
        method.instructions = request.form.get('instructions', '')
        method.is_active = bool(request.form.get('is_active'))
        method.is_verification_pending = bool(request.form.get('is_verification_pending'))
        method.sort_order = int(request.form.get('sort_order', 0)) if request.form.get('sort_order') else 0
        
        db.session.commit()
        flash('Payment method updated successfully!', 'success')
        return redirect(url_for('admin.payment_methods'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating payment method: {str(e)}', 'danger')
        return render_template('admin/payment_methods/form.html', method=method)

@admin_bp.route('/payment-methods/<int:id>/delete', methods=['POST'])
@admin_required
def payment_methods_delete(id):
    """Delete payment method"""
    try:
        method = PaymentMethod.query.get_or_404(id)
        db.session.delete(method)
        db.session.commit()
        
        flash('Payment method deleted successfully!', 'success')
        return redirect(url_for('admin.payment_methods'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting payment method: {str(e)}', 'danger')
        return redirect(url_for('admin.payment_methods'))

# ============ THANKSGIVING SETTINGS ============
@admin_bp.route('/thanksgiving-settings')
@admin_required
def thanksgiving_settings():
    """Manage thanksgiving page settings"""
    settings = ThanksgivingSettings.query.first()
    if not settings:
        # Create default settings
        settings = ThanksgivingSettings()
        db.session.add(settings)
        db.session.commit()
    
    return render_template('admin/thanksgiving_settings/form.html', settings=settings)

@admin_bp.route('/thanksgiving-settings/update', methods=['POST'])
@admin_required
def thanksgiving_settings_update():
    """Update thanksgiving settings"""
    try:
        settings = ThanksgivingSettings.query.first()
        if not settings:
            settings = ThanksgivingSettings()
            db.session.add(settings)
        
        settings.page_title = request.form['page_title']
        settings.page_description = request.form['page_description']
        settings.show_donor_names = bool(request.form.get('show_donor_names'))
        settings.show_amounts = bool(request.form.get('show_amounts'))
        settings.show_messages = bool(request.form.get('show_messages'))
        settings.min_amount_display = float(request.form.get('min_amount_display', 0))
        settings.anonymous_display_text = request.form['anonymous_display_text']
        settings.thank_you_message = request.form['thank_you_message']
        settings.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        flash('Thanksgiving settings updated successfully!', 'success')
        return redirect(url_for('admin.thanksgiving_settings'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating settings: {str(e)}', 'danger')
        return redirect(url_for('admin.thanksgiving_settings'))

# ============ DONATION SETTINGS ============
@admin_bp.route('/donation-settings')
@admin_required
def donation_settings():
    """Manage general donation settings"""
    settings = DonationSettings.query.first()
    if not settings:
        settings = DonationSettings()
        db.session.add(settings)
        db.session.commit()
    
    return render_template('admin/donation_settings/form.html', settings=settings)

@admin_bp.route('/donation-settings/update', methods=['POST'])
@admin_required
def donation_settings_update():
    """Update donation settings"""
    try:
        settings = DonationSettings.query.first()
        if not settings:
            settings = DonationSettings()
            db.session.add(settings)
        
        settings.default_currency = request.form['default_currency']
        settings.enable_custom_amounts = bool(request.form.get('enable_custom_amounts'))
        settings.enable_anonymous_donations = bool(request.form.get('enable_anonymous_donations'))
        settings.require_phone_verification = bool(request.form.get('require_phone_verification'))
        settings.thank_you_email_template = request.form.get('thank_you_email_template', '')
        settings.admin_notification_emails = request.form.get('admin_notification_emails', '')
        settings.auto_approve_donations = bool(request.form.get('auto_approve_donations'))
        
        db.session.commit()
        flash('Donation settings updated successfully!', 'success')
        return redirect(url_for('admin.donation_settings'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating settings: {str(e)}', 'danger')
        return redirect(url_for('admin.donation_settings'))

# ============ SESSION API ENDPOINTS ============
@admin_bp.route('/api/session-status')
@admin_required
def api_session_status():
    """Get current session status and time remaining"""
    try:
        # Check if session exists and is valid
        if 'user_id' not in session or 'login_time' not in session:
            return jsonify({'status': 'expired', 'time_remaining': 0})
        
        # Calculate time remaining (2 hours session)
        session_timeout = 7200  # 2 hours in seconds
        login_time_str = session.get('login_time')
        login_time = datetime.fromisoformat(login_time_str)
        current_time = datetime.utcnow()
        time_elapsed = (current_time - login_time).total_seconds()
        time_remaining = max(0, session_timeout - time_elapsed)
        
        if time_remaining <= 0:
            return jsonify({'status': 'expired', 'time_remaining': 0})
        elif time_remaining <= 300:  # 5 minutes warning
            return jsonify({'status': 'warning', 'time_remaining': int(time_remaining)})
        else:
            return jsonify({'status': 'active', 'time_remaining': int(time_remaining)})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@admin_bp.route('/api/extend-session', methods=['POST'])
@admin_required
def api_extend_session():
    """Extend the current session"""
    try:
        # Reset the session timer by updating login time
        session['login_time'] = datetime.utcnow().isoformat()
        session_timeout = 7200  # 2 hours
        
        return jsonify({
            'status': 'success',
            'message': 'Session extended successfully',
            'time_remaining': session_timeout
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============ DATA BACKUP AND EXPORT ============
@admin_bp.route('/data-management')
@admin_required
def data_management():
    """Data backup and export management page"""
    return render_template('admin/data_management.html')

@admin_bp.route('/export/full-backup')
@admin_required
def export_full_backup():
    """Export full database backup as JSON"""
    try:
        backup_data = {}
        
        # Export all models
        models_to_export = [
            User, Project, ProjectCategory, ContactSubmission, NewsletterSubscriber,
            SeoSettings, PersonalInfo, SocialLink, Skill, Experience, Education,
            Testimonial, DonationProject, Donation, PaymentMethod, ThanksgivingSettings,
            DonationSettings, WikiArticle, WikiCategory
        ]
        
        for model in models_to_export:
            table_name = model.__tablename__
            records = []
            
            for record in model.query.all():
                record_dict = {}
                for column in model.__table__.columns:
                    value = getattr(record, column.name)
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    record_dict[column.name] = value
                records.append(record_dict)
            
            backup_data[table_name] = records
        
        # Add metadata
        backup_data['_metadata'] = {
            'export_date': datetime.utcnow().isoformat(),
            'version': '1.0',
            'total_tables': len(models_to_export)
        }
        
        # Create response
        output = io.StringIO()
        json.dump(backup_data, output, indent=2, default=str)
        output.seek(0)
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Disposition'] = f'attachment; filename=portfolio_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        flash('Full backup exported successfully!', 'success')
        return response
        
    except Exception as e:
        flash(f'Error creating backup: {str(e)}', 'danger')
        return redirect(url_for('admin.data_management'))

@admin_bp.route('/export/donations-csv')
@admin_required
def export_donations_csv():
    """Export donations as CSV file"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            'ID', 'Donor Name', 'Email', 'Amount', 'Currency', 'Message',
            'Status', 'Project Title', 'Payment Method', 'Transaction ID',
            'Created At', 'Updated At'
        ])
        
        # Write data
        donations = Donation.query.all()
        for donation in donations:
            project_title = donation.project.title if donation.project else 'General Donation'
            writer.writerow([
                donation.id,
                donation.donor_name or 'Anonymous',
                donation.donor_email,
                donation.amount,
                donation.currency,
                donation.message or '',
                donation.status,
                project_title,
                donation.payment_method or '',
                donation.transaction_id or '',
                donation.created_at.isoformat() if donation.created_at else '',
                donation.updated_at.isoformat() if donation.updated_at else ''
            ])
        
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=donations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        flash('Donations exported successfully!', 'success')
        return response
        
    except Exception as e:
        flash(f'Error exporting donations: {str(e)}', 'danger')
        return redirect(url_for('admin.data_management'))

@admin_bp.route('/export/contacts-csv')
@admin_required
def export_contacts_csv():
    """Export contact submissions as CSV file"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(['ID', 'Name', 'Email', 'Subject', 'Message', 'Status', 'Created At'])
        
        # Write data
        contacts = ContactSubmission.query.all()
        for contact in contacts:
            writer.writerow([
                contact.id,
                contact.name,
                contact.email,
                contact.subject,
                contact.message,
                contact.status,
                contact.created_at.isoformat() if contact.created_at else ''
            ])
        
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=contacts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        flash('Contacts exported successfully!', 'success')
        return response
        
    except Exception as e:
        flash(f'Error exporting contacts: {str(e)}', 'danger')
        return redirect(url_for('admin.data_management'))

@admin_bp.route('/export/newsletter-csv')
@admin_required
def export_newsletter_csv():
    """Export newsletter subscribers as CSV file"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(['ID', 'Email', 'Interests', 'Status', 'Subscribed At'])
        
        # Write data
        subscribers = NewsletterSubscriber.query.all()
        for subscriber in subscribers:
            writer.writerow([
                subscriber.id,
                subscriber.email,
                subscriber.interests or '',
                'Active' if subscriber.is_active else 'Inactive',
                subscriber.created_at.isoformat() if subscriber.created_at else ''
            ])
        
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=newsletter_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        flash('Newsletter subscribers exported successfully!', 'success')
        return response
        
    except Exception as e:
        flash(f'Error exporting newsletter: {str(e)}', 'danger')
        return redirect(url_for('admin.data_management'))

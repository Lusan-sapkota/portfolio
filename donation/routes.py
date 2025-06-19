from flask import render_template, request, jsonify, flash, redirect, url_for, current_app
from . import donation_bp
from models import DonationProject, Donation, NewsletterSubscriber, db
from email_service import email_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@donation_bp.route('/')
def index():
    """Main donation page showing all active projects"""
    from models import SeoSettings, PersonalInfo, SocialLink
    
    # Get donation projects (we can use regular projects for donations too)
    try:
        # Check if we have DonationProject model, otherwise use Project
        featured_projects = DonationProject.query.filter_by(is_active=True, is_featured=True).all()
        all_projects = DonationProject.query.filter_by(is_active=True).all()
        
        # Get recent donations for activity feed
        recent_donations = Donation.query.filter_by(status='completed')\
                                       .order_by(Donation.created_at.desc())\
                                       .limit(10).all()
    except:
        # Fallback to regular projects if DonationProject doesn't exist
        from models import Project
        featured_projects = Project.query.filter_by(is_featured=True).all()
        all_projects = Project.query.all()
        recent_donations = []
    
    # Get CMS data
    seo = SeoSettings.query.filter_by(page_name='donation').first() or SeoSettings.query.first()
    personal = PersonalInfo.query.first()
    social_links = SocialLink.query.all()
    
    return render_template('donation.html', 
                         featured_projects=featured_projects,
                         all_projects=all_projects,
                         recent_donations=recent_donations,
                         seo_settings=seo,
                         personal_info=personal,
                         social_links=social_links,
                         current_year=datetime.now().year)

@donation_bp.route('/project/<int:project_id>')
def project_detail(project_id):
    """Detailed view of a specific donation project"""
    from models import SeoSettings, PersonalInfo
    
    try:
        project = DonationProject.query.get_or_404(project_id)
        
        # Get recent donations for this project
        donations = Donation.query.filter_by(project_id=project_id, status='completed')\
                                 .order_by(Donation.created_at.desc())\
                                 .limit(20).all()
    except:
        # Fallback to regular projects
        from models import Project
        project = Project.query.get_or_404(project_id)
        donations = []
    
    # Get CMS data
    seo = SeoSettings.query.filter_by(page_name='donation').first() or SeoSettings.query.first()
    personal = PersonalInfo.query.first()
    
    return render_template('project_detail.html', 
                         project=project,
                         donations=donations,
                         seo=seo,
                         personal=personal,
                         current_year=datetime.now().year)

@donation_bp.route('/donate/<int:project_id>', methods=['GET', 'POST'])
def donate(project_id):
    """Handle donation submission for a specific project"""
    from models import SeoSettings, PersonalInfo, SocialLink
    
    project = DonationProject.query.get_or_404(project_id)
    
    if request.method == 'POST':
        try:
            # Get form data
            donor_name = request.form.get('donor_name', '').strip()
            donor_email = request.form.get('donor_email', '').strip()
            amount = float(request.form.get('amount', 0))
            message = request.form.get('message', '').strip()
            is_anonymous = bool(request.form.get('is_anonymous'))
            payment_method = request.form.get('payment_method', 'manual')
            
            # Validate required fields
            if not donor_name or not donor_email or amount <= 0:
                if request.is_json:
                    return jsonify({'success': False, 'message': 'Please fill in all required fields'}), 400
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('donation.donate', project_id=project_id))
            
            # Create donation record
            donation = Donation(
                project_id=project_id,
                donor_name=donor_name,
                donor_email=donor_email,
                amount=amount,
                message=message,
                is_anonymous=is_anonymous,
                payment_method=payment_method,
                status='pending'  # Start as pending, admin can mark as completed
            )
            
            db.session.add(donation)
            db.session.commit()
            
            # Send thank you email
            try:
                if email_service:
                    email_service.send_donation_thank_you(
                        donor_email, 
                        donor_name, 
                        amount, 
                        project.title
                    )
            except Exception as e:
                logger.error(f"Failed to send thank you email: {e}")
            
            if request.is_json:
                return jsonify({
                    'success': True, 
                    'message': 'Thank you for your donation! Your contribution is being processed.',
                    'donation_id': donation.id
                })
            
            flash('Thank you for your donation! Your contribution is being processed.', 'success')
            return redirect(url_for('donation.donation_success', donation_id=donation.id))
            
        except ValueError:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Invalid amount entered'}), 400
            flash('Please enter a valid donation amount', 'error')
            return redirect(url_for('donation.donate', project_id=project_id))
        except Exception as e:
            logger.error(f"Donation error: {e}")
            db.session.rollback()
            if request.is_json:
                return jsonify({'success': False, 'message': 'An error occurred while processing your donation'}), 500
            flash('An error occurred while processing your donation. Please try again.', 'error')
            return redirect(url_for('donation.donate', project_id=project_id))
    
    # GET request - show donation form
    seo = SeoSettings.query.filter_by(page_name='donation').first() or SeoSettings.query.first()
    personal = PersonalInfo.query.first()
    social_links = SocialLink.query.all()
    
    return render_template('project_detail.html',
                         project=project,
                         seo_settings=seo,
                         personal_info=personal,
                         social_links=social_links,
                         current_year=datetime.now().year)

@donation_bp.route('/success/<int:donation_id>')
def donation_success(donation_id):
    """Thank you page after successful donation"""
    from models import SeoSettings, PersonalInfo, SocialLink
    
    donation = Donation.query.get_or_404(donation_id)
    
    seo = SeoSettings.query.filter_by(page_name='donation').first() or SeoSettings.query.first()
    personal = PersonalInfo.query.first()
    social_links = SocialLink.query.all()
    
    return render_template('donation_success.html',
                         donation=donation,
                         seo_settings=seo,
                         personal_info=personal,
                         social_links=social_links,
                         current_year=datetime.now().year)

@donation_bp.route('/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter"""
    try:
        email = request.form.get('email', '').strip().lower()
        name = request.form.get('name', '').strip()
        interests = request.form.get('interests', '').strip()
        
        if not email:
            if request.is_json or 'application/json' in request.headers.get('Accept', ''):
                return jsonify({'success': False, 'status': 'error', 'message': 'Please provide a valid email address.'})
            flash('Please provide a valid email address.', 'error')
            return redirect(url_for('donation.index'))
        
        # Check if already subscribed
        existing = NewsletterSubscriber.query.filter_by(email=email).first()
        if existing:
            if existing.is_active:
                if request.is_json or 'application/json' in request.headers.get('Accept', ''):
                    return jsonify({'success': False, 'status': 'info', 'message': 'You are already subscribed to our newsletter.'})
                flash('You are already subscribed to my newsletter.', 'info')
            else:
                existing.is_active = True
                existing.name = name or existing.name
                existing.interests = interests or existing.interests
                db.session.commit()
                if request.is_json or 'application/json' in request.headers.get('Accept', ''):
                    return jsonify({'success': True, 'status': 'success', 'message': 'Your newsletter subscription has been reactivated.'})
                flash('Your newsletter subscription has been reactivated.', 'success')
        else:
            subscriber = NewsletterSubscriber(
                email=email,
                name=name,
                interests=interests
            )
            db.session.add(subscriber)
            db.session.commit()
            
            # Send welcome email
            try:
                if email_service:
                    email_service.send_newsletter_welcome(email, name or 'Subscriber')
            except Exception as e:
                logger.error(f"Failed to send welcome email: {e}")
            
            if request.is_json or 'application/json' in request.headers.get('Accept', ''):
                return jsonify({'success': True, 'status': 'success', 'message': 'Thank you for subscribing to our newsletter!'})
            flash('Thank you for subscribing to my newsletter!', 'success')
        
        if request.is_json or 'application/json' in request.headers.get('Accept', ''):
            return jsonify({'success': True, 'status': 'success', 'message': 'Newsletter subscription updated successfully.'})
        return redirect(url_for('donation.index'))
        
    except Exception as e:
        logger.error(f"Newsletter subscription error: {e}")
        if request.is_json or 'application/json' in request.headers.get('Accept', ''):
            return jsonify({'success': False, 'status': 'error', 'message': 'An error occurred while subscribing. Please try again.'})
        flash('An error occurred while subscribing. Please try again.', 'error')
        return redirect(url_for('donation.index'))

@donation_bp.route('/api/projects')
def api_projects():
    """API endpoint to get all active projects"""
    projects = DonationProject.query.filter_by(is_active=True).all()
    return jsonify([project.to_dict() for project in projects])

@donation_bp.route('/api/project/<int:project_id>')
def api_project(project_id):
    """API endpoint to get a specific project"""
    project = DonationProject.query.get_or_404(project_id)
    return jsonify(project.to_dict())

@donation_bp.route('/api/donations/<int:project_id>')
def api_donations(project_id):
    """API endpoint to get donations for a project"""
    donations = Donation.query.filter_by(project_id=project_id, status='completed')\
                             .order_by(Donation.created_at.desc()).all()
    return jsonify([donation.to_dict() for donation in donations])

@donation_bp.route('/highlights')
def highlights():
    """Page showing project highlights and success stories"""
    featured_projects = DonationProject.query.filter_by(is_featured=True).all()
    completed_projects = DonationProject.query.filter(
        DonationProject.current_amount >= DonationProject.goal_amount
    ).all()
    
    return render_template('highlight.html',
                         featured_projects=featured_projects,
                         completed_projects=completed_projects,
                         current_year=datetime.now().year)

@donation_bp.route('/thanksgiving')
def thanksgiving():
    """Thanksgiving page showing appreciation for supporters"""
    recent_donations = Donation.query.filter_by(status='completed')\
                                   .order_by(Donation.created_at.desc())\
                                   .limit(20).all()
    
    total_donations = db.session.query(db.func.sum(Donation.amount))\
                               .filter_by(status='completed').scalar() or 0
    
    total_supporters = db.session.query(db.func.count(Donation.id.distinct()))\
                                .filter_by(status='completed').scalar() or 0
    
    return render_template('thanksgiving.html',
                         recent_donations=recent_donations,
                         total_donations=total_donations,
                         total_supporters=total_supporters,
                         current_year=datetime.now().year)

@donation_bp.route('/why-donate/<int:project_id>')
def why_donate(project_id):
    """Page explaining why someone should donate to a specific project"""
    project = DonationProject.query.get_or_404(project_id)
    return render_template('why_donate.html',
                         project=project,
                         current_year=datetime.now().year)

@donation_bp.route('/api/donate', methods=['POST'])
def api_donate():
    """API endpoint for donation submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['project_id', 'donor_name', 'donor_email', 'amount']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
        
        project = DonationProject.query.get(data['project_id'])
        if not project or not project.is_active:
            return jsonify({'success': False, 'message': 'Project not found or inactive'}), 404
        
        # Create donation record
        donation = Donation(
            project_id=data['project_id'],
            donor_name=data['donor_name'],
            donor_email=data['donor_email'],
            amount=float(data['amount']),
            message=data.get('message', ''),
            is_anonymous=data.get('is_anonymous', False),
            payment_method=data.get('payment_method', 'api'),
            status='pending'
        )
        
        db.session.add(donation)
        db.session.commit()
        
        # Send thank you email
        try:
            if email_service:
                email_service.send_donation_thank_you(
                    donation.donor_email, 
                    donation.donor_name, 
                    donation.amount, 
                    project.title
                )
        except Exception as e:
            logger.error(f"Failed to send thank you email: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Donation submitted successfully',
            'donation_id': donation.id
        })
        
    except Exception as e:
        logger.error(f"API donation error: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'An error occurred while processing your donation'}), 500

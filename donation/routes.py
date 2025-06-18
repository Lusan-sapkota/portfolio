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
    featured_projects = DonationProject.query.filter_by(is_active=True, is_featured=True).all()
    all_projects = DonationProject.query.filter_by(is_active=True).all()
    
    # Get recent donations for activity feed
    recent_donations = Donation.query.filter_by(status='completed')\
                                   .order_by(Donation.created_at.desc())\
                                   .limit(10).all()
    
    return render_template('donation.html', 
                         featured_projects=featured_projects,
                         all_projects=all_projects,
                         recent_donations=recent_donations,
                         current_year=datetime.now().year)

@donation_bp.route('/project/<int:project_id>')
def project_detail(project_id):
    """Detailed view of a specific donation project"""
    project = DonationProject.query.get_or_404(project_id)
    
    # Get recent donations for this project
    donations = Donation.query.filter_by(project_id=project_id, status='completed')\
                             .order_by(Donation.created_at.desc())\
                             .limit(20).all()
    
    return render_template('project_detail.html', 
                         project=project,
                         donations=donations,
                         current_year=datetime.now().year)

@donation_bp.route('/donate/<int:project_id>', methods=['POST'])
def make_donation(project_id):
    """Process a donation to a specific project"""
    try:
        project = DonationProject.query.get_or_404(project_id)
        
        # Get form data
        donor_name = request.form.get('donor_name', '').strip()
        donor_email = request.form.get('donor_email', '').strip()
        amount = float(request.form.get('amount', 0))
        message = request.form.get('message', '').strip()
        is_anonymous = request.form.get('is_anonymous') == 'on'
        payment_method = request.form.get('payment_method', 'paypal')
        
        # Validate input
        if not donor_name or not donor_email or amount <= 0:
            flash('Please fill in all required fields with valid values.', 'error')
            return redirect(url_for('donation.project_detail', project_id=project_id))
        
        # Create donation record
        donation = Donation(
            project_id=project_id,
            donor_name=donor_name,
            donor_email=donor_email,
            amount=amount,
            message=message,
            is_anonymous=is_anonymous,
            payment_method=payment_method,
            status='pending'
        )
        
        db.session.add(donation)
        db.session.commit()
        
        # In a real implementation, you would integrate with payment processors here
        # For now, we'll simulate a successful payment
        donation.status = 'completed'
        donation.payment_id = f"sim_{datetime.now().timestamp()}"
        
        # Update project total
        project.current_amount += amount
        db.session.commit()
        
        # Send confirmation email
        try:
            email_service.send_donation_confirmation(
                donor_email, donor_name, project.title, amount
            )
        except Exception as e:
            logger.error(f"Failed to send confirmation email: {e}")
        
        flash(f'Thank you for your donation of ${amount:.2f} to {project.title}!', 'success')
        return redirect(url_for('donation.project_detail', project_id=project_id))
        
    except ValueError:
        flash('Invalid donation amount.', 'error')
        return redirect(url_for('donation.project_detail', project_id=project_id))
    except Exception as e:
        logger.error(f"Donation processing error: {e}")
        flash('An error occurred while processing your donation. Please try again.', 'error')
        return redirect(url_for('donation.project_detail', project_id=project_id))

@donation_bp.route('/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter"""
    try:
        email = request.form.get('email', '').strip().lower()
        name = request.form.get('name', '').strip()
        interests = request.form.get('interests', '').strip()
        
        if not email:
            flash('Please provide a valid email address.', 'error')
            return redirect(url_for('donation.index'))
        
        # Check if already subscribed
        existing = NewsletterSubscriber.query.filter_by(email=email).first()
        if existing:
            if existing.is_active:
                flash('You are already subscribed to our newsletter.', 'info')
            else:
                existing.is_active = True
                existing.name = name or existing.name
                existing.interests = interests or existing.interests
                db.session.commit()
                flash('Your newsletter subscription has been reactivated.', 'success')
        else:
            subscriber = NewsletterSubscriber(
                email=email,
                name=name,
                interests=interests
            )
            db.session.add(subscriber)
            db.session.commit()
            flash('Thank you for subscribing to our newsletter!', 'success')
        
        return redirect(url_for('donation.index'))
        
    except Exception as e:
        logger.error(f"Newsletter subscription error: {e}")
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

# ...existing routes continue...

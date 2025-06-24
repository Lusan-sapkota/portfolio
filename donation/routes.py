from flask import render_template, request, jsonify, flash, redirect, url_for, current_app
from . import donation_bp
from models import DonationProject, Donation, NewsletterSubscriber, PaymentMethod, ThanksgivingSettings, DonationSettings, db
from email_service import email_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@donation_bp.route('/')
def index():
    """Main donation page showing all active projects"""
    from models import SeoSettings, PersonalInfo, SocialLink
    
    # Get SEO settings for donation page
    seo_settings = SeoSettings.query.filter_by(page_name='donation').first()
    personal_info = PersonalInfo.query.first()
    
    # Get donation projects and regular projects - combine both for comprehensive display
    try:
        from models import Project
        
        # Get DonationProjects (specific donation campaigns)
        donation_featured = DonationProject.query.filter_by(is_active=True, is_featured=True).all()
        donation_all = DonationProject.query.filter_by(is_active=True).all()
        
        # Get regular Projects that can also accept donations
        regular_featured = Project.query.filter_by(is_featured=True).all()
        regular_all = Project.query.all()
        
        # Combine both types for comprehensive project lists
        featured_projects = donation_featured + regular_featured
        all_projects = donation_all + regular_all
        
        # Remove duplicates if any (unlikely but safe)
        featured_projects = list({p.id: p for p in featured_projects}.values())
        all_projects = list({p.id: p for p in all_projects}.values())
        
        logger.info(f"Loaded {len(donation_all)} DonationProjects + {len(regular_all)} regular Projects")
        logger.info(f"Featured: {len(donation_featured)} donation + {len(regular_featured)} regular")
        
        # Get recent donations for activity feed - only completed donations
        recent_donations = Donation.query.filter_by(status='completed')\
                                       .order_by(Donation.created_at.desc())\
                                       .limit(10).all()
        
    except Exception as e:
        logger.error(f"Error loading projects: {e}")
        featured_projects = []
        all_projects = []
        recent_donations = []
    
    # Calculate real-time statistics
    try:
        # Count all available projects (both donation and regular)
        project_count = len(all_projects)
        
        # Calculate total raised in different currencies
        total_usd = db.session.query(db.func.sum(Donation.amount)).filter(
            Donation.status == 'completed',
            Donation.currency == 'USD'
        ).scalar() or 0
        
        total_npr = db.session.query(db.func.sum(Donation.amount)).filter(
            Donation.status == 'completed',
            Donation.currency == 'NPR'
        ).scalar() or 0
        
        # Format the totals for display with proper currency symbols
        total_raised_display = ""
        if total_usd > 0 and total_npr > 0:
            total_raised_display = f"${total_usd:,.2f} / Rs.{total_npr:,.2f}"
        elif total_usd > 0:
            total_raised_display = f"${total_usd:,.2f}"
        elif total_npr > 0:
            total_raised_display = f"Rs.{total_npr:,.2f}"
        else:
            total_raised_display = "$0 / Rs.0"
        
        # Count unique supporters
        supporter_count = db.session.query(db.func.count(db.func.distinct(Donation.donor_email))).filter_by(status='completed').scalar() or 0
        
    except Exception as e:
        logger.error(f"Error calculating statistics: {e}")
        project_count = len(all_projects) if all_projects else 0
        total_raised_display = "$0 / Rs.0"
        supporter_count = 0
    
    # Get CMS data
    seo = SeoSettings.query.filter_by(page_name='donation').first() or SeoSettings.query.first()
    personal = PersonalInfo.query.first()
    social_links = SocialLink.query.all()
    
    return render_template('donation/donation.html', 
                         featured_projects=featured_projects,
                         all_projects=all_projects,
                         recent_donations=recent_donations,
                         seo_settings=seo_settings,
                         personal_info=personal_info,
                         social_links=social_links,
                         project_count=project_count,
                         total_raised=total_raised_display,
                         supporter_count=supporter_count,
                         current_year=datetime.now().year)

@donation_bp.route('/project/<int:project_id>')
def project_detail(project_id):
    """Detailed view of a specific donation project (supports both DonationProject and regular Project)"""
    from models import SeoSettings, PersonalInfo, Project
    
    project = None
    donations = []
    project_type = "donation"  # Track which type of project this is
    
    # Try DonationProject first
    try:
        project = DonationProject.query.filter_by(id=project_id, is_active=True).first()
        if project:
            # Get recent donations for this donation project - show all statuses for admin visibility
            donations = Donation.query.filter_by(project_id=project_id)\
                                     .order_by(Donation.created_at.desc())\
                                     .limit(20).all()
            logger.info(f"Loaded DonationProject: {project.title}")
        else:
            project_type = "regular"
    except Exception as e:
        logger.error(f"Error loading DonationProject {project_id}: {e}")
        project_type = "regular"
    
    # If no DonationProject found, try regular Project
    if not project:
        try:
            project = Project.query.get_or_404(project_id)
            # For regular projects, we might not have direct donations, but show any that exist
            donations = Donation.query.filter_by(project_id=project_id)\
                                     .order_by(Donation.created_at.desc())\
                                     .limit(20).all()
            logger.info(f"Loaded regular Project: {project.title}")
        except Exception as e:
            logger.error(f"Could not load any project with ID {project_id}: {e}")
            from flask import abort
            abort(404)
    
    # Get available payment methods - sorted by currency and status
    try:
        payment_methods = PaymentMethod.query.filter_by(is_active=True)\
                                            .order_by(PaymentMethod.currency, 
                                                     PaymentMethod.is_verification_pending,
                                                     PaymentMethod.sort_order).all()
        
        # Separate by currency for better organization
        npr_methods = [pm for pm in payment_methods if pm.currency == 'NPR']
        usd_methods = [pm for pm in payment_methods if pm.currency == 'USD']
        
        logger.info(f"Payment methods available: {len(npr_methods)} NPR, {len(usd_methods)} USD")
        
    except Exception as e:
        logger.error(f"Error loading payment methods: {e}")
        payment_methods = []
        npr_methods = []
        usd_methods = []
    
    # Get CMS data
    seo = SeoSettings.query.filter_by(page_name='donation').first() or SeoSettings.query.first()
    personal = PersonalInfo.query.first()
    
    return render_template('donation/project_detail.html', 
                         project=project,
                         project_type=project_type,
                         donations=donations,
                         payment_methods=payment_methods,
                         npr_methods=npr_methods,
                         usd_methods=usd_methods,
                         seo=seo,
                         personal=personal,
                         current_year=datetime.now().year)

@donation_bp.route('/donate/<int:project_id>', methods=['GET', 'POST'])
def donate(project_id):
    """Handle donation submission for a specific project (supports both project types)"""
    from models import SeoSettings, PersonalInfo, SocialLink, Project
    
    # Try to get the project (DonationProject or regular Project)
    project = None
    try:
        project = DonationProject.query.filter_by(id=project_id, is_active=True).first()
        if not project:
            project = Project.query.get_or_404(project_id)
    except:
        from flask import abort
        abort(404)
    
    if request.method == 'POST':
        try:
            # Get form data
            donor_name = request.form.get('donor_name', '').strip()
            donor_email = request.form.get('donor_email', '').strip()
            donor_phone = request.form.get('donor_phone', '').strip()
            amount = float(request.form.get('amount', 0))
            currency = request.form.get('currency', 'NPR').upper()
            message = request.form.get('message', '').strip()
            is_anonymous = bool(request.form.get('is_anonymous'))
            payment_method = request.form.get('payment_method', 'manual')
            
            # Validate required fields
            if not donor_name or not donor_email or amount <= 0:
                if request.is_json:
                    return jsonify({'success': False, 'message': 'Please fill in all required fields'}), 400
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('donation.project_detail', project_id=project_id))
            
            # Validate currency
            if currency not in ['NPR', 'USD']:
                currency = 'NPR'  # Default fallback
            
            # Validate payment method exists for the selected currency
            selected_payment_method = PaymentMethod.query.filter_by(
                method_name=payment_method, 
                currency=currency, 
                is_active=True
            ).first()
            
            if not selected_payment_method:
                flash(f'Selected payment method is not available for {currency}', 'error')
                return redirect(url_for('donation.project_detail', project_id=project_id))
            
            # Create donation record
            donation = Donation(
                project_id=project_id,
                donor_name=donor_name,
                donor_email=donor_email,
                donor_phone=donor_phone,
                amount=amount,
                currency=currency,
                message=message,
                is_anonymous=is_anonymous,
                payment_method=payment_method,
                status='pending'  # Start as pending, admin can mark as completed
            )
            
            db.session.add(donation)
            db.session.commit()
            
            # Send thank you email to donor
            try:
                if email_service:
                    email_service.send_donation_thank_you(
                        donor_email, 
                        donor_name, 
                        amount, 
                        project.title,
                        currency
                    )
            except Exception as e:
                logger.error(f"Failed to send thank you email: {e}")
            
            # Send admin notification email
            try:
                if email_service:
                    email_service.send_admin_donation_notification(
                        donation,
                        project.title
                    )
            except Exception as e:
                logger.error(f"Failed to send admin notification email: {e}")
            
            if request.is_json:
                return jsonify({
                    'success': True, 
                    'message': 'Thank you for your donation! Your contribution is being processed.',
                    'donation_id': donation.id
                })
            
            flash('Thank you for your donation! Please complete the payment using the instructions below.', 'success')
            return redirect(url_for('donation.payment_instructions', donation_id=donation.id))
            
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
    
    return render_template('donation/project_detail.html',
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
    
    return render_template('donation/donation_success.html',
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
                    return jsonify({'success': False, 'status': 'info', 'message': 'You are already subscribed to my newsletter.'})
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
                return jsonify({'success': True, 'status': 'success', 'message': 'Thank you for subscribing to my newsletter!'})
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
    from models import SeoSettings, PersonalInfo, Project
    
    # Get featured and completed donation projects
    featured_projects = DonationProject.query.filter_by(is_featured=True).all()
    completed_projects = DonationProject.query.filter(
        DonationProject.current_amount >= DonationProject.goal_amount
    ).all()
    
    # Calculate real-time statistics for achievements
    try:
        # Get all donation projects and regular projects
        all_donation_projects = DonationProject.query.filter_by(is_active=True).all()
        all_regular_projects = Project.query.all()
        
        # Total project count (both donation and regular projects)
        total_projects = len(all_donation_projects) + len(all_regular_projects)
        
        # Count completed donation projects
        completed_count = len(completed_projects)
        
        # Count featured projects (both donation and regular)
        featured_donation_count = len(featured_projects)
        featured_regular_count = Project.query.filter_by(is_featured=True).count()
        total_featured = featured_donation_count + featured_regular_count
        
        # Calculate total raised in different currencies
        total_usd = db.session.query(db.func.sum(Donation.amount)).filter(
            Donation.status == 'completed',
            Donation.currency == 'USD'
        ).scalar() or 0
        
        total_npr = db.session.query(db.func.sum(Donation.amount)).filter(
            Donation.status == 'completed',
            Donation.currency == 'NPR'
        ).scalar() or 0
        
        # Format the totals for display with proper currency symbols
        if total_usd > 0 and total_npr > 0:
            total_raised_display = f"${total_usd:,.0f} / Rs.{total_npr:,.0f}"
        elif total_usd > 0:
            total_raised_display = f"${total_usd:,.0f}"
        elif total_npr > 0:
            total_raised_display = f"Rs.{total_npr:,.0f}"
        else:
            total_raised_display = "$0 / Rs.0"
        
        # Count unique supporters
        supporter_count = db.session.query(db.func.count(db.func.distinct(Donation.donor_email))).filter_by(status='completed').scalar() or 0
        
        # Prepare achievement stats
        achievement_stats = {
            'total_projects': total_projects,
            'completed_projects': completed_count,
            'featured_projects': total_featured,
            'total_raised_display': total_raised_display,
            'total_usd': total_usd,
            'total_npr': total_npr,
            'supporter_count': supporter_count
        }
        
    except Exception as e:
        logger.error(f"Error calculating achievement statistics: {e}")
        # Fallback to basic counts
        achievement_stats = {
            'total_projects': len(featured_projects) + len(completed_projects),
            'completed_projects': len(completed_projects),
            'featured_projects': len(featured_projects),
            'total_raised_display': "$0 / Rs.0",
            'total_usd': 0,
            'total_npr': 0,
            'supporter_count': 0
        }
    
    return render_template('donation/highlight.html',
                         featured_projects=featured_projects,
                         completed_projects=completed_projects,
                         achievement_stats=achievement_stats,
                         current_year=datetime.now().year)

@donation_bp.route('/thanksgiving')
def thanksgiving():
    """Thanksgiving page showing donor recognition"""
    from models import SeoSettings, PersonalInfo, ThanksgivingSettings
    
    # Get thanksgiving settings
    thanksgiving_settings = ThanksgivingSettings.query.filter_by(is_active=True).first()
    if not thanksgiving_settings:
        # Default settings if none exist
        thanksgiving_settings = ThanksgivingSettings(
            page_title='Thank You to My Amazing Supporters',
            page_description='I am grateful for the incredible support from my community. Your contributions make my projects possible and help me build technology that makes a difference.',
            thank_you_message='Thank you for believing in my work and supporting my projects. Every contribution, no matter the size, makes a real difference and helps me continue building technology that matters.',
            show_donor_names=True,
            show_amounts=False,
            show_messages=True,
            min_amount_display=0,
            anonymous_display_text='Anonymous Supporter',
            is_active=True
        )
    
    # Get donations for display based on settings
    query = Donation.query.filter_by(status='completed')
    
    # Check if min_amount_display is set and greater than 0
    if thanksgiving_settings.min_amount_display and thanksgiving_settings.min_amount_display > 0:
        query = query.filter(Donation.verified_amount >= thanksgiving_settings.min_amount_display)
    
    donations = query.order_by(Donation.created_at.desc()).all()
    
    # Filter donations based on display settings
    display_donations = []
    for donation in donations:
        donation_data = {
            'donor_name': donation.donor_name if not donation.is_anonymous and thanksgiving_settings.show_donor_names else thanksgiving_settings.anonymous_display_text,
            'amount': donation.verified_amount or donation.amount if thanksgiving_settings.show_amounts else None,
            'currency': donation.currency,  # Always include currency for statistics
            'message': donation.message if thanksgiving_settings.show_messages and donation.message else None,
            'created_at': donation.created_at,
            'project_title': donation.project.title if donation.project else None
        }
        display_donations.append(donation_data)
    
    # Get CMS data
    seo = SeoSettings.query.filter_by(page_name='thanksgiving').first() or SeoSettings.query.first()
    personal = PersonalInfo.query.first()
    
    return render_template('donation/thanksgiving.html', 
                         donations=display_donations,
                         thanksgiving_settings=thanksgiving_settings,
                         seo_settings=seo,
                         personal_info=personal,
                         current_year=datetime.now().year)

@donation_bp.route('/why-donate/<int:project_id>')
def why_donate(project_id):
    """Page explaining why someone should donate to a specific project"""
    project = DonationProject.query.get_or_404(project_id)
    return render_template('donation/why_donate.html',
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
                    project.title,
                    donation.currency
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

@donation_bp.route('/payment/<int:donation_id>')
def payment_instructions(donation_id):
    """Show payment instructions after donation submission"""
    from models import SeoSettings, PersonalInfo, PaymentMethod, DonationSettings
    
    donation = Donation.query.get_or_404(donation_id)
    
    # Get payment methods for the selected currency
    payment_methods = PaymentMethod.query.filter_by(
        currency=donation.currency, 
        is_active=True
    ).order_by(PaymentMethod.sort_order).all()
    
    # Get donation settings
    settings = DonationSettings.query.first()
    
    # Get CMS data
    seo = SeoSettings.query.filter_by(page_name='donation').first() or SeoSettings.query.first()
    personal = PersonalInfo.query.first()
    
    return render_template('donation/donation_payment.html', 
                         donation=donation,
                         payment_methods=payment_methods,
                         settings=settings,
                         seo_settings=seo,
                         personal_info=personal,
                         current_year=datetime.now().year)

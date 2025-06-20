from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for
import re
from urllib.parse import urlparse

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class ProjectCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # For FontAwesome icons
    color = db.Column(db.String(7))  # Hex color
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Projects in this category
    projects = db.relationship('Project', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<ProjectCategory {self.name}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    live_url = db.Column(db.String(255))
    commercial_url = db.Column(db.String(255))  # For commercial product links
    technologies = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('project_category.id'))
    is_featured = db.Column(db.Boolean, default=False)
    is_opensource = db.Column(db.Boolean, default=True)
    show_on_homepage = db.Column(db.Boolean, default=True)  # Control home page display
    stars = db.Column(db.Integer, default=0)
    forks = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime)
    github_data_updated = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='completed')  # completed, in-progress, maintenance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Project {self.title}>'
    
    def extract_github_repo(self):
        """Extract username and repo name from GitHub URL"""
        if not self.github_url:
            return None, None
            
        # Handle various GitHub URL formats
        patterns = [
            r'github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$',
            r'github\.com/([^/]+)/([^/]+?)(?:/.*)?$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.github_url)
            if match:
                username, repo = match.groups()
                # Remove .git suffix if present
                repo = repo.replace('.git', '')
                return username, repo
        
        return None, None
    
    def fetch_github_data(self):
        """Fetch data from GitHub API using the caching service"""
        username, repo = self.extract_github_repo()
        if not username or not repo:
            return False
        
        try:
            # Import here to avoid circular imports
            from github_service import github_service
            
            # Get data from the caching service
            github_data = github_service.get_repository_data(username, repo)
            
            if github_data:
                # Update project data from GitHub
                self.stars = github_data.get('stargazers_count', 0)
                self.forks = github_data.get('forks_count', 0)
                
                # Update last_updated from GitHub's updated_at
                if github_data.get('updated_at'):
                    try:
                        # Handle GitHub's ISO format
                        github_updated = datetime.fromisoformat(
                            github_data.get('updated_at').replace('Z', '+00:00')
                        )
                        self.last_updated = github_updated
                    except (ValueError, AttributeError):
                        pass
                
                # Update description if not set locally
                if not self.description and github_data.get('description'):
                    self.description = github_data.get('description')
                
                # Update github_data_updated timestamp
                self.github_data_updated = datetime.utcnow()
                
                print(f"Successfully updated GitHub data for {username}/{repo}")
                return True
            else:
                print(f"No GitHub data available for {username}/{repo} (cached error or not found)")
                # Still update the timestamp to avoid repeated attempts
                self.github_data_updated = datetime.utcnow()
                return False
                
        except Exception as e:
            print(f"Error updating GitHub data for {username}/{repo}: {e}")
            return False
    
    def should_update_github_data(self):
        """Check if GitHub data should be updated (every 24 hours)"""
        if not self.github_data_updated:
            return True
            
        from datetime import timedelta
        return datetime.utcnow() - self.github_data_updated > timedelta(hours=24)

class WikiArticle(db.Model):
    __tablename__ = 'wiki_article'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('wiki_category.id'), nullable=True)
    tags = db.Column(db.String(200))
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<WikiArticle {self.title}>'
    
    def strip_html(self, text):
        """Remove HTML tags from text"""
        if not text:
            return ""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    
    def get_excerpt(self, length=200):
        """Get a clean text excerpt without HTML tags"""
        if self.summary:
            return self.strip_html(self.summary)
        elif self.content:
            clean_content = self.strip_html(self.content)
            if len(clean_content) > length:
                return clean_content[:length] + '...'
            return clean_content
        return "No content available"
    
    def get_reading_time(self):
        """Estimate reading time in minutes"""
        if self.content:
            word_count = len(self.strip_html(self.content).split())
            return max(1, word_count // 200)  # Assume 200 words per minute
        return 1
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'excerpt': self.get_excerpt(),
            'category_id': self.category_id,
            'tags': self.tags,
            'views': self.views,
            'reading_time': self.get_reading_time(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WikiCategory(db.Model):
    __tablename__ = 'wiki_category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('wiki_category.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    subcategories = db.relationship('WikiCategory', backref=db.backref('parent', remote_side=[id]))
    articles = db.relationship('WikiArticle', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<WikiCategory {self.name}>'
    
    @property
    def article_count(self):
        return self.articles.count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'article_count': self.article_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default="Lusan's Portfolio")
    meta_description = db.Column(db.String(255))
    contact_email = db.Column(db.String(120))
    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    twitter_url = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DonationProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(500))
    goal_amount = db.Column(db.Float, default=0.0)
    current_amount = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    demo_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with donations
    donations = db.relationship('Donation', backref='project', lazy='dynamic')
    
    def __repr__(self):
        return f'<DonationProject {self.title}>'
    
    def get_progress_percentage(self):
        if self.goal_amount == 0:
            return 0
        return min(100, (self.current_amount / self.goal_amount) * 100)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'short_description': self.short_description,
            'goal_amount': self.goal_amount,
            'current_amount': self.current_amount,
            'progress_percentage': self.get_progress_percentage(),
            'image_url': self.image_url,
            'github_url': self.github_url,
            'demo_url': self.demo_url,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('donation_project.id'), nullable=False)
    donor_name = db.Column(db.String(100), nullable=False)
    donor_email = db.Column(db.String(120), nullable=False)
    donor_phone = db.Column(db.String(20))  # Phone for verification (not shown publicly)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='NPR')  # NPR or USD
    message = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.String(50))  # wallet, bank_transfer, swift_transfer, payoneer
    payment_id = db.Column(db.String(100))  # external payment ID
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    verified_amount = db.Column(db.Float)  # Amount actually received (can differ from requested)
    admin_notes = db.Column(db.Text)  # Admin notes about the donation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Donation {self.amount} {self.currency} for {self.project.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'donor_name': self.donor_name if not self.is_anonymous else 'Anonymous',
            'amount': self.amount,
            'currency': self.currency,
            'verified_amount': self.verified_amount,
            'message': self.message,
            'is_anonymous': self.is_anonymous,
            'payment_method': self.payment_method,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class NewsletterSubscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    interests = db.Column(db.String(500))  # comma-separated interests
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_email_sent = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'is_active': self.is_active,
            'interests': self.interests.split(',') if self.interests else [],
            'subscribed_at': self.subscribed_at.isoformat() if self.subscribed_at else None
        }

class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    user_agent = db.Column(db.String(500))
    is_spam = db.Column(db.Boolean, default=False)
    is_replied = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    replied_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<ContactSubmission {self.name} - {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'is_spam': self.is_spam,
            'is_replied': self.is_replied,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None
        }

class SeoSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(100), unique=True, nullable=False)  # 'home', 'about', 'contact', etc.
    title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    meta_keywords = db.Column(db.Text)
    og_title = db.Column(db.String(200))
    og_description = db.Column(db.Text)
    og_image = db.Column(db.String(255))
    canonical_url = db.Column(db.String(255))
    robots = db.Column(db.String(100), default='index, follow')
    schema_markup = db.Column(db.Text)  # JSON-LD structured data
    is_active = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SeoSettings {self.page_name}>'

class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200))
    bio = db.Column(db.Text)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    profile_image = db.Column(db.String(255))
    resume_url = db.Column(db.String(255))
    location = db.Column(db.String(100))
    tagline = db.Column(db.String(200))
    years_experience = db.Column(db.Integer)
    projects_completed = db.Column(db.Integer)
    clients_served = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PersonalInfo {self.name}>'

class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)  # github, linkedin, twitter, etc.
    url = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50))  # FontAwesome icon class
    display_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SocialLink {self.platform}>'

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # programming, frontend, backend, database, etc.
    proficiency = db.Column(db.Integer)  # 1-100 percentage
    icon = db.Column(db.String(50))
    description = db.Column(db.Text)
    years_experience = db.Column(db.Float)
    is_featured = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Skill {self.name}>'

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)  # NULL means current position
    location = db.Column(db.String(100))
    company_url = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))
    technologies = db.Column(db.Text)  # Comma-separated
    achievements = db.Column(db.Text)  # JSON or formatted text
    is_current = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Experience {self.company} - {self.position}>'

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    field_of_study = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    grade = db.Column(db.String(20))
    location = db.Column(db.String(100))
    institution_url = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))
    is_current = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Education {self.institution} - {self.degree}>'

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_title = db.Column(db.String(100))
    client_company = db.Column(db.String(100))
    testimonial_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    client_image = db.Column(db.String(255))
    project_related = db.Column(db.String(100))
    is_featured = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Testimonial {self.client_name}>'

class PaymentMethod(db.Model):
    """Payment methods configuration for different currencies"""
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False)  # NPR or USD
    method_name = db.Column(db.String(50), nullable=False)  # wallet, bank_transfer, etc.
    display_name = db.Column(db.String(100), nullable=False)  # "eSewa Wallet"
    account_info = db.Column(db.Text)  # Account details
    qr_code_url = db.Column(db.String(255))  # QR code image URL
    instructions = db.Column(db.Text)  # Payment instructions
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PaymentMethod {self.currency} - {self.display_name}>'

class ThanksgivingSettings(db.Model):
    """Settings for the thanksgiving/donor recognition page"""
    id = db.Column(db.Integer, primary_key=True)
    page_title = db.Column(db.String(200), default='Thank You to Our Amazing Supporters')
    page_description = db.Column(db.Text, default='We are grateful for the incredible support from our community.')
    show_donor_names = db.Column(db.Boolean, default=True)
    show_amounts = db.Column(db.Boolean, default=False)
    show_messages = db.Column(db.Boolean, default=True)
    min_amount_display = db.Column(db.Float, default=0.0)  # Minimum amount to display
    anonymous_display_text = db.Column(db.String(100), default='Anonymous Supporter')
    thank_you_message = db.Column(db.Text, default='Your support means the world to us and helps keep our projects alive!')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ThanksgivingSettings {self.page_title}>'

class DonationSettings(db.Model):
    """General donation system settings"""
    id = db.Column(db.Integer, primary_key=True)
    default_currency = db.Column(db.String(3), default='NPR')
    enable_custom_amounts = db.Column(db.Boolean, default=True)
    enable_anonymous_donations = db.Column(db.Boolean, default=True)
    require_phone_verification = db.Column(db.Boolean, default=False)
    thank_you_email_template = db.Column(db.Text)
    admin_notification_emails = db.Column(db.String(500))  # Comma-separated emails
    auto_approve_donations = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DonationSettings {self.default_currency}>'
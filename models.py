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
    technologies = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('project_category.id'))
    is_featured = db.Column(db.Boolean, default=False)
    is_opensource = db.Column(db.Boolean, default=True)
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
    amount = db.Column(db.Float, nullable=False)
    message = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.String(50))  # paypal, stripe, etc.
    payment_id = db.Column(db.String(100))  # external payment ID
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Donation {self.amount} for {self.project.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'donor_name': self.donor_name if not self.is_anonymous else 'Anonymous',
            'amount': self.amount,
            'message': self.message,
            'is_anonymous': self.is_anonymous,
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
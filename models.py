from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for

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

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    live_url = db.Column(db.String(255))
    technologies = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Project {self.title}>'

class WikiCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('wiki_category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for hierarchy
    subcategories = db.relationship(
        'WikiCategory', 
        backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic'
    )
    
    # Articles in this category
    articles = db.relationship('WikiArticle', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<WikiCategory {self.name}>'
    
    def to_dict(self):
        """Serializes the object to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'subcategories': [cat.to_dict() for cat in self.subcategories],
            'articles': [article.to_dict() for article in self.articles]
        }

class WikiArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200))  # Comma-separated tags
    category_id = db.Column(db.Integer, db.ForeignKey('wiki_category.id'))  # Add this line
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<WikiArticle {self.title}>'

    def to_dict(self):
        """Serializes the object to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'category_id': self.category_id,
            # Return a snippet of content for search results
            'content_snippet': (self.content[:150] + '...') if len(self.content) > 150 else self.content,
            'tags': self.tags,
            # Generate the URL for the article view
            'url': url_for('wiki.article', article_id=self.id, _external=False)
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
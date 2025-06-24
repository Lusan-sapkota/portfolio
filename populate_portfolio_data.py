#!/usr/bin/env python3
"""
Populate Portfolio Database with Sample Data
This script adds sample projects and categories to the portfolio database.
"""

import os
from app import app
from database import db
from models import Project, ProjectCategory

def create_sample_categories():
    """Create sample project categories"""
    categories = [
        {
            'name': 'Web Apps',
            'description': 'Full-stack web applications and services',
            'icon': 'fas fa-globe',
            'color': '#3498db'
        },
        {
            'name': 'AI/ML',
            'description': 'Artificial Intelligence and Machine Learning projects',
            'icon': 'fas fa-robot',
            'color': '#e74c3c'
        },
        {
            'name': 'Mobile',
            'description': 'Mobile applications and responsive designs',
            'icon': 'fas fa-mobile-alt',
            'color': '#2ecc71'
        },
        {
            'name': 'Tools',
            'description': 'Developer tools and utilities',
            'icon': 'fas fa-tools',
            'color': '#f39c12'
        }
    ]
    
    created_categories = {}
    for cat_data in categories:
        existing = ProjectCategory.query.filter_by(name=cat_data['name']).first()
        if not existing:
            category = ProjectCategory(**cat_data)
            db.session.add(category)
            db.session.commit()
            created_categories[cat_data['name']] = category
            print(f"Created category: {cat_data['name']}")
        else:
            created_categories[cat_data['name']] = existing
            print(f"Category already exists: {cat_data['name']}")
    
    return created_categories

def create_sample_projects(categories):
    """Create sample projects"""
    projects_data = [
        {
            'title': 'Ambulance Tracking System',
            'description': 'Real-time ambulance tracking system with GPS integration, optimizing emergency response times and resource allocation.',
            'image_url': '/static/assets/images/portfolio/p1.png',
            'github_url': 'https://github.com/Lusan-sapkota/Ambulance-tracking-system',
            'live_url': None,
            'technologies': 'Python,Flask,JavaScript,GPS API',
            'category': 'Web Apps',
            'is_featured': True,
            'status': 'completed'
        },
        {
            'title': 'Face Recognition Attendance',
            'description': 'AI-powered attendance system using computer vision and machine learning for automated student/employee tracking.',
            'image_url': '/static/assets/images/portfolio/p2.png',
            'github_url': 'https://github.com/Lusan-sapkota/Face-Recognition-Based-Attendance-System',
            'live_url': None,
            'technologies': 'Python,OpenCV,Machine Learning,Computer Vision',
            'category': 'AI/ML',
            'is_featured': True,
            'status': 'completed'
        },
        {
            'title': 'Task Master',
            'description': 'Comprehensive task management application with team collaboration features, real-time updates, and productivity analytics.',
            'image_url': '/static/assets/images/portfolio/p3.png',
            'github_url': 'https://github.com/Lusan-sapkota/Task-Master',
            'live_url': None,
            'technologies': 'React,Node.js,MongoDB,Socket.io',
            'category': 'Web Apps',
            'is_featured': True,
            'status': 'completed'
        },
        {
            'title': 'Jarvis AI Assistant',
            'description': 'Intelligent voice-activated assistant with natural language processing, automation capabilities, and smart home integration.',
            'image_url': '/static/assets/images/portfolio/p4.png',
            'github_url': 'https://github.com/Lusan-sapkota/Jarvis',
            'live_url': None,
            'technologies': 'Python,NLP,Speech Recognition,AI/ML',
            'category': 'AI/ML',
            'is_featured': True,
            'status': 'completed'
        },
        {
            'title': 'Chat History Master',
            'description': 'Advanced chat management system with search, backup, and analytics features for multiple messaging platforms.',
            'image_url': '/static/assets/images/portfolio/p5.png',
            'github_url': 'https://github.com/Lusan-sapkota/Chat-History_Master',
            'live_url': None,
            'technologies': 'Django,PostgreSQL,Redis,API Integration',
            'category': 'Web Apps',
            'is_featured': True,
            'status': 'completed'
        },
        {
            'title': 'Modern Portfolio Website',
            'description': 'Responsive developer portfolio with modern design, subdomain architecture, and integrated project showcase.',
            'image_url': '/static/assets/images/portfolio/portfolio-site.jpg',
            'github_url': 'https://github.com/Lusan-sapkota/portfolio',
            'live_url': 'https://lusansapkota.com.np',
            'technologies': 'Flask,JavaScript,CSS3,Bootstrap',
            'category': 'Web Apps',
            'is_featured': True,
            'status': 'completed'
        }
    ]
    
    for project_data in projects_data:
        # Check if project already exists
        existing = Project.query.filter_by(title=project_data['title']).first()
        if existing:
            print(f"Project already exists: {project_data['title']}")
            continue
        
        # Get category
        category_name = project_data.pop('category')
        category = categories.get(category_name)
        
        # Create project
        project = Project(
            **project_data,
            category_id=category.id if category else None
        )
        
        db.session.add(project)
        print(f"Created project: {project_data['title']}")
    
    db.session.commit()

def populate_portfolio_database():
    """Main function to populate the database"""
    print("Starting portfolio database population...")
    
    try:
        # Create categories first
        categories = create_sample_categories()
        
        # Create projects
        create_sample_projects(categories)
        
        print("\n✅ Portfolio database populated successfully!")
        print(f"Created {len(categories)} categories")
        print(f"Project count in database: {Project.query.count()}")
        
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Populate with sample data
        populate_portfolio_database()

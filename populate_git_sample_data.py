#!/usr/bin/env python3
"""
Sample data for Git section - Project Categories and Projects
"""

from database import db
from models import Project, ProjectCategory
from datetime import datetime

def populate_git_sample_data():
    """Populate sample project categories and projects"""
    
    print("🔧 Populating Git section sample data...")
    
    # Check if categories already exist
    if ProjectCategory.query.first():
        print("📋 Project categories already exist, skipping...")
    else:
        # Create sample categories
        categories = [
            {
                'name': 'Web Development',
                'description': 'Full-stack web applications and websites',
                'icon': 'fas fa-globe-americas',
                'color': '#f39c12'
            },
            {
                'name': 'Mobile Apps',
                'description': 'iOS and Android mobile applications',
                'icon': 'fas fa-mobile-alt',
                'color': '#e74c3c'
            },
            {
                'name': 'Data Science',
                'description': 'Machine learning and data analysis projects',
                'icon': 'fas fa-chart-line',
                'color': '#3498db'
            },
            {
                'name': 'DevOps',
                'description': 'Infrastructure and deployment automation',
                'icon': 'fas fa-server',
                'color': '#2ecc71'
            },
            {
                'name': 'Open Source',
                'description': 'Community-driven open source projects',
                'icon': 'fab fa-osi',
                'color': '#9b59b6'
            },
            {
                'name': 'Commercial',
                'description': 'Client work and commercial solutions',
                'icon': 'fas fa-briefcase',
                'color': '#34495e'
            },
            {
                'name': 'API Development',
                'description': 'RESTful APIs and microservices',
                'icon': 'fas fa-plug',
                'color': '#f1c40f'
            },
            {
                'name': 'Desktop Apps',
                'description': 'Cross-platform desktop applications',
                'icon': 'fas fa-desktop',
                'color': '#95a5a6'
            }
        ]
        
        for cat_data in categories:
            category = ProjectCategory(
                name=cat_data['name'],
                description=cat_data['description'],
                icon=cat_data['icon'],
                color=cat_data['color']
            )
            db.session.add(category)
        
        db.session.commit()
        print("✅ Created sample project categories")
    
    # Get categories for reference
    web_dev = ProjectCategory.query.filter_by(name='Web Development').first()
    mobile = ProjectCategory.query.filter_by(name='Mobile Apps').first()
    data_science = ProjectCategory.query.filter_by(name='Data Science').first()
    devops = ProjectCategory.query.filter_by(name='DevOps').first()
    opensource = ProjectCategory.query.filter_by(name='Open Source').first()
    commercial = ProjectCategory.query.filter_by(name='Commercial').first()
    api_dev = ProjectCategory.query.filter_by(name='API Development').first()
    desktop = ProjectCategory.query.filter_by(name='Desktop Apps').first()
    
    # Check if projects already exist
    if Project.query.first():
        print("📋 Projects already exist, updating with new fields...")
        
        # Update existing projects with new fields
        projects = Project.query.all()
        for i, project in enumerate(projects):
            if not hasattr(project, 'category_id') or project.category_id is None:
                # Assign categories based on project index
                categories_list = [web_dev, mobile, data_science, devops, opensource, api_dev]
                project.category_id = categories_list[i % len(categories_list)].id if categories_list else None
            
            if not hasattr(project, 'is_featured') or project.is_featured is None:
                project.is_featured = (i % 3 == 0)  # Every 3rd project is featured
            
            if not hasattr(project, 'is_opensource') or project.is_opensource is None:
                project.is_opensource = True
            
            if not hasattr(project, 'stars') or project.stars is None:
                project.stars = (i + 1) * 5  # Some sample stars
            
            if not hasattr(project, 'status') or project.status is None:
                statuses = ['completed', 'in-progress', 'maintenance']
                project.status = statuses[i % len(statuses)]
        
        db.session.commit()
        print("✅ Updated existing projects with new fields")
    
    else:
        # Create sample projects
        sample_projects = [
            {
                'title': 'Portfolio Website',
                'description': 'A modern, responsive portfolio website built with Flask and featuring dynamic content management, beautiful animations, and multiple sections including projects, blog, and contact forms.',
                'image_url': '/static/assets/images/portfolio/portfolio-website.jpg',
                'github_url': 'https://github.com/lusansapkota/portfolio',
                'live_url': 'https://lusansapkota.com',
                'technologies': 'Python, Flask, HTML5, CSS3, JavaScript, Bootstrap, SQLAlchemy',
                'category_id': web_dev.id if web_dev else None,
                'is_featured': True,
                'is_opensource': True,
                'stars': 25,
                'status': 'completed'
            },
            {
                'title': 'Task Management API',
                'description': 'RESTful API for task management with user authentication, real-time notifications, and team collaboration features. Built with modern Python frameworks and comprehensive testing.',
                'image_url': '/static/assets/images/portfolio/task-api.jpg',
                'github_url': 'https://github.com/lusansapkota/task-api',
                'live_url': 'https://api.taskmanager.com',
                'technologies': 'Python, FastAPI, PostgreSQL, Redis, JWT, WebSockets',
                'category_id': api_dev.id if api_dev else None,
                'is_featured': False,
                'is_opensource': True,
                'stars': 18,
                'status': 'completed'
            },
            {
                'title': 'E-commerce Mobile App',
                'description': 'Cross-platform mobile application for online shopping with features like product catalog, shopping cart, payment integration, and order tracking.',
                'image_url': '/static/assets/images/portfolio/ecommerce-app.jpg',
                'github_url': 'https://github.com/lusansapkota/ecommerce-mobile',
                'live_url': 'https://play.google.com/store/apps/details?id=com.lusan.ecommerce',
                'technologies': 'React Native, Node.js, MongoDB, Stripe API, Push Notifications',
                'category_id': mobile.id if mobile else None,
                'is_featured': True,
                'is_opensource': False,
                'stars': 42,
                'status': 'completed'
            },
            {
                'title': 'Data Analytics Dashboard',
                'description': 'Interactive dashboard for data visualization and analytics with real-time charts, filtering, and export capabilities. Processes large datasets efficiently.',
                'image_url': '/static/assets/images/portfolio/analytics-dashboard.jpg',
                'github_url': 'https://github.com/lusansapkota/analytics-dashboard',
                'live_url': 'https://analytics.example.com',
                'technologies': 'Python, Pandas, Plotly, Dash, NumPy, Scikit-learn',
                'category_id': data_science.id if data_science else None,
                'is_featured': False,
                'is_opensource': True,
                'stars': 31,
                'status': 'in-progress'
            },
            {
                'title': 'Docker Deployment Pipeline',
                'description': 'Automated CI/CD pipeline using Docker containers, with staging environments, automated testing, and deployment to cloud infrastructure.',
                'image_url': '/static/assets/images/portfolio/docker-pipeline.jpg',
                'github_url': 'https://github.com/lusansapkota/docker-pipeline',
                'live_url': None,
                'technologies': 'Docker, Jenkins, AWS, Kubernetes, Terraform, Ansible',
                'category_id': devops.id if devops else None,
                'is_featured': False,
                'is_opensource': True,
                'stars': 15,
                'status': 'completed'
            },
            {
                'title': 'Open Source Library',
                'description': 'A utility library for common web development tasks with comprehensive documentation, unit tests, and community contributions.',
                'image_url': '/static/assets/images/portfolio/open-source-lib.jpg',
                'github_url': 'https://github.com/lusansapkota/web-utils',
                'live_url': 'https://pypi.org/project/lusan-web-utils/',
                'technologies': 'Python, PyPI, Sphinx, pytest, GitHub Actions',
                'category_id': opensource.id if opensource else None,
                'is_featured': True,
                'is_opensource': True,
                'stars': 67,
                'status': 'maintenance'
            },
            {
                'title': 'Client CRM System',
                'description': 'Custom customer relationship management system built for a client with lead tracking, sales pipeline, and reporting features.',
                'image_url': '/static/assets/images/portfolio/crm-system.jpg',
                'github_url': None,  # Private repository
                'live_url': 'https://crm.clientsite.com',
                'technologies': 'Django, PostgreSQL, Redis, Celery, Chart.js, Bootstrap',
                'category_id': commercial.id if commercial else None,
                'is_featured': False,
                'is_opensource': False,
                'stars': 0,
                'status': 'completed'
            },
            {
                'title': 'Desktop PDF Manager',
                'description': 'Cross-platform desktop application for PDF management with features like merging, splitting, watermarking, and batch processing.',
                'image_url': '/static/assets/images/portfolio/pdf-manager.jpg',
                'github_url': 'https://github.com/lusansapkota/pdf-manager',
                'live_url': 'https://releases.github.com/lusansapkota/pdf-manager',
                'technologies': 'Python, Tkinter, PyPDF2, cx_Freeze, PIL, Threading',
                'category_id': desktop.id if desktop else None,
                'is_featured': False,
                'is_opensource': True,
                'stars': 23,
                'status': 'completed'
            }
        ]
        
        for project_data in sample_projects:
            project = Project(
                title=project_data['title'],
                description=project_data['description'],
                image_url=project_data['image_url'],
                github_url=project_data['github_url'],
                live_url=project_data['live_url'],
                technologies=project_data['technologies'],
                category_id=project_data['category_id'],
                is_featured=project_data['is_featured'],
                is_opensource=project_data['is_opensource'],
                stars=project_data['stars'],
                status=project_data['status']
            )
            db.session.add(project)
        
        db.session.commit()
        print("✅ Created sample projects")
    
    print("🎉 Git section sample data populated successfully!")

if __name__ == '__main__':
    from app import app
    
    with app.app_context():
        populate_git_sample_data()

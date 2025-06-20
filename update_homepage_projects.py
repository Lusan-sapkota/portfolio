#!/usr/bin/env python3
"""
Script to set some projects to show on homepage by default
"""

from app import app
from models import db, Project

def update_homepage_projects():
    """Set first 3 projects to show on homepage"""
    with app.app_context():
        # Get first 3 projects and set them to show on homepage
        projects = Project.query.limit(3).all()
        
        for project in projects:
            project.show_on_homepage = True
            print(f"Set '{project.title}' to show on homepage")
        
        db.session.commit()
        print(f"Updated {len(projects)} projects to show on homepage")

if __name__ == '__main__':
    update_homepage_projects()

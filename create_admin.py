#!/usr/bin/env python3
"""
Quick admin user creation
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
admin_user = os.environ.get('ADMIN_USER')
admin_password = os.environ.get('ADMIN_PASSWORD')
admin_email = os.environ.get('ADMIN_EMAIL')

def create_admin_user():
    try:
        from app import app
        from models import User
        from database import db
        
        with app.app_context():
            # Create tables if they don't exist
            db.create_all()
            
            # Check for existing admin
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("Admin user already exists!")
                print(f"   Username: admin")
                print(f"   Email: {admin.email}")
                print(f"   Admin: {admin.is_admin}")
                return
            
            # Create new admin
            admin = User(
                username=admin_user,
                email=admin_email,
                is_admin=True
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("Admin user created successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_admin_user()

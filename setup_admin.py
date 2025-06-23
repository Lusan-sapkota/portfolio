#!/usr/bin/env python3
"""
Setup admin user for the portfolio CMS
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db
from models import User

def setup_admin():
    """Create default admin user"""
    
    with app.app_context():
        try:
            # Check if any admin user exists
            existing_admin = User.query.filter_by(is_admin=True).first()
            
            if existing_admin:
                print("✅ Admin user already exists:")
                print(f"   Username: {existing_admin.username}")
                print(f"   Email: {existing_admin.email}")
                print()
                print("🔑 Use these credentials to login to /admin")
                return True
            
            # Create default admin user
            print("🚀 Creating default admin user...")
            
            username = 'admin'
            email = 'contact@lusansapkota.com.np'
            password = 'admin123'
            
            user = User(username=username, email=email, is_admin=True)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            print("✅ Admin user created successfully!")
            print()
            print("🔑 Admin Login Credentials:")
            print(f"   URL: http://localhost:5000/admin")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            print(f"   Email: {email}")
            print()
            print("⚠️  IMPORTANT: Change the default password after first login!")
            print("   You can create additional admin users using:")
            print("   python -m flask create-admin <username> <email> <password>")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            return False

if __name__ == '__main__':
    print("🎯 Setting up admin user for Portfolio CMS...")
    print()
    
    success = setup_admin()
    
    if success:
        print()
        print("🎉 Setup complete! You can now:")
        print("   1. Start the development server: python app.py")
        print("   2. Visit http://localhost:5000/admin")
        print("   3. Login with the credentials above")
        print("   4. Start managing your portfolio content!")
    else:
        print()
        print("❌ Setup failed. Please check the error messages above.")

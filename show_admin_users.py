#!/usr/bin/env python3
"""
Show all admin users in the database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def show_admin_users():
    try:
        from app import app
        from models import User
        from database import db
        
        with app.app_context():
            print("🔑 Available Admin Users:")
            print("=" * 50)
            
            admin_users = User.query.filter_by(is_admin=True).all()
            
            if admin_users:
                for i, user in enumerate(admin_users, 1):
                    print(f"{i}. Username: {user.username}")
                    print(f"   Email: {user.email}")
                    print(f"   Admin: {user.is_admin}")
                    print(f"   Created: {user.created_at if hasattr(user, 'created_at') else 'N/A'}")
                    print("-" * 30)
                
                print()
                print("🌐 Admin Panel Access:")
                print("   URL: http://localhost:5000/admin")
                print("   Use any of the usernames above with their respective passwords")
                print()
                print("⚠️  If you don't know the password for existing users,")
                print("   you can create a new admin user with:")
                print("   python -m flask create-admin <username> <email> <password>")
                
            else:
                print("❌ No admin users found in the database.")
                print()
                print("Creating default admin user...")
                
                # Create default admin user
                admin = User(
                    username='admin',
                    email='admin@lusansapkota.com.np',
                    is_admin=True
                )
                admin.set_password('admin123')
                
                db.session.add(admin)
                db.session.commit()
                
                print("✅ Default admin user created!")
                print()
                print("🔑 Login Credentials:")
                print("   Username: admin")
                print("   Password: admin123")
                print("   Email: admin@lusansapkota.com.np")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    show_admin_users()

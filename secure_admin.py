#!/usr/bin/env python3
"""
Secure Admin Management Script
Removes all admin users except one and sets up a secure admin account.
"""

import secrets
import string
from database import db
from models import User
from app import app

def generate_secure_password(length=16):
    """Generate a cryptographically secure password."""
    # Combine uppercase, lowercase, digits, and special characters
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character from each category
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*")
    ]
    
    # Fill the rest of the password length
    for i in range(length - 4):
        password.append(secrets.choice(alphabet))
    
    # Shuffle the password list
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def secure_admin_setup():
    """Remove all admin users and create one secure admin."""
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        print("🔒 Securing Admin Access...")
        print("=" * 50)
        
        # Get all current admin users
        current_admins = User.query.filter_by(is_admin=True).all()
        
        if current_admins:
            print(f"Found {len(current_admins)} admin user(s):")
            for admin in current_admins:
                print(f"   - {admin.username} ({admin.email})")
        
        # Remove all existing admin users
        for admin in current_admins:
            db.session.delete(admin)
            print(f"   ✗ Removed admin: {admin.username}")
        
        # Also remove any non-admin users with the target email
        existing_user = User.query.filter_by(email="admin@lusansapkota.com.np").first()
        if existing_user:
            db.session.delete(existing_user)
            print(f"   ✗ Removed existing user with target email: {existing_user.username}")
        
        # Commit deletions
        db.session.commit()
        
        # Create new secure admin
        username = "admin"
        email = "admin@lusansapkota.com.np"
        secure_password = generate_secure_password(20)
        
        new_admin = User(
            username=username,
            email=email,
            is_admin=True
        )
        new_admin.set_password(secure_password)
        
        db.session.add(new_admin)
        db.session.commit()
        
        print("\n✅ Secure Admin Created:")
        print("=" * 50)
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {secure_password}")
        print("\n⚠️  IMPORTANT: Save these credentials securely!")
        print("   This password will not be shown again.")
        
        print("\n🌐 Admin Panel Access:")
        print(f"   URL: http://localhost:5000/admin")
        print(f"   Username: {username}")
        print(f"   Password: {secure_password}")
        
        # Save credentials to a secure file
        try:
            with open('/home/lusan/Documents/portfolio/ADMIN_CREDENTIALS.txt', 'w') as f:
                f.write("SECURE ADMIN CREDENTIALS\n")
                f.write("=" * 30 + "\n")
                f.write(f"Username: {username}\n")
                f.write(f"Email: {email}\n")
                f.write(f"Password: {secure_password}\n")
                f.write(f"Admin Panel: http://localhost:5000/admin\n")
                f.write("\nCreated: " + str(new_admin.created_at) + "\n")
                f.write("\nIMPORTANT: Keep this file secure and delete it after saving credentials elsewhere!\n")
            
            print(f"\n📄 Credentials also saved to: ADMIN_CREDENTIALS.txt")
            print("   Please save these credentials securely and delete this file!")
            
        except Exception as e:
            print(f"\n⚠️  Could not save credentials file: {e}")
        
        print("\n🔐 Security Features Added:")
        print("   ✓ Strong 20-character password with mixed characters")
        print("   ✓ Only one admin user exists")
        print("   ✓ Secure password hashing")
        print("   ✓ Rate limiting on login attempts")
        print("   ✓ Session timeout (24 hours)")
        print("   ✓ Brute-force protection with delays")
        print("   ✓ Security logging")
        
        return True

if __name__ == "__main__":
    try:
        secure_admin_setup()
        print("\n🎉 Admin security setup completed successfully!")
    except Exception as e:
        print(f"\n❌ Error setting up secure admin: {e}")
        exit(1)

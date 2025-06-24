#!/usr/bin/env python3
"""
Secure Admin Setup Script - Production Environment
No default passwords, no environment variable dependencies
Interactive setup with strong validation
"""
import sys
import os
import getpass
import re
import secrets
import string
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class AdminSetup:
    def __init__(self):
        self.min_password_length = 16
        self.admin_user = None
        self.admin_email = None
        self.admin_password = None

    def generate_secure_password(self, length=20):
        """Generate a cryptographically secure password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

    def validate_username(self, username):
        """Validate username for production use"""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        if username.lower() in ['admin', 'administrator', 'root', 'test']:
            return False, "Username cannot be a common default name"
        
        return True, "Username is valid"

    def validate_email(self, email):
        """Validate email address"""
        if not email:
            return False, "Email cannot be empty"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        return True, "Email is valid"

    def validate_password(self, password):
        """Validate password strength for production"""
        if len(password) < self.min_password_length:
            return False, f"Password must be at least {self.min_password_length} characters long"
        
        checks = [
            (r'[A-Z]', "uppercase letter"),
            (r'[a-z]', "lowercase letter"),
            (r'\d', "number"),
            (r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', "special character")
        ]
        
        for pattern, description in checks:
            if not re.search(pattern, password):
                return False, f"Password must contain at least one {description}"
        
        # Check for common weak patterns
        weak_patterns = [
            'password', '123456', 'qwerty', 'admin', 'letmein',
            'welcome', 'monkey', 'dragon', 'master', 'hello'
        ]
        
        password_lower = password.lower()
        for pattern in weak_patterns:
            if pattern in password_lower:
                return False, f"Password cannot contain common weak pattern: {pattern}"
        
        # Check for keyboard patterns
        keyboard_patterns = ['qwerty', 'asdf', '1234', 'abcd']
        for pattern in keyboard_patterns:
            if pattern in password_lower:
                return False, "Password cannot contain keyboard patterns"
        
        return True, "Password meets security requirements"

    def get_credentials(self):
        """Interactive credential collection with validation"""
        print("🔐 SECURE ADMIN SETUP")
        print("=" * 50)
        print("This will create a production-ready admin user.")
        print("All credentials will be validated for security.\n")

        # Username
        while True:
            username = input("Admin Username (no common names): ").strip()
            is_valid, message = self.validate_username(username)
            if is_valid:
                self.admin_user = username
                break
            print(f"❌ {message}")

        # Email
        while True:
            email = input("Admin Email: ").strip()
            is_valid, message = self.validate_email(email)
            if is_valid:
                self.admin_email = email
                break
            print(f"❌ {message}")

        # Password options
        print(f"\nPassword Options:")
        print(f"1. Enter your own password (min {self.min_password_length} chars)")
        print(f"2. Generate secure password automatically")
        
        choice = input("\nChoose option (1 or 2): ").strip()
        
        if choice == "2":
            # Generate secure password
            self.admin_password = self.generate_secure_password()
            print(f"\n🔑 Generated secure password: {self.admin_password}")
            print("⚠️  IMPORTANT: Save this password securely! You won't see it again.")
            input("Press Enter when you have saved the password...")
        else:
            # Manual password entry
            print(f"\nPassword Requirements:")
            print(f"• At least {self.min_password_length} characters")
            print(f"• Must contain: uppercase, lowercase, numbers, special chars")
            print(f"• No common weak patterns or keyboard sequences")
            
            while True:
                password = getpass.getpass("\nEnter secure password: ")
                is_valid, message = self.validate_password(password)
                if is_valid:
                    confirm = getpass.getpass("Confirm password: ")
                    if password == confirm:
                        self.admin_password = password
                        break
                    else:
                        print("❌ Passwords do not match")
                else:
                    print(f"❌ {message}")

    def create_admin(self):
        """Create the admin user in database"""
        try:
            from app import app
            from models import User
            from database import db
            
            with app.app_context():
                # Check database connection
                db.create_all()
                
                # Check for existing users
                existing_user = User.query.filter_by(username=self.admin_user).first()
                if existing_user:
                    print(f"❌ User '{self.admin_user}' already exists!")
                    return False
                
                existing_email = User.query.filter_by(email=self.admin_email).first()
                if existing_email:
                    print(f"❌ Email '{self.admin_email}' already in use!")
                    return False
                
                # Create admin user
                admin = User(
                    username=self.admin_user,
                    email=self.admin_email,
                    is_admin=True
                )
                admin.set_password(self.admin_password)
                
                db.session.add(admin)
                db.session.commit()
                
                print(f"\n✅ SUCCESS!")
                print(f"🎉 Admin user '{self.admin_user}' created successfully")
                print(f"📧 Email: {self.admin_email}")
                print(f"🔐 Admin privileges: Enabled")
                print(f"🚀 You can now access /admin with these credentials")
                
                return True
                
        except Exception as e:
            print(f"❌ Database error: {str(e)}")
            return False

    def run_setup(self):
        """Run the complete setup process"""
        try:
            self.get_credentials()
            
            print(f"\n📋 SETUP SUMMARY")
            print(f"Username: {self.admin_user}")
            print(f"Email: {self.admin_email}")
            print(f"Password: [SECURED]")
            
            confirm = input("\nProceed with admin creation? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                return self.create_admin()
            else:
                print("Setup cancelled.")
                return False
                
        except KeyboardInterrupt:
            print("\n\nSetup cancelled by user.")
            return False
        except Exception as e:
            print(f"\n❌ Setup failed: {str(e)}")
            return False

if __name__ == '__main__':
    print(f"🔒 Portfolio Secure Admin Setup")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    setup = AdminSetup()
    
    if setup.run_setup():
        print(f"\n🎊 PRODUCTION SETUP COMPLETE!")
        print(f"Your portfolio is ready for production use.")
    else:
        print(f"\n💥 Setup failed or cancelled.")
        sys.exit(1)

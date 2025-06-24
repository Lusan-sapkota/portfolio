#!/usr/bin/env python3
"""
Production-level admin user creation script
Security Requirements:
- No default passwords
- Strong password validation
- Environment variable validation
- Proper error handling
"""
import sys
import os
import getpass
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def validate_strong_password(password: str) -> tuple[bool, str]:
    """Validate password meets production security standards"""
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        return False, "Password must contain at least one special character"
    
    # Check for common weak patterns
    weak_patterns = ['123456', 'password', 'admin', 'qwerty', 'abc123']
    for pattern in weak_patterns:
        if pattern.lower() in password.lower():
            return False, f"Password cannot contain common pattern: {pattern}"
    
    return True, "Password is strong"

def get_admin_credentials():
    """Get admin credentials with proper validation"""
    print("=== Production Admin User Creation ===")
    print("This script will create an admin user for production use.")
    print("All fields are required and will be validated.\n")
    
    # Get credentials from environment first
    admin_user = os.environ.get('ADMIN_USER')
    admin_email = os.environ.get('ADMIN_EMAIL') 
    admin_password = os.environ.get('ADMIN_PASSWORD')
    
    # Validate and prompt if missing
    if not admin_user:
        print("ERROR: ADMIN_USER environment variable not set!")
        admin_user = input("Enter admin username (no defaults): ").strip()
        if not admin_user:
            print("Username cannot be empty!")
            sys.exit(1)
    
    if not admin_email:
        print("ERROR: ADMIN_EMAIL environment variable not set!")
        admin_email = input("Enter admin email (no defaults): ").strip()
        if not admin_email or '@' not in admin_email:
            print("Valid email address required!")
            sys.exit(1)
    
    if not admin_password:
        print("ERROR: ADMIN_PASSWORD environment variable not set!")
        print("Password requirements:")
        print("- At least 12 characters")
        print("- Must contain uppercase, lowercase, numbers, and special characters")
        print("- No common weak patterns\n")
        
        while True:
            admin_password = getpass.getpass("Enter secure admin password: ")
            if not admin_password:
                print("Password cannot be empty!")
                continue
                
            is_valid, message = validate_strong_password(admin_password)
            if is_valid:
                confirm_password = getpass.getpass("Confirm password: ")
                if admin_password == confirm_password:
                    break
                else:
                    print("Passwords do not match!")
            else:
                print(f"Password validation failed: {message}")
    
    return admin_user, admin_email, admin_password

def create_admin_user():
    """Create admin user with production-level security"""
    try:
        # Get validated credentials
        admin_user, admin_email, admin_password = get_admin_credentials()
        
        print(f"\nCreating admin user:")
        print(f"Username: {admin_user}")
        print(f"Email: {admin_email}")
        print("Password: [SECURED]")
        
        from app import app
        from models import User
        from database import db
        
        with app.app_context():
            # Create tables if they don't exist
            db.create_all()
            
            # Check for existing admin with same username
            existing_user = User.query.filter_by(username=admin_user).first()
            if existing_user:
                print(f"\nERROR: User with username '{admin_user}' already exists!")
                print(f"   Email: {existing_user.email}")
                print(f"   Admin: {existing_user.is_admin}")
                print("\nChoose a different username or delete the existing user first.")
                return False
            
            # Check for existing admin with same email
            existing_email = User.query.filter_by(email=admin_email).first()
            if existing_email:
                print(f"\nERROR: User with email '{admin_email}' already exists!")
                print(f"   Username: {existing_email.username}")
                print(f"   Admin: {existing_email.is_admin}")
                print("\nChoose a different email or delete the existing user first.")
                return False
            
            # Create new admin user
            admin = User(
                username=admin_user,
                email=admin_email,
                is_admin=True
            )
            admin.set_password(admin_password)
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"\n✅ SUCCESS: Admin user '{admin_user}' created successfully!")
            print("🔐 User has admin privileges and can access /admin")
            print("🚀 Production environment is ready!")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: Failed to create admin user: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_environment():
    """Check if environment is properly configured"""
    required_vars = ['SECRET_KEY', 'DATABASE_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        return False
    
    print("✅ Environment configuration validated")
    return True

if __name__ == '__main__':
    print("🔧 Portfolio Production Admin Setup")
    print("=" * 40)
    
    # Check environment first
    if not check_environment():
        sys.exit(1)
    
    # Create admin user
    if create_admin_user():
        print("\n🎉 Setup completed successfully!")
        print("You can now start your application and access the admin panel.")
    else:
        print("\n💥 Setup failed! Please fix the errors above and try again.")
        sys.exit(1)

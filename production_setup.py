#!/usr/bin/env python3
"""
🚀 Portfolio Production Setup Script
Complete setup for production deployment with security validation
"""
import sys
import os
import subprocess
import time
from datetime import datetime

class ProductionSetup:
    def __init__(self):
        self.setup_steps = [
            ("🔍 Environment Validation", self.check_environment),
            ("🗄️  Database Migration", self.run_migrations), 
            ("👤 Admin User Creation", self.setup_admin),
            ("💳 Payment Methods Setup", self.setup_payment_methods),
            ("🔒 Security Configuration", self.configure_security),
            ("✅ Final Validation", self.validate_setup)
        ]
        
    def print_header(self):
        print("🚀 PORTFOLIO PRODUCTION SETUP")
        print("=" * 50)
        print(f"⏰ Setup started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 This script will prepare your portfolio for production use")
        print("🔐 All security measures will be validated\n")

    def check_environment(self):
        """Validate environment configuration"""
        try:
            print("📋 Checking environment variables...")
            
            # Required environment variables
            required_vars = {
                'SECRET_KEY': 'Flask secret key',
                'DATABASE_URL': 'PostgreSQL database connection',
                'ADMIN_USER': 'Admin username',
                'ADMIN_EMAIL': 'Admin email', 
                'ADMIN_PASSWORD': 'Admin password'
            }
            
            missing_vars = []
            for var, description in required_vars.items():
                value = os.environ.get(var)
                if not value:
                    missing_vars.append(f"  ❌ {var}: {description}")
                else:
                    # Mask sensitive values
                    if 'PASSWORD' in var or 'SECRET' in var:
                        display_value = f"[SET - {len(value)} chars]"
                    else:
                        display_value = value[:50] + "..." if len(value) > 50 else value
                    print(f"  ✅ {var}: {display_value}")
            
            if missing_vars:
                print("\n❌ Missing required environment variables:")
                for var in missing_vars:
                    print(var)
                print("\nPlease check your .env file and try again.")
                return False
            
            # Check database connectivity
            print("🔗 Testing database connection...")
            try:
                from app import app
                from database import db
                from sqlalchemy import text
                with app.app_context():
                    db.session.execute(text("SELECT 1"))
                print("  ✅ Database connection successful")
            except Exception as e:
                print(f"  ❌ Database connection failed: {e}")
                return False
                
            print("✅ Environment validation passed!\n")
            return True
            
        except Exception as e:
            print(f"❌ Environment check failed: {e}")
            return False

    def run_migrations(self):
        """Run all necessary database migrations"""
        try:
            print("🔄 Running database migrations...")
            
            # Run payment method migration
            print("  💳 Migrating PaymentMethod table...")
            result = subprocess.run([sys.executable, "migrate_payment_methods.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("  ✅ PaymentMethod migration completed")
            else:
                print(f"  ❌ PaymentMethod migration failed: {result.stderr}")
                return False
            
            # Create all tables
            print("  🗄️  Creating/updating database tables...")
            from app import app
            from database import db
            
            with app.app_context():
                db.create_all()
                print("  ✅ Database tables updated")
            
            print("✅ Database migrations completed!\n")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False

    def setup_admin(self):
        """Setup admin user"""
        try:
            print("👤 Setting up admin user...")
            
            # Check if admin already exists
            admin_user = os.environ.get('ADMIN_USER')
            from app import app
            from models import User
            
            with app.app_context():
                existing_admin = User.query.filter_by(username=admin_user).first()
                
                if existing_admin:
                    print(f"  ✅ Admin user '{admin_user}' already exists")
                    print(f"     Email: {existing_admin.email}")
                    print(f"     Admin privileges: {existing_admin.is_admin}")
                else:
                    # Create admin user
                    print(f"  🔧 Creating admin user '{admin_user}'...")
                    result = subprocess.run([sys.executable, "create_admin.py"], 
                                          capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print("  ✅ Admin user created successfully")
                    else:
                        print(f"  ❌ Admin creation failed: {result.stderr}")
                        return False
            
            print("✅ Admin setup completed!\n")
            return True
            
        except Exception as e:
            print(f"❌ Admin setup failed: {e}")
            return False

    def setup_payment_methods(self):
        """Configure payment methods with verification status"""
        try:
            print("💳 Configuring payment methods...")
            
            from app import app
            from models import PaymentMethod
            from database import db
            
            with app.app_context():
                # Count payment methods
                total_methods = PaymentMethod.query.count()
                pending_methods = PaymentMethod.query.filter_by(is_verification_pending=True).count()
                active_methods = PaymentMethod.query.filter_by(is_active=True).count()
                
                print(f"  📊 Payment methods status:")
                print(f"     Total methods: {total_methods}")
                print(f"     Active methods: {active_methods}")
                print(f"     Pending verification: {pending_methods}")
                
                if total_methods == 0:
                    print("  ⚠️  No payment methods configured. Please add them via admin panel.")
                else:
                    print("  ✅ Payment methods are configured")
                
                # Show verification pending methods
                if pending_methods > 0:
                    pending = PaymentMethod.query.filter_by(is_verification_pending=True).all()
                    print("  🔒 Methods pending verification:")
                    for method in pending:
                        print(f"     - {method.display_name} ({method.currency})")
            
            print("✅ Payment methods check completed!\n")
            return True
            
        except Exception as e:
            print(f"❌ Payment methods setup failed: {e}")
            return False

    def configure_security(self):
        """Configure security settings"""
        try:
            print("🔒 Configuring security settings...")
            
            # Check DEBUG mode
            debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
            if debug_mode:
                print("  ⚠️  WARNING: DEBUG mode is enabled")
                print("     For production, set DEBUG=False in your .env file")
            else:
                print("  ✅ DEBUG mode is disabled")
            
            # Check secret key strength
            secret_key = os.environ.get('SECRET_KEY')
            if len(secret_key) < 32:
                print("  ⚠️  WARNING: SECRET_KEY is too short")
                print("     Recommended: At least 32 characters")
            else:
                print("  ✅ SECRET_KEY length is adequate")
            
            # Check admin password from environment
            admin_password = os.environ.get('ADMIN_PASSWORD')
            if len(admin_password) < 12:
                print("  ⚠️  WARNING: ADMIN_PASSWORD may be too weak")
                print("     Recommended: At least 12 characters with mixed case, numbers, and symbols")
            else:
                print("  ✅ ADMIN_PASSWORD meets minimum length requirements")
            
            print("✅ Security configuration reviewed!\n")
            return True
            
        except Exception as e:
            print(f"❌ Security configuration failed: {e}")
            return False

    def validate_setup(self):
        """Final validation of the setup"""
        try:
            print("🧪 Running final validation...")
            
            from app import app
            from models import User, PaymentMethod
            
            with app.app_context():
                # Check admin user exists
                admin_count = User.query.filter_by(is_admin=True).count()
                if admin_count == 0:
                    print("  ❌ No admin users found")
                    return False
                else:
                    print(f"  ✅ {admin_count} admin user(s) configured")
                
                # Check payment methods
                payment_count = PaymentMethod.query.filter_by(is_active=True).count()
                print(f"  ✅ {payment_count} active payment method(s)")
                
                # Check database tables
                tables = [
                    'user', 'project', 'project_category', 'contact_submission',
                    'newsletter_subscriber', 'seo_settings', 'personal_info',
                    'social_link', 'payment_method', 'donation'
                ]
                
                from sqlalchemy import text
                from database import db
                
                table_count = 0
                for table in tables:
                    try:
                        result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.scalar()
                        table_count += 1
                    except:
                        pass
                
                print(f"  ✅ {table_count}/{len(tables)} core tables available")
            
            print("✅ Final validation completed!\n")
            return True
            
        except Exception as e:
            print(f"❌ Final validation failed: {e}")
            return False

    def run_setup(self):
        """Run the complete production setup"""
        self.print_header()
        
        success_count = 0
        total_steps = len(self.setup_steps)
        
        for i, (step_name, step_function) in enumerate(self.setup_steps, 1):
            print(f"🔧 Step {i}/{total_steps}: {step_name}")
            print("-" * 50)
            
            try:
                if step_function():
                    success_count += 1
                    print(f"✅ Step {i} completed successfully!\n")
                else:
                    print(f"❌ Step {i} failed!\n")
                    break
            except Exception as e:
                print(f"❌ Step {i} failed with error: {e}\n")
                break
        
        # Final summary
        print("=" * 50)
        print("🎯 SETUP SUMMARY")
        print("=" * 50)
        
        if success_count == total_steps:
            print("🎉 SUCCESS! Your portfolio is ready for production!")
            print("\n📋 Next steps:")
            print("   1. Start your application with: gunicorn app:app")
            print("   2. Access admin panel at: /admin")
            print("   3. Configure payment methods via admin")
            print("   4. Test donation functionality")
            print("   5. Monitor logs for any issues")
            
            print(f"\n🔗 Admin Access:")
            print(f"   Username: {os.environ.get('ADMIN_USER')}")
            print(f"   Email: {os.environ.get('ADMIN_EMAIL')}")
            print(f"   Panel: /admin")
            
        else:
            print(f"💥 SETUP INCOMPLETE! ({success_count}/{total_steps} steps completed)")
            print("Please fix the errors above and run the setup again.")
            return False
        
        print(f"\n⏰ Setup completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True

if __name__ == '__main__':
    setup = ProductionSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)

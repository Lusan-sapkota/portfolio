#!/usr/bin/env python3
"""
Migration script to add SWIFT code and verification pending fields to PaymentMethod table
Enhanced with better error handling and verification status updates
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def migrate_payment_methods():
    """Add new fields to PaymentMethod table and update verification status"""
    try:
        from app import app
        from database import db
        from sqlalchemy import text
        
        with app.app_context():
            print("🔍 Checking existing PaymentMethod table structure...")
            
            # Check if columns already exist
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'payment_method' 
                AND column_name IN ('swift_code', 'is_verification_pending')
            """))
            
            existing_columns = [row[0] for row in result.fetchall()]
            print(f"Existing columns: {existing_columns}")
            
            migrations_needed = []
            
            # Add swift_code column if missing
            if 'swift_code' not in existing_columns:
                migrations_needed.append({
                    'sql': "ALTER TABLE payment_method ADD COLUMN swift_code VARCHAR(15)",
                    'description': 'swift_code column'
                })
            else:
                print("✓ swift_code column already exists")
            
            # Add is_verification_pending column if missing  
            if 'is_verification_pending' not in existing_columns:
                migrations_needed.append({
                    'sql': "ALTER TABLE payment_method ADD COLUMN is_verification_pending BOOLEAN DEFAULT FALSE",
                    'description': 'is_verification_pending column'
                })
            else:
                print("✓ is_verification_pending column already exists")
            
            if not migrations_needed:
                print("✅ All required columns exist. Checking verification status...")
            else:
                print(f"📝 Running {len(migrations_needed)} migration(s)...")
                
                # Run migrations
                for migration in migrations_needed:
                    try:
                        print(f"Adding {migration['description']}...")
                        db.session.execute(text(migration['sql']))
                        print(f"✓ Successfully added {migration['description']}")
                    except Exception as e:
                        print(f"❌ Error adding {migration['description']}: {e}")
                        return False
                
                db.session.commit()
                print("✅ Schema migration completed!")
            
            # Update existing PayPal and Payoneer methods to verification pending
            print("🔄 Updating verification status for PayPal/Payoneer methods...")
            
            update_result = db.session.execute(text("""
                UPDATE payment_method 
                SET is_verification_pending = TRUE 
                WHERE (method_name IN ('paypal', 'payoneer') 
                OR display_name ILIKE '%paypal%' 
                OR display_name ILIKE '%payoneer%')
                AND is_verification_pending = FALSE
            """))
            
            updated_count = update_result.rowcount
            db.session.commit()
            
            if updated_count > 0:
                print(f"✓ Updated {updated_count} payment method(s) to verification pending")
            else:
                print("✓ No payment methods needed verification status update")
            
            # Show current payment methods status
            print("\n📋 Current PaymentMethod status:")
            methods = db.session.execute(text("""
                SELECT display_name, currency, method_name, 
                       COALESCE(is_verification_pending, FALSE) as verification_pending,
                       is_active
                FROM payment_method 
                ORDER BY currency, sort_order
            """)).fetchall()
            
            for method in methods:
                status = "🔒 Verification Pending" if method[3] else "✅ Active"
                active = "🟢" if method[4] else "🔴"
                print(f"  {active} {method[0]} ({method[1]}) - {status}")
            
            print(f"\n✅ PaymentMethod migration completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🔧 PaymentMethod Table Migration")
    print("=" * 40)
    
    if migrate_payment_methods():
        print("\n🎉 Migration completed successfully!")
    else:
        print("\n💥 Migration failed!")
        sys.exit(1)

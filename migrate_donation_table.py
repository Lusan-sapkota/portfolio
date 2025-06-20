#!/usr/bin/env python3
"""
Database migration script to add new columns to existing donation table.
This adds the new fields we defined in the enhanced Donation model.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import db
from sqlalchemy import text

def migrate_donation_table():
    """Add new columns to the existing donation table"""
    # Import app after setting up the path
    import app
    
    with app.app.app_context():
        try:
            # Get current table structure
            result = db.session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'donation';"))
            existing_columns = [row[0] for row in result.fetchall()]
            print(f"Existing columns in donation table: {existing_columns}")
            
            # Define new columns to add
            new_columns = [
                ("donor_phone", "VARCHAR(20)"),
                ("currency", "VARCHAR(3) DEFAULT 'NPR'"),
                ("verified_amount", "FLOAT"),
                ("admin_notes", "TEXT"),
                ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            ]
            
            # Add missing columns
            for column_name, column_type in new_columns:
                if column_name not in existing_columns:
                    try:
                        sql = f"ALTER TABLE donation ADD COLUMN {column_name} {column_type};"
                        print(f"Adding column: {column_name}")
                        db.session.execute(text(sql))
                        db.session.commit()
                        print(f"✅ Added column: {column_name}")
                    except Exception as e:
                        print(f"❌ Failed to add column {column_name}: {e}")
                        db.session.rollback()
                else:
                    print(f"⏭️ Column {column_name} already exists")
            
            # Now create the new tables for PaymentMethod, ThanksgivingSettings, and DonationSettings
            print("\nCreating new tables...")
            db.create_all()
            
            print("\n✅ Migration completed successfully!")
            print("🎉 Enhanced donation system is ready!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Migration failed: {e}")
            return False
            
    return True

if __name__ == '__main__':
    migrate_donation_table()

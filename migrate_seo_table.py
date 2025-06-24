#!/usr/bin/env python3
"""
Manual database migration to add SEO fields
"""
import sys
import os
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from app import app
from database import db

def migrate_seo_table():
    """Add new SEO fields to existing table"""
    
    with app.app_context():
        try:
            # Get database connection
            connection = db.engine.connect()
            
            # List of new columns to add
            new_columns = [
                ("og_url", "VARCHAR(255)"),
                ("og_type", "VARCHAR(50) DEFAULT 'website'"),
                ("twitter_title", "VARCHAR(200)"),
                ("twitter_description", "TEXT"),
                ("twitter_image", "VARCHAR(255)"),
                ("twitter_url", "VARCHAR(255)"),
                ("twitter_card", "VARCHAR(50) DEFAULT 'summary_large_image'"),
                ("hreflang", "VARCHAR(10) DEFAULT 'en'"),
                ("focus_keywords", "TEXT"),
                ("meta_author", "VARCHAR(100)"),
                ("meta_publisher", "VARCHAR(100)"),
                ("article_section", "VARCHAR(100)"),
                ("article_tags", "TEXT"),
                ("page_priority", "FLOAT DEFAULT 0.5"),
                ("update_frequency", "VARCHAR(20) DEFAULT 'weekly'"),
                ("noindex", "BOOLEAN DEFAULT FALSE"),
                ("nofollow", "BOOLEAN DEFAULT FALSE"),
                ("noarchive", "BOOLEAN DEFAULT FALSE"),
                ("nosnippet", "BOOLEAN DEFAULT FALSE"),
                ("google_analytics_id", "VARCHAR(50)"),
                ("google_tag_manager_id", "VARCHAR(50)"),
                ("facebook_pixel_id", "VARCHAR(50)")
            ]
            
            # Check if table exists
            result = connection.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'seo_settings'
                );
            """)
            
            table_exists = result.fetchone()[0]
            
            if not table_exists:
                print("Creating seo_settings table...")
                db.create_all()
                print("✅ Tables created successfully!")
                return
            
            # Add new columns one by one
            for column_name, column_type in new_columns:
                try:
                    # Check if column exists
                    result = connection.execute(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name='seo_settings' AND column_name='{column_name}';
                    """)
                    
                    if not result.fetchone():
                        # Add the column
                        connection.execute(f"""
                            ALTER TABLE seo_settings 
                            ADD COLUMN {column_name} {column_type};
                        """)
                        print(f"✅ Added column: {column_name}")
                    else:
                        print(f"⚠️  Column already exists: {column_name}")
                        
                except Exception as e:
                    print(f"❌ Error adding column {column_name}: {e}")
                    continue
            
            # Commit changes
            connection.commit()
            connection.close()
            
            print("\n🎉 Database migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    migrate_seo_table()

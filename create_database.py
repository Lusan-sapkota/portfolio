#!/usr/bin/env python3
"""
Create all database tables
"""
import sys
import os
from app import app
from database import db
from models import *
        
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_database_tables():
    try:

        with app.app_context():
            print("🗄️  Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Show what tables were created
            tables = db.engine.table_names()
            print(f"📊 Created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"   - {table}")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_database_tables()

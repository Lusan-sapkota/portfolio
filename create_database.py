#!/usr/bin/env python3
"""
Create all database tables
"""
import os
import sys
from sqlalchemy import inspect, text

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def create_database_tables():
    """Create all database tables"""
    try:
        with app.app_context():
            print("🗄️  Creating database tables...")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check what tables were created using inspector (fixed method)
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"📋 Created tables: {', '.join(tables)}")
            else:
                print("⚠️  No tables found after creation")
                
            # Test database connection
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print("✅ Database connection test successful!")
                
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

def check_database_connection():
    """Check if database connection is working"""
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                print(f"✅ PostgreSQL version: {version}")
                return True
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting database setup...")
    
    # Check database connection first
    if not check_database_connection():
        print("❌ Please check your database configuration in .env file")
        sys.exit(1)
    
    # Create tables
    if create_database_tables():
        print("🎉 Database setup completed successfully!")
    else:
        print("❌ Database setup failed!")
        sys.exit(1)

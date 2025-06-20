#!/usr/bin/env python3

import os
import sys
from app import app
from database import db
from sqlalchemy import text

def add_project_columns():
    with app.app_context():
        try:
            # Add commercial_url column
            db.session.execute(text('ALTER TABLE project ADD COLUMN commercial_url VARCHAR(500);'))
            print('✓ Added commercial_url column')
        except Exception as e:
            if 'already exists' in str(e) or 'duplicate column' in str(e).lower():
                print('✓ commercial_url column already exists')
            else:
                print(f'Error adding commercial_url: {e}')
                return False
        
        try:
            # Add show_on_homepage column
            db.session.execute(text('ALTER TABLE project ADD COLUMN show_on_homepage BOOLEAN DEFAULT FALSE;'))
            print('✓ Added show_on_homepage column')
        except Exception as e:
            if 'already exists' in str(e) or 'duplicate column' in str(e).lower():
                print('✓ show_on_homepage column already exists')
            else:
                print(f'Error adding show_on_homepage: {e}')
                return False
        
        try:
            db.session.commit()
            print('✓ Database changes committed successfully!')
            return True
        except Exception as e:
            print(f'Error committing changes: {e}')
            db.session.rollback()
            return False

if __name__ == "__main__":
    if add_project_columns():
        print("\n🎉 Project table updated successfully!")
        sys.exit(0)
    else:
        print("\n❌ Failed to update project table")
        sys.exit(1)

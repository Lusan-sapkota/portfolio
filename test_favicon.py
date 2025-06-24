#!/usr/bin/env python3

from app import app
import tempfile
import os

def test_favicon_urls():
    """Test favicon URL generation in different contexts"""
    
    with app.app_context():
        # Test in main app context
        with app.test_request_context('/'):
            from flask import url_for
            main_favicon = url_for('static', filename='assets/logo/favicon.ico')
            main_logo = url_for('static', filename='assets/logo/logo.png')
            print(f"Main app context:")
            print(f"  Favicon: {main_favicon}")
            print(f"  Logo: {main_logo}")
        
        # Test in donation context
        with app.test_request_context('/donation/'):
            from flask import url_for
            donation_favicon = url_for('static', filename='assets/logo/favicon.ico')
            donation_logo = url_for('static', filename='assets/logo/logo.png')
            print(f"Donation context:")
            print(f"  Favicon: {donation_favicon}")
            print(f"  Logo: {donation_logo}")
        
        # Test donation static
        with app.test_request_context('/donation/'):
            from flask import url_for
            try:
                donation_static_css = url_for('donation.static', filename='css/donation-style.css')
                print(f"  Donation CSS: {donation_static_css}")
            except Exception as e:
                print(f"  Donation CSS error: {e}")

def test_file_existence():
    """Test if favicon files actually exist"""
    main_favicon = '/home/lusan/Desktop/portfolio_prod/portfolio/static/assets/logo/favicon.ico'
    main_logo = '/home/lusan/Desktop/portfolio_prod/portfolio/static/assets/logo/logo.png'
    
    print(f"File existence:")
    print(f"  Main favicon exists: {os.path.exists(main_favicon)}")
    print(f"  Main logo exists: {os.path.exists(main_logo)}")

if __name__ == "__main__":
    print("Testing favicon URL generation...")
    test_favicon_urls()
    print()
    test_file_existence()

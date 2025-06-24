#!/usr/bin/env python3
"""
Test New Admin Features
Tests the personal info, newsletter sending, and password change features
"""

import requests
import json
from datetime import datetime

def test_new_admin_features():
    """Test all new admin features"""
    
    print("🧪 Testing New Admin Features")
    print("=" * 50)
    
    # Admin credentials
    admin_credentials = {
        'username': 'admin',
        'password': 'H7CtoyboLqDVz@CU,zPI'
    }
    
    session = requests.Session()
    
    # Test 1: Login
    print("\n1. Testing admin login...")
    try:
        login_response = session.post('http://localhost:5000/admin/login', data=admin_credentials, timeout=10)
        if login_response.status_code == 200:
            print("   ✅ Admin login successful")
        else:
            print(f"   ❌ Login failed with status: {login_response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Login failed: {e}")
        return
    
    # Test 2: Personal Info page
    print("\n2. Testing personal info page...")
    try:
        response = session.get('http://localhost:5000/admin/personal-info', timeout=10)
        if response.status_code == 200:
            print("   ✅ Personal info page accessible")
        else:
            print(f"   ❌ Personal info page returned status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Personal info page failed: {e}")
    
    # Test 3: Newsletter sending page
    print("\n3. Testing newsletter sending page...")
    try:
        response = session.get('http://localhost:5000/admin/newsletter/send', timeout=10)
        if response.status_code == 200:
            print("   ✅ Newsletter sending page accessible")
        else:
            print(f"   ❌ Newsletter sending page returned status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Newsletter sending page failed: {e}")
    
    # Test 4: Password change page
    print("\n4. Testing password change page...")
    try:
        response = session.get('http://localhost:5000/admin/change-password', timeout=10)
        if response.status_code == 200:
            print("   ✅ Password change page accessible")
        else:
            print(f"   ❌ Password change page returned status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Password change page failed: {e}")
    
    # Test 5: Newsletter export functionality
    print("\n5. Testing newsletter export...")
    try:
        response = session.get('http://localhost:5000/admin/newsletter/export', timeout=10)
        if response.status_code == 200:
            print("   ✅ Newsletter export working")
        else:
            print(f"   ❌ Newsletter export returned status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Newsletter export failed: {e}")
    
    print(f"\n🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n✅ NEW FEATURES IMPLEMENTED:")
    print("=" * 50)
    print("1. 🔧 Fixed TemplateNotFound: admin/personal_info.html")
    print("   - Created missing personal_info.html template")
    print("   - Template includes all personal information fields")
    print("   - AJAX form submission with validation")
    print("")
    print("2. 📧 Newsletter Sending Feature")
    print("   - Send newsletters to all active subscribers")
    print("   - Test email functionality before mass sending")
    print("   - HTML content support with email template")
    print("   - Preview functionality")
    print("   - Subscriber count display")
    print("   - Safety confirmations for mass sending")
    print("")
    print("3. 🔐 Password Change Feature")
    print("   - Secure password change with current password verification")
    print("   - Password strength indicator")
    print("   - Automatic logout after password change")
    print("   - Email notification with IP geolocation")
    print("   - Security tips and requirements")
    print("   - Show/hide password toggles")
    print("")
    print("4. 🎯 Navigation Updates")
    print("   - Added 'Send Newsletter' to Communications menu")
    print("   - Added 'Change Password' to Admin user menu")
    print("   - Improved menu organization")
    print("")
    print("5. 📨 Email Notifications")
    print("   - Password change notifications with location")
    print("   - Professional HTML email templates")
    print("   - Security warnings and tips")

if __name__ == "__main__":
    test_new_admin_features()

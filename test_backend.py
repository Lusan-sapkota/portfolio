#!/usr/bin/env python3
"""
Test script for newsletter and contact form functionality
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_newsletter_subscription():
    """Test newsletter subscription endpoint"""
    print("Testing Newsletter Subscription...")
    
    data = {
        'email': 'test@example.com'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/newsletter/subscribe", data=data)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {result}")
        print("✅ Newsletter subscription test completed\n")
        
    except Exception as e:
        print(f"❌ Newsletter subscription test failed: {e}\n")

def test_contact_form():
    """Test contact form submission endpoint"""
    print("Testing Contact Form Submission...")
    
    data = {
        'name': 'Test User',
        'email': 'testuser@example.com',
        'subject': 'Test Subject',
        'message': 'This is a test message for the contact form functionality. It should be at least 10 characters long.'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contact/submit", data=data)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {result}")
        print("✅ Contact form submission test completed\n")
        
    except Exception as e:
        print(f"❌ Contact form submission test failed: {e}\n")

def test_bot_detection():
    """Test bot detection with honeypot fields"""
    print("Testing Bot Detection...")
    
    # Test newsletter with honeypot
    newsletter_data = {
        'email': 'bot@example.com',
        'website': 'http://spamsite.com'  # Honeypot field
    }
    
    try:
        response = requests.post(f"{BASE_URL}/newsletter/subscribe", data=newsletter_data)
        result = response.json()
        print(f"Newsletter Bot Test - Status: {response.status_code}, Response: {result}")
    except Exception as e:
        print(f"Newsletter bot test error: {e}")
    
    # Test contact form with honeypot
    contact_data = {
        'name': 'Bot User',
        'email': 'bot@example.com', 
        'subject': 'Bot Message',
        'message': 'This is a bot message',
        'botcheck': 'checked'  # Honeypot field
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contact/submit", data=contact_data)
        result = response.json()
        print(f"Contact Bot Test - Status: {response.status_code}, Response: {result}")
        print("✅ Bot detection test completed\n")
    except Exception as e:
        print(f"Contact bot test error: {e}\n")

def test_rate_limiting():
    """Test rate limiting functionality"""
    print("Testing Rate Limiting...")
    
    # Try multiple newsletter submissions
    for i in range(6):  # Should trigger rate limit after 5
        data = {'email': f'test{i}@example.com'}
        try:
            response = requests.post(f"{BASE_URL}/newsletter/subscribe", data=data)
            result = response.json()
            print(f"Newsletter Request {i+1}: {result.get('status', 'unknown')}")
        except Exception as e:
            print(f"Newsletter request {i+1} error: {e}")
    
    print("✅ Rate limiting test completed\n")

if __name__ == "__main__":
    print("🚀 Starting Backend Functionality Tests...\n")
    
    test_newsletter_subscription()
    test_contact_form()
    test_bot_detection()
    test_rate_limiting()
    
    print("🎉 All tests completed!")

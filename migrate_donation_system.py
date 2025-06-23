#!/usr/bin/env python3
"""
Migration script to create new donation-related models and update existing ones.
Run this after updating models.py to add the new fields and tables.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import db
from models import PaymentMethod, ThanksgivingSettings, DonationSettings

def migrate_donation_system():
    """Create tables and add sample data for the new donation system"""
    # Import app after setting up the path
    import app
    
    with app.app.app_context():
        try:
            # Create all tables
            db.create_all()
            
            # Check if I need to create default settings
            if not DonationSettings.query.first():
                print("Creating default donation settings...")
                settings = DonationSettings(
                    default_currency='NPR',
                    enable_custom_amounts=True,
                    enable_anonymous_donations=True,
                    require_phone_verification=False,
                    auto_approve_donations=False
                )
                db.session.add(settings)
            
            if not ThanksgivingSettings.query.first():
                print("Creating default thanksgiving settings...")
                thanksgiving = ThanksgivingSettings(
                    page_title='Thank You to My Amazing Supporters',
                    page_description='I are grateful for the incredible support from my community.',
                    show_donor_names=True,
                    show_amounts=False,
                    show_messages=True,
                    min_amount_display=0.0,
                    anonymous_display_text='Anonymous Supporter',
                    thank_you_message='Your support means the world to me and helps keep my projects alive!',
                    is_active=True
                )
                db.session.add(thanksgiving)
            
            # Add sample payment methods
            if not PaymentMethod.query.first():
                print("Creating sample payment methods...")
                
                # NPR Payment Methods
                esewa = PaymentMethod(
                    currency='NPR',
                    method_name='wallet',
                    display_name='eSewa Wallet',
                    account_info='eSewa ID: 9800000000<br>Name: Your Name',
                    instructions='1. Open eSewa app<br>2. Select "Send Money"<br>3. Enter the eSewa ID above<br>4. Enter the donation amount<br>5. Complete the transaction',
                    is_active=True,
                    sort_order=1
                )
                
                khalti = PaymentMethod(
                    currency='NPR',
                    method_name='wallet',
                    display_name='Khalti Wallet',
                    account_info='Khalti ID: 9800000000<br>Name: Your Name',
                    instructions='1. Open Khalti app<br>2. Select "Send Money"<br>3. Enter the Khalti ID above<br>4. Enter the donation amount<br>5. Complete the transaction',
                    is_active=True,
                    sort_order=2
                )
                
                bank_npr = PaymentMethod(
                    currency='NPR',
                    method_name='bank_transfer',
                    display_name='Bank Transfer (Nepal)',
                    account_info='Bank: Your Bank Name<br>Account Name: Your Name<br>Account Number: 1234567890<br>Branch: Your Branch',
                    instructions='1. Visit your bank or use online banking<br>2. Transfer to the account details above<br>3. Use "Donation" as reference<br>4. Keep the transaction receipt',
                    is_active=True,
                    sort_order=3
                )
                
                # USD Payment Methods
                paypal = PaymentMethod(
                    currency='USD',
                    method_name='wallet',
                    display_name='PayPal',
                    account_info='PayPal Email: your-email@example.com',
                    instructions='1. Log in to your PayPal account<br>2. Send money to the email above<br>3. Select "Friends & Family"<br>4. Enter the donation amount<br>5. Add "Donation" in the note',
                    is_active=True,
                    sort_order=1
                )
                
                swift = PaymentMethod(
                    currency='USD',
                    method_name='swift_transfer',
                    display_name='Swift Transfer / Bank Transfer',
                    account_info='Bank: Your International Bank<br>Account Name: Your Name<br>Account Number: 1234567890<br>Swift Code: ABCDUS33<br>Routing Number: 123456789',
                    instructions='1. Contact your bank for international transfer<br>2. Use the account details above<br>3. Include "Donation" as reference<br>4. Transfer fees may apply',
                    is_active=True,
                    sort_order=2
                )
                
                payoneer = PaymentMethod(
                    currency='USD',
                    method_name='payoneer',
                    display_name='Payoneer',
                    account_info='Payoneer Email: your-email@example.com',
                    instructions='1. Log in to your Payoneer account<br>2. Send money to the email above<br>3. Enter the donation amount<br>4. Complete the transfer',
                    is_active=True,
                    sort_order=3
                )
                
                # Add all payment methods
                for method in [esewa, khalti, bank_npr, paypal, swift, payoneer]:
                    db.session.add(method)
            
            # Commit all changes
            db.session.commit()
            print("✅ Migration completed successfully!")
            print("🎉 New donation system features are ready!")
            print("\nNext steps:")
            print("1. Update payment method details in admin panel")
            print("2. Upload QR codes to static/assets/images/qr/")
            print("3. Configure email settings")
            print("4. Test the donation flow")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Migration failed: {e}")
            return False
            
    return True

if __name__ == '__main__':
    migrate_donation_system()

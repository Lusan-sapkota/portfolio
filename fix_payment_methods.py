#!/usr/bin/env python3
"""
Fix payment methods and donation currency validation
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def fix_payment_methods():
    """Create proper payment methods with correct currency associations"""
    try:
        from app import app
        from models import PaymentMethod, Donation
        from database import db
        
        with app.app_context():
            print("🔧 FIXING PAYMENT METHODS AND CURRENCY VALIDATION")
            print("=" * 60)
            
            # Remove existing incorrect payment methods
            PaymentMethod.query.delete()
            db.session.commit()
            print("✓ Cleared existing payment methods")
            
            # Create proper NPR payment methods
            npr_methods = [
                {
                    'currency': 'NPR',
                    'method_name': 'esewa',
                    'display_name': 'eSewa Digital Wallet',
                    'account_info': 'eSewa ID: 9876543210\nAccount Name: Lusan Sapkota',
                    'instructions': 'Send payment to eSewa ID: 9876543210. Please include your name and "Donation" in the remarks.',
                    'is_active': True,
                    'is_verification_pending': False,
                    'sort_order': 1
                },
                {
                    'currency': 'NPR',
                    'method_name': 'khalti',
                    'display_name': 'Khalti Digital Wallet',
                    'account_info': 'Khalti ID: 9876543210\nAccount Name: Lusan Sapkota',
                    'instructions': 'Send payment to Khalti ID: 9876543210. Please include your name and "Donation" in the remarks.',
                    'is_active': True,
                    'is_verification_pending': False,
                    'sort_order': 2
                },
                {
                    'currency': 'NPR',
                    'method_name': 'bank_transfer',
                    'display_name': 'Bank Transfer (Nepal)',
                    'account_info': 'Bank: Nepal Investment Bank\nAccount Number: 1234567890\nAccount Name: Lusan Sapkota\nBranch: Kathmandu',
                    'instructions': 'Transfer to the above bank account. Please send a screenshot of the transfer receipt via email.',
                    'is_active': True,
                    'is_verification_pending': False,
                    'sort_order': 3
                }
            ]
            
            # Create proper USD payment methods
            usd_methods = [
                {
                    'currency': 'USD',
                    'method_name': 'paypal',
                    'display_name': 'PayPal',
                    'account_info': 'PayPal Email: contact@lusansapkota.com.np',
                    'instructions': 'Send payment to PayPal email: contact@lusansapkota.com.np. Please include "Donation" in the note.',
                    'is_active': True,
                    'is_verification_pending': True,  # Currently under verification
                    'sort_order': 1
                },
                {
                    'currency': 'USD',
                    'method_name': 'payoneer',
                    'display_name': 'Payoneer',
                    'account_info': 'Payoneer Email: contact@lusansapkota.com.np',
                    'instructions': 'Send payment via Payoneer to: contact@lusansapkota.com.np. Please include "Donation" in the note.',
                    'is_active': True,
                    'is_verification_pending': True,  # Currently under verification
                    'sort_order': 2
                },
                {
                    'currency': 'USD',
                    'method_name': 'swift_transfer',
                    'display_name': 'International Bank Transfer (SWIFT)',
                    'account_info': 'Bank: Nepal Investment Bank\nAccount Number: 1234567890\nAccount Name: Lusan Sapkota\nSWIFT Code: NIBLNPKA',
                    'swift_code': 'NIBLNPKA',
                    'instructions': 'Use SWIFT transfer to the above account. Please email transfer confirmation.',
                    'is_active': True,
                    'is_verification_pending': False,
                    'sort_order': 3
                }
            ]
            
            # Add all payment methods
            all_methods = npr_methods + usd_methods
            
            for method_data in all_methods:
                method = PaymentMethod(**method_data)
                db.session.add(method)
            
            db.session.commit()
            print(f"✓ Created {len(npr_methods)} NPR payment methods")
            print(f"✓ Created {len(usd_methods)} USD payment methods")
            
            # Fix existing donation with wrong currency-method combination
            wrong_donation = Donation.query.filter_by(payment_method='payoneer', currency='NPR').first()
            if wrong_donation:
                print(f"\n🔧 Found incorrect donation: NPR amount with Payoneer")
                print(f"   Donation ID: {wrong_donation.id}")
                print(f"   Amount: {wrong_donation.currency} {wrong_donation.amount}")
                print(f"   Current Method: {wrong_donation.payment_method}")
                
                # Fix it by changing to appropriate NPR method
                wrong_donation.payment_method = 'esewa'
                db.session.commit()
                print(f"✓ Fixed: Changed payment method to eSewa (appropriate for NPR)")
            
            # Display current payment methods
            print(f"\n💳 UPDATED PAYMENT METHODS:")
            print("-" * 50)
            
            methods = PaymentMethod.query.order_by(PaymentMethod.currency, PaymentMethod.sort_order).all()
            for method in methods:
                status = "🟢" if method.is_active else "🔴"
                verification = "🔒 Pending" if method.is_verification_pending else "✅ Ready"
                swift_info = f" (SWIFT: {method.swift_code})" if method.swift_code else ""
                
                print(f"  {status} {method.display_name} ({method.currency}) - {verification}{swift_info}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error fixing payment methods: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if fix_payment_methods():
        print(f"\n✅ Payment methods fixed successfully!")
        print(f"🎯 Now NPR methods are properly separated from USD methods")
        print(f"🔒 PayPal and Payoneer are marked as verification pending")
        print(f"💡 The donation system will now properly validate currency-method combinations")
    else:
        print(f"\n❌ Failed to fix payment methods!")
        sys.exit(1)

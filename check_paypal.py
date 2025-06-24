#!/usr/bin/env python3
"""Check PayPal payment method verification status"""

from app import app
from models import PaymentMethod

def check_paypal_methods():
    with app.app_context():
        # Check PayPal payment methods
        paypal_methods = PaymentMethod.query.filter(PaymentMethod.method_name.ilike('%paypal%')).all()
        
        if not paypal_methods:
            print("No PayPal payment methods found")
            # Also check by display_name
            paypal_methods = PaymentMethod.query.filter(PaymentMethod.display_name.ilike('%paypal%')).all()
            
        for method in paypal_methods:
            print(f'PayPal Method: {method.method_name} ({method.display_name})')
            print(f'  ID: {method.id}')
            print(f'  Currency: {method.currency}')
            print(f'  Is Verification Pending: {method.is_verification_pending}')
            print(f'  Account Info: {method.account_info}')
            print(f'  Instructions: {method.instructions}')
            print(f'  Is Active: {method.is_active}')
            print('---')

if __name__ == '__main__':
    check_paypal_methods()

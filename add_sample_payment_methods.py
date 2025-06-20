#!/usr/bin/env python3

from app import app
from models import PaymentMethod, db

def add_sample_payment_methods():
    """Add sample payment methods for testing"""
    
    with app.app_context():
        # Check if payment methods already exist
        existing = PaymentMethod.query.count()
        if existing > 0:
            print(f"Found {existing} existing payment methods. Skipping creation.")
            return
        
        # NPR Payment Methods
        methods = [
            {
                'display_name': 'eSewa',
                'method_type': 'wallet',
                'currency': 'NPR',
                'account_info': '9848189845',
                'instructions': '''<ol>
<li>Open eSewa app or visit esewa.com.np</li>
<li>Select "Send Money" or "Transfer"</li>
<li>Enter ID: <strong>9848189845</strong></li>
<li>Enter amount: <strong>NPR {amount}</strong></li>
<li>Add reference: <strong>Donation - {project}</strong></li>
<li>Complete payment and keep transaction ID</li>
</ol>''',
                'qr_code_url': '/static/assets/images/qr/esewa-qr.png',
                'is_active': True,
                'sort_order': 1
            },
            {
                'display_name': 'Khalti',
                'method_type': 'wallet',
                'currency': 'NPR',
                'account_info': '9848189845',
                'instructions': '''<ol>
<li>Open Khalti app or visit khalti.com</li>
<li>Select "Send Money"</li>
<li>Enter Mobile: <strong>9848189845</strong></li>
<li>Enter amount: <strong>NPR {amount}</strong></li>
<li>Add note: <strong>Donation for {project}</strong></li>
<li>Complete payment using PIN/Password</li>
</ol>''',
                'qr_code_url': '/static/assets/images/qr/khalti-qr.png',
                'is_active': True,
                'sort_order': 2
            },
            {
                'display_name': 'IME Pay',
                'method_type': 'wallet',
                'currency': 'NPR',
                'account_info': '9848189845',
                'instructions': '''<ol>
<li>Open IME Pay app</li>
<li>Select "Send Money" from menu</li>
<li>Enter Mobile: <strong>9848189845</strong></li>
<li>Enter amount: <strong>NPR {amount}</strong></li>
<li>Add remarks: <strong>Donation - {project}</strong></li>
<li>Verify details and confirm payment</li>
</ol>''',
                'qr_code_url': '/static/assets/images/qr/imepay-qr.png',
                'is_active': True,
                'sort_order': 3
            },
            {
                'display_name': 'Bank Transfer',
                'method_type': 'bank_transfer',
                'currency': 'NPR',
                'account_info': '''<strong>Account Name:</strong> Lusan Sapkota<br>
<strong>Bank:</strong> Nepal Investment Bank Ltd.<br>
<strong>Account Number:</strong> 0123456789<br>
<strong>Branch:</strong> Kathmandu<br>
<strong>SWIFT Code:</strong> NIBLNPKA''',
                'instructions': '''<ol>
<li>Visit your bank or use online banking</li>
<li>Transfer to the account details shown</li>
<li>Use reference: <strong>Donation - {project}</strong></li>
<li>Keep the transaction receipt</li>
<li>We'll verify within 24 hours</li>
</ol>''',
                'is_active': True,
                'sort_order': 4
            },
            # USD Payment Methods
            {
                'display_name': 'PayPal',
                'method_type': 'wallet',
                'currency': 'USD',
                'account_info': 'sapkotalusan@gmail.com',
                'instructions': '''<ol>
<li>Open PayPal app or visit paypal.com</li>
<li>Select "Send Money"</li>
<li>Enter email: <strong>sapkotalusan@gmail.com</strong></li>
<li>Enter amount: <strong>${amount} USD</strong></li>
<li>Add note: <strong>Donation for {project}</strong></li>
<li>Complete payment</li>
</ol>''',
                'is_active': True,
                'sort_order': 5
            },
            {
                'display_name': 'Wise (Bank Transfer)',
                'method_type': 'swift_transfer',
                'currency': 'USD',
                'account_info': '''<strong>Account Name:</strong> Lusan Sapkota<br>
<strong>Email:</strong> sapkotalusan@gmail.com<br>
<strong>Wise Profile:</strong> wise.com/user/lusansapkota''',
                'instructions': '''<ol>
<li>Visit wise.com or open Wise app</li>
<li>Send money to sapkotalusan@gmail.com</li>
<li>Amount: <strong>${amount} USD</strong></li>
<li>Add reference: <strong>Donation - {project}</strong></li>
<li>Processing takes 1-3 business days</li>
</ol>''',
                'is_active': True,
                'sort_order': 6
            }
        ]
        
        for method_data in methods:
            method = PaymentMethod(**method_data)
            db.session.add(method)
        
        try:
            db.session.commit()
            print(f"✅ Successfully added {len(methods)} payment methods!")
            
            # List what was created
            for method in PaymentMethod.query.all():
                print(f"  📱 {method.display_name} ({method.currency}) - {method.method_type}")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error adding payment methods: {e}")

if __name__ == '__main__':
    add_sample_payment_methods()

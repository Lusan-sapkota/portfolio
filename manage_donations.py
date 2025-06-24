#!/usr/bin/env python3
"""
Donation Management Script - Handle donation statuses and testing
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def manage_donations():
    """Manage donation statuses and show current donations"""
    try:
        from app import app
        from models import Donation, DonationProject
        from database import db
        
        with app.app_context():
            print("=== DONATION MANAGEMENT ===")
            
            # Show all donations
            all_donations = Donation.query.order_by(Donation.created_at.desc()).all()
            print(f"\n📊 Total Donations: {len(all_donations)}")
            
            for donation in all_donations:
                project_name = donation.project.title if donation.project else "General"
                print(f"\n💰 Donation #{donation.id}")
                print(f"   Donor: {donation.donor_name if not donation.is_anonymous else 'Anonymous'}")
                print(f"   Amount: {donation.currency} {donation.amount}")
                print(f"   Project: {project_name}")
                print(f"   Status: {donation.status}")
                print(f"   Payment Method: {donation.payment_method}")
                print(f"   Date: {donation.created_at}")
                print(f"   Anonymous: {donation.is_anonymous}")
                if donation.message:
                    print(f"   Message: {donation.message}")
            
            # Show completed donations (what appears in Recent Support)
            completed = Donation.query.filter_by(status='completed').all()
            print(f"\n✅ Completed Donations (shown in Recent Support): {len(completed)}")
            
            # Show pending donations
            pending = Donation.query.filter_by(status='pending').all()
            print(f"⏳ Pending Donations: {len(pending)}")
            
            # Interactive management
            if pending:
                print(f"\n🔧 PENDING DONATION MANAGEMENT")
                for i, donation in enumerate(pending, 1):
                    project_name = donation.project.title if donation.project else "General"
                    print(f"{i}. {donation.donor_name} - {donation.currency} {donation.amount} to {project_name}")
                
                try:
                    choice = input(f"\nEnter donation number to mark as completed (1-{len(pending)}) or 'skip': ").strip()
                    
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(pending):
                            donation = pending[idx]
                            donation.status = 'completed'
                            db.session.commit()
                            print(f"✅ Marked donation #{donation.id} as completed!")
                            print(f"   This donation will now appear in 'Recent Support'")
                        else:
                            print("Invalid choice.")
                    else:
                        print("Skipping donation management.")
                        
                except Exception as e:
                    print(f"Error: {e}")
            
            # Create test donations if none exist
            if len(all_donations) == 0:
                print(f"\n🎯 Creating test donations...")
                create_test_donations()
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def create_test_donations():
    """Create some test donations for demonstration"""
    try:
        from app import app
        from models import Donation, DonationProject
        from database import db
        from datetime import datetime, timedelta
        
        with app.app_context():
            # Get the first project
            project = DonationProject.query.first()
            if not project:
                print("❌ No donation projects found. Create a project first.")
                return
            
            test_donations = [
                {
                    'donor_name': 'John Doe',
                    'donor_email': 'john@example.com',
                    'amount': 50.0,
                    'currency': 'USD',
                    'message': 'Great work! Keep it up!',
                    'is_anonymous': False,
                    'status': 'completed',
                    'payment_method': 'PayPal',
                    'project_id': project.id,
                    'created_at': datetime.utcnow() - timedelta(days=1)
                },
                {
                    'donor_name': 'Anonymous Supporter',
                    'donor_email': 'anon@example.com',
                    'amount': 2500.0,
                    'currency': 'NPR',
                    'message': 'Supporting innovation in Nepal!',
                    'is_anonymous': True,
                    'status': 'completed',
                    'payment_method': 'eSewa',
                    'project_id': project.id,
                    'created_at': datetime.utcnow() - timedelta(days=2)
                },
                {
                    'donor_name': 'Tech Enthusiast',
                    'donor_email': 'tech@example.com',
                    'amount': 100.0,
                    'currency': 'USD',
                    'message': 'Love your projects!',
                    'is_anonymous': False,
                    'status': 'completed',
                    'payment_method': 'Bank Transfer',
                    'project_id': project.id,
                    'created_at': datetime.utcnow() - timedelta(hours=12)
                }
            ]
            
            for donation_data in test_donations:
                donation = Donation(**donation_data)
                db.session.add(donation)
            
            db.session.commit()
            print(f"✅ Created {len(test_donations)} test donations")
            
    except Exception as e:
        print(f"❌ Error creating test donations: {str(e)}")

if __name__ == '__main__':
    print("🎯 Donation Management System")
    print("=" * 40)
    manage_donations()

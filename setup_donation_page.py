#!/usr/bin/env python3
"""
Script to add more donation projects and test data for a complete donation page
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_donation_page():
    """Set up donation page with proper projects and test data"""
    try:
        from app import app
        from models import DonationProject, Donation
        from database import db
        from datetime import datetime, timedelta
        
        with app.app_context():
            print("🎯 Setting up donation page...")
            
            # Additional donation projects
            additional_projects = [
                {
                    'title': 'Open Source Nepal Initiative',
                    'description': 'Building open-source tools and libraries specifically for the Nepali tech community. This includes localization tools, Nepali language processing libraries, and educational resources.',
                    'short_description': 'Open-source tools for the Nepali tech community',
                    'goal_amount': 3000.0,
                    'is_featured': False,
                    'is_active': True
                },
                {
                    'title': 'Rural Tech Education Program',
                    'description': 'Bringing technology education to rural areas of Nepal through mobile workshops, free coding bootcamps, and providing computers to underserved communities.',
                    'short_description': 'Technology education for rural Nepal communities',
                    'goal_amount': 150000.0,
                    'is_featured': False,
                    'is_active': True
                }
            ]
            
            created_count = 0
            for project_data in additional_projects:
                existing = DonationProject.query.filter_by(title=project_data['title']).first()
                if not existing:
                    # Remove any fields that don't exist in the model
                    project_fields = {k: v for k, v in project_data.items() 
                                    if k in ['title', 'description', 'short_description', 'goal_amount', 
                                            'is_featured', 'is_active', 'image_url', 'github_url', 'demo_url']}
                    project = DonationProject(**project_fields)
                    db.session.add(project)
                    created_count += 1
                    print(f"✅ Created: {project_data['title']}")
                else:
                    print(f"📋 Exists: {project_data['title']}")
            
            db.session.commit()
            
            # Add some test donations for variety
            projects = DonationProject.query.filter_by(is_active=True).all()
            if projects and len(Donation.query.filter_by(status='completed').all()) < 5:
                print(f"\n💝 Adding test donations...")
                
                test_donations = [
                    {
                        'donor_name': 'Anonymous Supporter',
                        'donor_email': 'anon1@example.com',
                        'amount': 25000.0,
                        'currency': 'NPR',
                        'message': 'Supporting local tech development!',
                        'is_anonymous': True,
                        'status': 'completed',
                        'payment_method': 'khalti',
                        'project_id': projects[0].id,
                        'created_at': datetime.utcnow() - timedelta(days=3)
                    },
                    {
                        'donor_name': 'Tech Enthusiast',
                        'donor_email': 'tech@example.com',
                        'amount': 75.0,
                        'currency': 'USD',
                        'message': 'Amazing work on open source!',
                        'is_anonymous': False,
                        'status': 'completed',
                        'payment_method': 'swift_transfer',
                        'project_id': projects[-1].id if len(projects) > 1 else projects[0].id,
                        'created_at': datetime.utcnow() - timedelta(days=1, hours=5)
                    },
                    {
                        'donor_name': 'Community Supporter',
                        'donor_email': 'community@example.com',
                        'amount': 5000.0,
                        'currency': 'NPR',
                        'message': '',
                        'is_anonymous': False,
                        'status': 'completed',
                        'payment_method': 'esewa',
                        'project_id': projects[0].id,
                        'created_at': datetime.utcnow() - timedelta(hours=8)
                    }
                ]
                
                donation_count = 0
                for donation_data in test_donations:
                    donation = Donation(**donation_data)
                    db.session.add(donation)
                    donation_count += 1
                
                db.session.commit()
                print(f"✅ Added {donation_count} test donations")
            
            # Final status
            total_projects = DonationProject.query.filter_by(is_active=True).count()
            featured_projects = DonationProject.query.filter_by(is_active=True, is_featured=True).count()
            completed_donations = Donation.query.filter_by(status='completed').count()
            
            print(f"\n🎉 Donation page setup complete!")
            print(f"   📋 Total active projects: {total_projects}")
            print(f"   ✨ Featured projects: {featured_projects}")
            print(f"   💝 Completed donations: {completed_donations}")
            
            print(f"\n🌐 Your donation page now has:")
            print(f"   - Featured projects section with highlight")
            print(f"   - All projects section (including featured)")
            print(f"   - Recent support section (completed donations only)")
            print(f"   - Proper currency handling (NPR/USD)")
            print(f"   - Anonymous donation support")
            print(f"   - Verification pending payment method handling")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Donation Page Setup")
    print("=" * 40)
    
    if setup_donation_page():
        print(f"\n✅ Setup completed successfully!")
        print(f"🌐 Visit http://127.0.0.1:5000/donation/ to see your enhanced donation page!")
    else:
        print(f"\n❌ Setup failed!")
        sys.exit(1)

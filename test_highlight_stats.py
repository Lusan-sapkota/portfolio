#!/usr/bin/env python3
"""
Test script to verify highlight page achievement statistics
"""

from app import app
from models import db, DonationProject, Donation, Project

def test_highlight_stats():
    """Test the achievement statistics calculations"""
    with app.app_context():
        try:
            # Get all donation projects and regular projects
            all_donation_projects = DonationProject.query.filter_by(is_active=True).all()
            all_regular_projects = Project.query.all()
            
            # Total project count
            total_projects = len(all_donation_projects) + len(all_regular_projects)
            
            # Count completed donation projects
            completed_projects = DonationProject.query.filter(
                DonationProject.current_amount >= DonationProject.goal_amount
            ).all()
            completed_count = len(completed_projects)
            
            # Count featured projects
            featured_donation_count = DonationProject.query.filter_by(is_featured=True).count()
            featured_regular_count = Project.query.filter_by(is_featured=True).count()
            total_featured = featured_donation_count + featured_regular_count
            
            # Calculate total raised in different currencies
            total_usd = db.session.query(db.func.sum(Donation.amount)).filter(
                Donation.status == 'completed',
                Donation.currency == 'USD'
            ).scalar() or 0
            
            total_npr = db.session.query(db.func.sum(Donation.amount)).filter(
                Donation.status == 'completed',
                Donation.currency == 'NPR'
            ).scalar() or 0
            
            # Format the totals for display
            if total_usd > 0 and total_npr > 0:
                total_raised_display = f"${total_usd:,.0f} / Rs.{total_npr:,.0f}"
            elif total_usd > 0:
                total_raised_display = f"${total_usd:,.0f}"
            elif total_npr > 0:
                total_raised_display = f"Rs.{total_npr:,.0f}"
            else:
                total_raised_display = "$0 / Rs.0"
            
            # Count unique supporters
            supporter_count = db.session.query(db.func.count(db.func.distinct(Donation.donor_email))).filter_by(status='completed').scalar() or 0
            
            # Print results
            print("=" * 50)
            print("HIGHLIGHT PAGE ACHIEVEMENT STATISTICS")
            print("=" * 50)
            print(f"Total Projects: {total_projects}")
            print(f"  - Donation Projects: {len(all_donation_projects)}")
            print(f"  - Regular Projects: {len(all_regular_projects)}")
            print(f"Completed Projects: {completed_count}")
            print(f"Featured Projects: {total_featured}")
            print(f"  - Featured Donation Projects: {featured_donation_count}")
            print(f"  - Featured Regular Projects: {featured_regular_count}")
            print(f"Total Raised: {total_raised_display}")
            print(f"  - USD: ${total_usd:,.2f}")
            print(f"  - NPR: Rs.{total_npr:,.2f}")
            print(f"Unique Supporters: {supporter_count}")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"Error testing highlight statistics: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = test_highlight_stats()
    exit(0 if success else 1)

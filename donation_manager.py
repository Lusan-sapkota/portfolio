#!/usr/bin/env python3
"""
Donation Management Utility
View, sort, and manage donations with proper currency handling
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def view_donations():
    """Display all donations with proper sorting and formatting"""
    try:
        from app import app
        from models import Donation, DonationProject, Project, PaymentMethod
        from database import db
        
        with app.app_context():
            print("💰 DONATION MANAGEMENT DASHBOARD")
            print("=" * 60)
            
            # Get all donations with sorting options
            print("\n📊 DONATION SUMMARY BY STATUS:")
            statuses = ['pending', 'completed', 'failed', 'cancelled']
            
            for status in statuses:
                count = Donation.query.filter_by(status=status).count()
                if count > 0:
                    total_usd = db.session.query(db.func.sum(Donation.amount)).filter(
                        Donation.status == status, Donation.currency == 'USD'
                    ).scalar() or 0
                    
                    total_npr = db.session.query(db.func.sum(Donation.amount)).filter(
                        Donation.status == status, Donation.currency == 'NPR'
                    ).scalar() or 0
                    
                    print(f"  {status.upper()}: {count} donations")
                    if total_usd > 0:
                        print(f"    USD: ${total_usd:,.2f}")
                    if total_npr > 0:
                        print(f"    NPR: Rs.{total_npr:,.2f}")
            
            print("\n📋 RECENT DONATIONS (Last 20):")
            print("-" * 60)
            
            recent_donations = Donation.query.order_by(Donation.created_at.desc()).limit(20).all()
            
            if not recent_donations:
                print("No donations found.")
                return
            
            # Display donations in a formatted table
            print(f"{'ID':<4} {'Date':<12} {'Donor':<20} {'Amount':<15} {'Currency':<8} {'Method':<15} {'Status':<10}")
            print("-" * 100)
            
            for donation in recent_donations:
                # Get project name
                project_name = "Unknown"
                try:
                    if donation.project_id:
                        project = DonationProject.query.get(donation.project_id)
                        if not project:
                            project = Project.query.get(donation.project_id)
                        if project:
                            project_name = project.title[:15] + "..." if len(project.title) > 15 else project.title
                except:
                    pass
                
                donor_name = donation.donor_name or "Anonymous"
                if len(donor_name) > 20:
                    donor_name = donor_name[:17] + "..."
                
                amount_str = f"{donation.currency} {donation.amount:,.2f}"
                date_str = donation.created_at.strftime("%Y-%m-%d") if donation.created_at else "Unknown"
                
                # Status with emoji
                status_emoji = {
                    'pending': '⏳',
                    'completed': '✅',
                    'failed': '❌',
                    'cancelled': '🚫'
                }
                status_display = f"{status_emoji.get(donation.status, '❓')} {donation.status}"
                
                print(f"{donation.id:<4} {date_str:<12} {donor_name:<20} {amount_str:<15} {donation.currency:<8} {(donation.payment_method or 'Manual')[:15]:<15} {status_display:<10}")
            
            print("\n💳 PAYMENT METHODS STATUS:")
            print("-" * 40)
            
            payment_methods = PaymentMethod.query.order_by(PaymentMethod.currency, PaymentMethod.sort_order).all()
            
            for method in payment_methods:
                status = "🟢" if method.is_active else "🔴"
                verification = "🔒 Pending" if method.is_verification_pending else "✅ Ready"
                swift_info = f" (SWIFT: {method.swift_code})" if method.swift_code else ""
                
                print(f"  {status} {method.display_name} ({method.currency}) - {verification}{swift_info}")
            
            print("\n🎯 DONATION INSIGHTS:")
            print("-" * 30)
            
            # Top currencies
            usd_total = db.session.query(db.func.sum(Donation.amount)).filter(
                Donation.status == 'completed', Donation.currency == 'USD'
            ).scalar() or 0
            
            npr_total = db.session.query(db.func.sum(Donation.amount)).filter(
                Donation.status == 'completed', Donation.currency == 'NPR'
            ).scalar() or 0
            
            print(f"  💵 Total USD Raised: ${usd_total:,.2f}")
            print(f"  💰 Total NPR Raised: Rs.{npr_total:,.2f}")
            
            # Unique donors
            unique_donors = db.session.query(db.func.count(db.func.distinct(Donation.donor_email))).filter_by(status='completed').scalar() or 0
            print(f"  👥 Unique Supporters: {unique_donors}")
            
            # Average donation
            if recent_donations:
                completed_donations = [d for d in recent_donations if d.status == 'completed']
                if completed_donations:
                    avg_usd = sum(d.amount for d in completed_donations if d.currency == 'USD') / max(1, len([d for d in completed_donations if d.currency == 'USD']))
                    avg_npr = sum(d.amount for d in completed_donations if d.currency == 'NPR') / max(1, len([d for d in completed_donations if d.currency == 'NPR']))
                    
                    if avg_usd > 0:
                        print(f"  📊 Average USD Donation: ${avg_usd:.2f}")
                    if avg_npr > 0:
                        print(f"  📊 Average NPR Donation: Rs.{avg_npr:.2f}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error viewing donations: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_donation_status():
    """Interactive tool to update donation status"""
    try:
        from app import app
        from models import Donation
        from database import db
        
        with app.app_context():
            print("\n🔧 UPDATE DONATION STATUS")
            print("-" * 30)
            
            # Get pending donations
            pending = Donation.query.filter_by(status='pending').order_by(Donation.created_at.desc()).all()
            
            if not pending:
                print("No pending donations to update.")
                return
            
            print(f"Found {len(pending)} pending donation(s):")
            
            for i, donation in enumerate(pending, 1):
                print(f"{i}. ID: {donation.id} - {donation.donor_name} - {donation.currency} {donation.amount} - {donation.payment_method}")
            
            try:
                choice = int(input(f"\nSelect donation to update (1-{len(pending)}, 0 to cancel): "))
                if choice == 0:
                    return
                
                if 1 <= choice <= len(pending):
                    donation = pending[choice - 1]
                    
                    print(f"\nSelected: {donation.donor_name} - {donation.currency} {donation.amount}")
                    print("Status options:")
                    print("1. Completed")
                    print("2. Failed") 
                    print("3. Cancelled")
                    
                    status_choice = int(input("Select new status (1-3): "))
                    status_map = {1: 'completed', 2: 'failed', 3: 'cancelled'}
                    
                    if status_choice in status_map:
                        old_status = donation.status
                        donation.status = status_map[status_choice]
                        db.session.commit()
                        
                        print(f"✅ Updated donation {donation.id} status: {old_status} → {donation.status}")
                    else:
                        print("Invalid status choice.")
                else:
                    print("Invalid donation choice.")
                    
            except ValueError:
                print("Invalid input. Please enter a number.")
                
    except Exception as e:
        print(f"❌ Error updating donation: {e}")

if __name__ == '__main__':
    print("🎯 Portfolio Donation Management")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. View all donations")
        print("2. Update donation status") 
        print("3. Exit")
        
        try:
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == '1':
                view_donations()
            elif choice == '2':
                update_donation_status()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1-3.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

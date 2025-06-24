#!/usr/bin/env python3
"""
Script to add sample donation projects for testing and demonstration
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_sample_donation_projects():
    """Create sample donation projects for the donation page"""
    try:
        from app import app
        from models import DonationProject
        from database import db
        
        with app.app_context():
            # Sample donation projects
            sample_projects = [
                {
                    'title': 'AI Research & Development Initiative',
                    'description': 'Funding research into cutting-edge AI technologies and machine learning algorithms. This project aims to develop innovative solutions for real-world problems using artificial intelligence.',
                    'short_description': 'Support AI research and development for innovative solutions',
                    'goal_amount': 5000.0,
                    'currency': 'USD',
                    'image_url': '/static/assets/images/projects/ai-research.jpg',
                    'is_featured': True,
                    'is_active': True,
                    'priority': 1
                },
                {
                    'title': 'Open Source Development Tools',
                    'description': 'Creating free, open-source development tools and libraries that benefit the entire programming community. These tools will help developers worldwide build better software faster.',
                    'short_description': 'Build open-source tools for the developer community',
                    'goal_amount': 3000.0,
                    'currency': 'USD',
                    'image_url': '/static/assets/images/projects/open-source.jpg',
                    'is_featured': False,
                    'is_active': True,
                    'priority': 2
                },
                {
                    'title': 'Educational Platform Development',
                    'description': 'Building an online educational platform to provide free programming and technology courses to students in Nepal and developing countries.',
                    'short_description': 'Free educational platform for programming courses',
                    'goal_amount': 2500.0,
                    'currency': 'USD',
                    'image_url': '/static/assets/images/projects/education.jpg',
                    'is_featured': False,
                    'is_active': True,
                    'priority': 3
                },
                {
                    'title': 'Mobile App Innovation Lab',
                    'description': 'Establishing a mobile app development lab focused on creating innovative mobile applications that solve local problems and improve daily life.',
                    'short_description': 'Innovation lab for mobile app development',
                    'goal_amount': 4000.0,
                    'currency': 'USD',
                    'image_url': '/static/assets/images/projects/mobile-lab.jpg',
                    'is_featured': False,
                    'is_active': True,
                    'priority': 4
                },
                {
                    'title': 'Community Tech Workshops',
                    'description': 'Organizing free technology workshops and coding bootcamps for underprivileged youth in rural areas of Nepal.',
                    'short_description': 'Free tech workshops for underprivileged youth',
                    'goal_amount': 1500.0,
                    'currency': 'USD',
                    'image_url': '/static/assets/images/projects/workshops.jpg',
                    'is_featured': False,
                    'is_active': True,
                    'priority': 5
                }
            ]
            
            created_count = 0
            updated_count = 0
            
            for project_data in sample_projects:
                # Check if project already exists
                existing = DonationProject.query.filter_by(title=project_data['title']).first()
                
                if existing:
                    # Update existing project
                    for key, value in project_data.items():
                        setattr(existing, key, value)
                    updated_count += 1
                    print(f"✓ Updated: {project_data['title']}")
                else:
                    # Create new project
                    project = DonationProject(**project_data)
                    db.session.add(project)
                    created_count += 1
                    print(f"✓ Created: {project_data['title']}")
            
            db.session.commit()
            
            print(f"\n✅ Sample donation projects setup completed!")
            print(f"   Created: {created_count} new projects")
            print(f"   Updated: {updated_count} existing projects")
            
            # Show current status
            total_projects = DonationProject.query.count()
            active_projects = DonationProject.query.filter_by(is_active=True).count()
            featured_projects = DonationProject.query.filter_by(is_featured=True, is_active=True).count()
            
            print(f"\n📊 Current Status:")
            print(f"   Total Projects: {total_projects}")
            print(f"   Active Projects: {active_projects}")
            print(f"   Featured Projects: {featured_projects}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating sample projects: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🎯 Creating Sample Donation Projects")
    print("=" * 40)
    
    if create_sample_donation_projects():
        print("\n🎉 Sample projects created successfully!")
        print("Visit /donation to see your projects!")
    else:
        print("\n💥 Failed to create sample projects!")
        sys.exit(1)

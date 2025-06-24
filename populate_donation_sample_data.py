#!/usr/bin/env python3
"""
Populate sample donation data for testing
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db
from models import DonationProject, Donation, NewsletterSubscriber

def populate_donation_data():
    """Populate database with sample donation data"""
    
    with app.app_context():
        try:
            # Sample donation projects
            projects_data = [
                {
                    'title': 'Open Source Portfolio CMS',
                    'description': '''A comprehensive Content Management System built for developers to easily manage their portfolio websites. 
                    
Features include:
- Dynamic content management for projects, skills, and experience
- SEO optimization tools and meta tag management
- Contact form and newsletter management
- Responsive admin dashboard with CRUD operations
- Email integration for notifications and auto-replies
- Dark/light theme support
- Donation management system

This project aims to help developers showcase their work professionally while maintaining full control over their content. Your support will help add more features like analytics integration, advanced SEO tools, and mobile app companion.''',
                    'short_description': 'A comprehensive CMS for developer portfolios with admin dashboard, SEO tools, and donation management.',
                    'goal_amount': 5000.0,
                    'current_amount': 1250.0,
                    'image_url': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop',
                    'github_url': 'https://github.com/lusansapkota/portfolio-cms',
                    'demo_url': 'https://lusansapkota.com.np',
                    'is_active': True,
                    'is_featured': True
                },
                {
                    'title': 'AI-Powered Code Review Tool',
                    'description': '''An intelligent code review tool that uses machine learning to identify potential bugs, security vulnerabilities, and code quality issues.

Key Features:
- Automated code analysis using AI/ML algorithms
- Integration with popular version control systems
- Real-time feedback and suggestions
- Security vulnerability detection
- Performance optimization recommendations
- Custom rule configuration
- Team collaboration features

This tool will help developers write better, more secure code while reducing manual review time. Your donation will support the development of advanced AI models and integration with more platforms.''',
                    'short_description': 'AI-powered tool for automated code review, bug detection, and security analysis.',
                    'goal_amount': 8000.0,
                    'current_amount': 3200.0,
                    'image_url': 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=400&fit=crop',
                    'github_url': 'https://github.com/lusansapkota/ai-code-review',
                    'demo_url': 'https://code-review.lusansapkota.com.np',
                    'is_active': True,
                    'is_featured': True
                },
                {
                    'title': 'Real-time Collaboration Platform',
                    'description': '''A modern real-time collaboration platform for remote teams, featuring video calls, screen sharing, collaborative editing, and project management tools.

Features:
- HD video conferencing with screen sharing
- Real-time collaborative document editing
- Project management with kanban boards
- File sharing and version control
- Team chat and messaging
- Calendar integration
- Mobile app support

This platform aims to improve remote work productivity and team collaboration. Your support will help me add advanced features like AI meeting summaries, advanced analytics, and enterprise-grade security.''',
                    'short_description': 'Real-time collaboration platform with video calls, document editing, and project management.',
                    'goal_amount': 12000.0,
                    'current_amount': 4800.0,
                    'image_url': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&h=400&fit=crop',
                    'github_url': 'https://github.com/lusansapkota/collab-platform',
                    'demo_url': 'https://collab.lusansapkota.com.np',
                    'is_active': True,
                    'is_featured': False
                },
                {
                    'title': 'Mobile App Development Framework',
                    'description': '''A cross-platform mobile app development framework that simplifies building native-quality apps for iOS and Android using web technologies.

Features:
- Cross-platform compatibility
- Native performance optimization
- Rich UI component library
- Built-in state management
- Hot reload development
- Easy deployment tools
- Comprehensive documentation

This framework will help developers build high-quality mobile apps faster and more efficiently. Your contribution will support the development of advanced components, testing tools, and performance optimizations.''',
                    'short_description': 'Cross-platform mobile development framework for building native-quality apps.',
                    'goal_amount': 6500.0,
                    'current_amount': 2100.0,
                    'image_url': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&h=400&fit=crop',
                    'github_url': 'https://github.com/lusansapkota/mobile-framework',
                    'is_active': True,
                    'is_featured': False
                },
                {
                    'title': 'Blockchain Learning Platform',
                    'description': '''An interactive learning platform for blockchain technology and cryptocurrency development, featuring hands-on tutorials, smart contract examples, and real-world projects.

Learning Modules:
- Blockchain fundamentals
- Smart contract development
- DeFi protocols
- NFT creation and trading
- Cryptocurrency economics
- Security best practices
- Real-world case studies

This platform will make blockchain technology accessible to everyone. Your donation will help create more interactive content, add new programming languages, and develop mobile apps for learning on-the-go.''',
                    'short_description': 'Interactive platform for learning blockchain development and cryptocurrency technology.',
                    'goal_amount': 4000.0,
                    'current_amount': 850.0,
                    'image_url': 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800&h=400&fit=crop',
                    'github_url': 'https://github.com/lusansapkota/blockchain-learning',
                    'is_active': True,
                    'is_featured': False
                }
            ]
            
            # Create donation projects
            created_projects = []
            for project_data in projects_data:
                # Check if project already exists
                existing = DonationProject.query.filter_by(title=project_data['title']).first()
                if not existing:
                    project = DonationProject(**project_data)
                    db.session.add(project)
                    created_projects.append(project)
                    print(f"Created donation project: {project_data['title']}")
                else:
                    created_projects.append(existing)
                    print(f"Project already exists: {project_data['title']}")
            
            db.session.commit()
            
            # Sample donations
            sample_donors = [
                {'name': 'Alex Johnson', 'email': 'alex.johnson@example.com'},
                {'name': 'Sarah Chen', 'email': 'sarah.chen@example.com'},
                {'name': 'Michael Brown', 'email': 'michael.brown@example.com'},
                {'name': 'Emily Davis', 'email': 'emily.davis@example.com'},
                {'name': 'David Wilson', 'email': 'david.wilson@example.com'},
                {'name': 'Lisa Garcia', 'email': 'lisa.garcia@example.com'},
                {'name': 'Anonymous', 'email': 'anonymous@example.com'},
                {'name': 'John Smith', 'email': 'john.smith@example.com'},
                {'name': 'Maria Rodriguez', 'email': 'maria.rodriguez@example.com'},
                {'name': 'Robert Taylor', 'email': 'robert.taylor@example.com'}
            ]
            
            sample_messages = [
                "Great work! Keep it up!",
                "This project will be very useful for the community.",
                "Thanks for building amazing open source tools.",
                "Love the idea, excited to see the progress!",
                "Supporting innovation in tech!",
                "Hope this helps you reach your goal.",
                "Amazing project, well done!",
                "This will help so many developers.",
                "Keep building awesome things!",
                ""  # Empty message
            ]
            
            # Create sample donations
            for project in created_projects:
                # Number of donations for this project (more for featured projects)
                num_donations = random.randint(5, 15) if project.is_featured else random.randint(2, 8)
                
                for i in range(num_donations):
                    donor = random.choice(sample_donors)
                    amount = random.choice([10, 25, 50, 100, 150, 200, 250, 500])
                    message = random.choice(sample_messages)
                    is_anonymous = random.choice([True, False]) if donor['name'] != 'Anonymous' else True
                    
                    # Random date within last 6 months
                    days_ago = random.randint(1, 180)
                    created_date = datetime.utcnow() - timedelta(days=days_ago)
                    
                    # Check if donation already exists
                    existing_donation = Donation.query.filter_by(
                        project_id=project.id,
                        donor_email=donor['email'],
                        amount=amount
                    ).first()
                    
                    if not existing_donation:
                        donation = Donation(
                            project_id=project.id,
                            donor_name=donor['name'],
                            donor_email=donor['email'],
                            amount=amount,
                            message=message if message else None,
                            is_anonymous=is_anonymous,
                            payment_method='paypal',
                            status='completed',
                            created_at=created_date
                        )
                        db.session.add(donation)
            
            db.session.commit()
            
            # Sample newsletter subscribers
            sample_subscribers = [
                {'email': 'dev.enthusiast@example.com', 'name': 'Dev Enthusiast', 'interests': 'Web Development, AI, Mobile Apps'},
                {'email': 'tech.lover@example.com', 'name': 'Tech Lover', 'interests': 'Blockchain, Machine Learning'},
                {'email': 'coding.ninja@example.com', 'name': 'Coding Ninja', 'interests': 'Full Stack Development, DevOps'},
                {'email': 'startup.founder@example.com', 'name': 'Startup Founder', 'interests': 'Entrepreneurship, Product Development'},
                {'email': 'open.source@example.com', 'name': 'Open Source Advocate', 'interests': 'Open Source, Community Building'},
                {'email': 'frontend.dev@example.com', 'name': 'Frontend Developer', 'interests': 'React, Vue.js, UI/UX'},
                {'email': 'backend.dev@example.com', 'name': 'Backend Developer', 'interests': 'Node.js, Python, Database Design'},
                {'email': 'mobile.dev@example.com', 'name': 'Mobile Developer', 'interests': 'iOS Development, Android, Flutter'},
                {'email': 'data.scientist@example.com', 'name': 'Data Scientist', 'interests': 'Data Science, Analytics, AI'},
                {'email': 'product.manager@example.com', 'name': 'Product Manager', 'interests': 'Product Strategy, User Research'}
            ]
            
            for subscriber_data in sample_subscribers:
                existing = NewsletterSubscriber.query.filter_by(email=subscriber_data['email']).first()
                if not existing:
                    subscriber = NewsletterSubscriber(
                        email=subscriber_data['email'],
                        name=subscriber_data['name'],
                        interests=subscriber_data['interests'],
                        is_active=True,
                        subscribed_at=datetime.utcnow() - timedelta(days=random.randint(1, 90))
                    )
                    db.session.add(subscriber)
                    print(f"Created newsletter subscriber: {subscriber_data['email']}")
            
            db.session.commit()
            
            print("\n✅ Sample donation data populated successfully!")
            print(f"📊 Created {len(created_projects)} donation projects")
            print(f"💰 Created sample donations")
            print(f"📧 Created sample newsletter subscribers")
            
            # Display summary
            total_projects = DonationProject.query.count()
            total_donations = Donation.query.count()
            total_raised = db.session.query(db.func.sum(Donation.amount)).filter_by(status='completed').scalar() or 0
            total_subscribers = NewsletterSubscriber.query.filter_by(is_active=True).count()
            
            print(f"\n📈 Current Statistics:")
            print(f"   Projects: {total_projects}")
            print(f"   Donations: {total_donations}")
            print(f"   Total Raised: ${total_raised:.2f}")
            print(f"   Newsletter Subscribers: {total_subscribers}")
            
        except Exception as e:
            print(f"❌ Error populating data: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == '__main__':
    print("🚀 Populating sample donation data...")
    success = populate_donation_data()
    if success:
        print("\n🎉 All done! You can now test the donation system.")
        print("👉 Visit the admin panel to manage donations and projects.")
        print("👉 Visit the donation page to see the projects and make test donations.")
    else:
        print("\n❌ Failed to populate data. Check the error messages above.")

#!/usr/bin/env python3
"""
Script to populate sample donation projects for testing
"""
from app import app, db
from models import DonationProject, Donation
from datetime import datetime

def create_sample_projects():
    """Create sample donation projects"""
    
    # Check if projects already exist
    if DonationProject.query.first():
        print("Sample projects already exist!")
        return
    
    projects_data = [
        {
            'title': 'Open Source Portfolio Platform',
            'description': '''
            <p>A comprehensive, modern portfolio platform built with Flask, featuring multiple subdomains for different functionalities including wiki, git repository browser, and donation management.</p>
            
            <h4>Key Features:</h4>
            <ul>
                <li>Multi-subdomain architecture (wiki.domain.com, git.domain.com, donation.domain.com)</li>
                <li>Responsive design with modern UI/UX</li>
                <li>Database-driven content management</li>
                <li>Email notification system</li>
                <li>Newsletter subscription management</li>
                <li>Admin panel for content management</li>
            </ul>
            
            <h4>Technologies Used:</h4>
            <p>Flask, SQLAlchemy, Bootstrap, JavaScript, HTML5/CSS3, SQLite/PostgreSQL</p>
            
            <h4>Why Support This Project?</h4>
            <p>This platform will be open-sourced to help other developers create their own professional portfolios. Your support helps maintain the servers, add new features, and create comprehensive documentation and tutorials.</p>
            ''',
            'short_description': 'A modern, multi-subdomain portfolio platform with wiki, git browser, and donation management.',
            'goal_amount': 2000.0,
            'current_amount': 450.0,
            'image_url': '/static/assets/images/portfolio/portfolio-platform.jpg',
            'github_url': 'https://github.com/Lusan-sapkota/portfolio-platform',
            'demo_url': 'https://lusansapkota.com.np',
            'is_featured': True
        },
        {
            'title': 'AI-Powered Code Review Tool',
            'description': '''
            <p>An intelligent code review tool that uses machine learning to automatically identify potential issues, suggest improvements, and enforce coding standards.</p>
            
            <h4>Features in Development:</h4>
            <ul>
                <li>Automated code quality analysis</li>
                <li>Smart refactoring suggestions</li>
                <li>Security vulnerability detection</li>
                <li>Performance optimization recommendations</li>
                <li>Integration with popular Git platforms</li>
                <li>Team collaboration features</li>
            </ul>
            
            <h4>Target Languages:</h4>
            <p>Python, JavaScript, TypeScript, Java, C++, Go</p>
            
            <h4>Impact:</h4>
            <p>This tool will help developers write better code, reduce bugs in production, and learn best practices. It's designed to be especially helpful for junior developers and teams working on large codebases.</p>
            ''',
            'short_description': 'AI-powered tool for automated code review, quality analysis, and developer mentoring.',
            'goal_amount': 5000.0,
            'current_amount': 1200.0,
            'image_url': '/static/assets/images/portfolio/ai-code-review.jpg',
            'github_url': 'https://github.com/Lusan-sapkota/ai-code-review',
            'is_featured': True
        },
        {
            'title': 'Real-time Ambulance Tracking System',
            'description': '''
            <p>A life-saving emergency response system that optimizes ambulance dispatch and provides real-time tracking for hospitals and emergency services.</p>
            
            <h4>Core Features:</h4>
            <ul>
                <li>GPS-based real-time tracking</li>
                <li>Intelligent dispatch algorithm</li>
                <li>Hospital capacity monitoring</li>
                <li>Emergency contact notifications</li>
                <li>Route optimization</li>
                <li>Medical history integration</li>
            </ul>
            
            <h4>Technology Stack:</h4>
            <p>Python/Django, PostgreSQL, Redis, WebSocket, Google Maps API, Mobile Apps (React Native)</p>
            
            <h4>Social Impact:</h4>
            <p>This system can significantly reduce emergency response times, potentially saving thousands of lives. I're working with local hospitals to implement this in Nepal first, then expand to other regions.</p>
            ''',
            'short_description': 'Life-saving emergency response system with real-time tracking and intelligent dispatch.',
            'goal_amount': 3000.0,
            'current_amount': 2100.0,
            'image_url': '/static/assets/images/portfolio/ambulance-tracking.jpg',
            'github_url': 'https://github.com/Lusan-sapkota/ambulance-tracker',
            'demo_url': 'https://demo.ambulancetracker.np',
            'is_featured': True
        },
        {
            'title': 'Educational Resource Platform',
            'description': '''
            <p>A comprehensive educational platform providing free programming tutorials, courses, and resources for students in developing countries.</p>
            
            <h4>Platform Features:</h4>
            <ul>
                <li>Interactive coding exercises</li>
                <li>Video tutorials with subtitles</li>
                <li>Progress tracking and certificates</li>
                <li>Community forums and mentorship</li>
                <li>Mobile-responsive design</li>
                <li>Offline content access</li>
            </ul>
            
            <h4>Course Content:</h4>
            <p>Web Development, Python Programming, Data Science, Mobile App Development, DevOps, and more.</p>
            
            <h4>Mission:</h4>
            <p>To make quality programming education accessible to everyone, regardless of their economic background. Special focus on students in Nepal and other developing countries.</p>
            ''',
            'short_description': 'Free educational platform providing programming courses and resources for developing countries.',
            'goal_amount': 1500.0,
            'current_amount': 890.0,
            'image_url': '/static/assets/images/portfolio/education-platform.jpg',
            'github_url': 'https://github.com/Lusan-sapkota/edu-platform',
            'demo_url': 'https://learn.lusansapkota.com.np'
        },
        {
            'title': 'Open Source Development Tools',
            'description': '''
            <p>A collection of developer productivity tools and utilities designed to streamline the development workflow.</p>
            
            <h4>Tools in Development:</h4>
            <ul>
                <li>Smart commit message generator</li>
                <li>Database schema visualizer</li>
                <li>API documentation generator</li>
                <li>Code snippet manager</li>
                <li>Project template creator</li>
                <li>Development environment setup scripts</li>
            </ul>
            
            <h4>Benefits:</h4>
            <p>These tools will be completely free and open source, helping developers worldwide to be more productive and write better code.</p>
            ''',
            'short_description': 'Collection of open source development tools to improve developer productivity.',
            'goal_amount': 800.0,
            'current_amount': 320.0,
            'image_url': '/static/assets/images/portfolio/dev-tools.jpg',
            'github_url': 'https://github.com/Lusan-sapkota/dev-tools'
        }
    ]
    
    for project_data in projects_data:
        project = DonationProject(**project_data)
        db.session.add(project)
    
    # Add some sample donations
    sample_donations = [
        {
            'project_id': 1,
            'donor_name': 'Sarah Chen',
            'donor_email': 'sarah.chen@example.com',
            'amount': 50.0,
            'message': 'Great work on the portfolio platform! Looking forward to using it.',
            'is_anonymous': False,
            'status': 'completed'
        },
        {
            'project_id': 1,
            'donor_name': 'Anonymous',
            'donor_email': 'anonymous@example.com',
            'amount': 100.0,
            'message': 'Keep up the excellent work!',
            'is_anonymous': True,
            'status': 'completed'
        },
        {
            'project_id': 2,
            'donor_name': 'Dev Team Solutions',
            'donor_email': 'contact@devteam.com',
            'amount': 500.0,
            'message': 'I believe this tool will revolutionize code review. Excited to see it in production!',
            'is_anonymous': False,
            'status': 'completed'
        },
        {
            'project_id': 3,
            'donor_name': 'Dr. Medical Corp',
            'donor_email': 'info@medcorp.com',
            'amount': 1000.0,
            'message': 'This system could save lives. I support this initiative wholeheartedly.',
            'is_anonymous': False,
            'status': 'completed'
        }
    ]
    
    for donation_data in sample_donations:
        donation = Donation(**donation_data)
        db.session.add(donation)
    
    db.session.commit()
    print("Sample donation projects and donations created successfully!")
    print("\nCreated projects:")
    for project in DonationProject.query.all():
        print(f"- {project.title}: ${project.current_amount}/${project.goal_amount}")

if __name__ == '__main__':
    with app.app_context():
        create_sample_projects()

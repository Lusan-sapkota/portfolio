#!/usr/bin/env python3
"""
Populate SEO Settings with comprehensive meta data for all pages
"""
import sys
import os
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from app import app
from database import db
from models import SeoSettings

def populate_seo_data():
    """Populate comprehensive SEO settings for all pages"""
    
    with app.app_context():
        # Base URLs
        base_url = "https://www.lusansapkota.com.np"
        
        seo_pages = [
            {
                'page_name': 'home',
                'title': 'Lusan Sapkota | Full Stack Software Developer & AI/ML Engineer from Nepal',
                'meta_description': 'Full Stack Software Developer & AI/ML Engineer from Nepal specializing in Python, JavaScript, TypeScript, React, Django, Flask, and cutting-edge technologies. Expert in graph algorithms, machine learning, and scalable web applications.',
                'meta_keywords': 'Lusan Sapkota, Full Stack Developer Nepal, Software Developer Nepal, Python Developer, JavaScript Developer, AI ML Engineer Nepal, React Developer, Django Developer, TypeScript Expert, Next.js Developer, Graph Algorithms Expert, Data Analysis, Machine Learning Nepal, Web Development Nepal, Nepali Developer, Tech Professional Nepal, Software Engineer Kathmandu, Portfolio Website, Open Source Developer Nepal',
                'focus_keywords': 'Lusan Sapkota, Full Stack Developer Nepal, AI ML Engineer Nepal, Python JavaScript Developer',
                'og_title': 'Lusan Sapkota | Full Stack Software Developer & AI/ML Engineer from Nepal',
                'og_description': 'Full Stack Software Developer & AI/ML Engineer from Nepal specializing in Python, JavaScript, TypeScript, React, and modern web technologies. Expert in graph algorithms and scalable applications.',
                'og_image': f'{base_url}/static/assets/images/profile.jpg',
                'og_url': f'{base_url}/',
                'og_type': 'profile',
                'twitter_title': 'Lusan Sapkota | Full Stack Developer & AI/ML Engineer',
                'twitter_description': 'Full Stack Software Developer from Nepal specializing in Python, JavaScript, AI/ML, and modern web technologies. Expert in graph algorithms and scalable applications.',
                'twitter_image': f'{base_url}/static/assets/images/profile.jpg',
                'twitter_url': f'{base_url}/',
                'canonical_url': f'{base_url}/',
                'page_priority': 1.0,
                'update_frequency': 'weekly',
                'meta_author': 'Lusan Sapkota',
                'meta_publisher': 'Lusan Sapkota Portfolio'
            },
            {
                'page_name': 'about',
                'title': 'About Lusan Sapkota | Professional Background & Technical Expertise',
                'meta_description': 'Learn about Lusan Sapkota - Full Stack Software Developer and AI/ML Engineer from Nepal. Discover professional background, technical expertise, education, and passion for innovative software solutions.',
                'meta_keywords': 'About Lusan Sapkota, Professional Background, Technical Expertise, Software Developer Nepal, AI ML Engineer Background, Programming Experience, Developer Story, Tech Professional Journey',
                'focus_keywords': 'About Lusan Sapkota, Professional Background, Software Developer Nepal',
                'og_title': 'About Lusan Sapkota | Professional Background & Technical Expertise',
                'og_description': 'Discover the professional journey of Lusan Sapkota - Full Stack Software Developer and AI/ML Engineer from Nepal with expertise in modern technologies.',
                'og_url': f'{base_url}/#about',
                'twitter_title': 'About Lusan Sapkota | Tech Professional from Nepal',
                'twitter_description': 'Professional journey of a Full Stack Software Developer and AI/ML Engineer from Nepal with expertise in modern technologies.',
                'twitter_url': f'{base_url}/#about',
                'canonical_url': f'{base_url}/#about',
                'page_priority': 0.8,
                'update_frequency': 'monthly'
            },
            {
                'page_name': 'projects',
                'title': 'Software Projects Portfolio | Lusan Sapkota\'s Development Work',
                'meta_description': 'Explore Lusan Sapkota\'s software development portfolio featuring innovative Python, JavaScript, AI/ML projects, web applications, and open-source contributions.',
                'meta_keywords': 'Software Projects Portfolio, Python Projects, JavaScript Projects, AI ML Projects, Web Applications, Open Source Projects, Development Portfolio, Programming Projects Nepal',
                'focus_keywords': 'Software Projects Portfolio, Development Work, Programming Projects',
                'og_title': 'Software Projects Portfolio | Innovation & Development',
                'og_description': 'Innovative software development projects featuring Python, JavaScript, AI/ML solutions, and web applications.',
                'og_url': f'{base_url}/#projects',
                'twitter_title': 'Software Projects Portfolio | Development Work',
                'twitter_description': 'Innovative projects featuring Python, JavaScript, AI/ML solutions, and modern web applications.',
                'twitter_url': f'{base_url}/#projects',
                'canonical_url': f'{base_url}/#projects',
                'page_priority': 0.9,
                'update_frequency': 'weekly'
            },
            {
                'page_name': 'skills',
                'title': 'Technical Skills & Expertise | Programming & Development Capabilities',
                'meta_description': 'Comprehensive overview of Lusan Sapkota\'s technical skills including Python, JavaScript, React, Django, AI/ML, cloud technologies, and modern development tools.',
                'meta_keywords': 'Technical Skills, Programming Skills, Python Expertise, JavaScript Skills, React Skills, Django Skills, AI ML Skills, Cloud Technologies, Development Tools',
                'focus_keywords': 'Technical Skills, Programming Expertise, Development Capabilities',
                'og_title': 'Technical Skills & Programming Expertise',
                'og_description': 'Comprehensive technical skills in Python, JavaScript, React, Django, AI/ML, and modern development technologies.',
                'og_url': f'{base_url}/#skills',
                'twitter_title': 'Technical Skills & Programming Expertise',
                'twitter_description': 'Comprehensive skills in Python, JavaScript, React, Django, AI/ML, and modern development technologies.',
                'twitter_url': f'{base_url}/#skills',
                'canonical_url': f'{base_url}/#skills',
                'page_priority': 0.7,
                'update_frequency': 'monthly'
            },
            {
                'page_name': 'contact',
                'title': 'Contact Lusan Sapkota | Software Development Services & Collaboration',
                'meta_description': 'Get in touch with Lusan Sapkota for software development services, project collaboration, technical consulting, or professional opportunities.',
                'meta_keywords': 'Contact Lusan Sapkota, Software Development Services, Project Collaboration, Technical Consulting, Hire Developer Nepal, Programming Services',
                'focus_keywords': 'Contact Lusan Sapkota, Software Development Services, Technical Consulting',
                'og_title': 'Contact Lusan Sapkota | Professional Services',
                'og_description': 'Connect for software development services, project collaboration, and technical consulting opportunities.',
                'og_url': f'{base_url}/#contact',
                'twitter_title': 'Contact Lusan Sapkota | Professional Services',
                'twitter_description': 'Connect for software development services and technical consulting opportunities.',
                'twitter_url': f'{base_url}/#contact',
                'canonical_url': f'{base_url}/#contact',
                'page_priority': 0.6,
                'update_frequency': 'monthly'
            }
        ]
        
        # Add subdomain SEO data
        subdomain_pages = [
            {
                'page_name': 'wiki',
                'title': 'Lusan\'s Wiki | Technical Knowledge Base & Programming Documentation',
                'meta_description': 'Comprehensive technical wiki covering software development, AI/ML, web technologies, programming tutorials, and tech insights by Lusan Sapkota.',
                'meta_keywords': 'Technical Wiki, Programming Documentation, Software Development Guides, AI ML Tutorials, Web Technology Articles, Programming Knowledge Base',
                'focus_keywords': 'Technical Wiki, Programming Documentation, Software Development Guides',
                'og_title': 'Lusan\'s Wiki | Technical Knowledge Base',
                'og_description': 'Comprehensive technical documentation and programming tutorials covering modern software development.',
                'og_url': 'https://wiki.lusansapkota.com.np/',
                'twitter_title': 'Technical Wiki | Programming Documentation',
                'twitter_description': 'Comprehensive technical documentation covering software development and programming.',
                'twitter_url': 'https://wiki.lusansapkota.com.np/',
                'canonical_url': 'https://wiki.lusansapkota.com.np/',
                'page_priority': 0.8,
                'update_frequency': 'weekly'
            },
            {
                'page_name': 'git',
                'title': 'Code Repository | Open Source Projects & Development Portfolio',
                'meta_description': 'Explore Lusan Sapkota\'s open source projects, code repositories, and software development portfolio featuring innovative solutions.',
                'meta_keywords': 'Code Repository, Open Source Projects, GitHub Projects, Software Portfolio, Development Work, Programming Projects',
                'focus_keywords': 'Code Repository, Open Source Projects, Software Portfolio',
                'og_title': 'Code Repository | Open Source Development',
                'og_description': 'Open source projects and code repositories featuring innovative software solutions.',
                'og_url': 'https://git.lusansapkota.com.np/',
                'twitter_title': 'Code Repository | Open Source Projects',
                'twitter_description': 'Open source projects and development work featuring innovative software solutions.',
                'twitter_url': 'https://git.lusansapkota.com.np/',
                'canonical_url': 'https://git.lusansapkota.com.np/',
                'page_priority': 0.8,
                'update_frequency': 'daily'
            },
            {
                'page_name': 'donation',
                'title': 'Support Open Source Innovation | Donation Platform',
                'meta_description': 'Support Lusan Sapkota\'s open source development and innovation. Secure donation platform funding cutting-edge AI/ML research and community resources.',
                'meta_keywords': 'Donation Support, Open Source Funding, Developer Support, Innovation Funding, Software Development Support, Tech Project Funding',
                'focus_keywords': 'Donation Support, Open Source Funding, Developer Support',
                'og_title': 'Support Open Source Innovation',
                'og_description': 'Support cutting-edge software development and AI/ML research through secure donations.',
                'og_url': 'https://donation.lusansapkota.com.np/',
                'twitter_title': 'Support Open Source Innovation',
                'twitter_description': 'Support software development and AI/ML research through secure donations.',
                'twitter_url': 'https://donation.lusansapkota.com.np/',
                'canonical_url': 'https://donation.lusansapkota.com.np/',
                'page_priority': 0.5,
                'update_frequency': 'monthly'
            }
        ]
        
        all_pages = seo_pages + subdomain_pages
        
        for page_data in all_pages:
            # Check if page already exists
            existing_page = SeoSettings.query.filter_by(page_name=page_data['page_name']).first()
            
            if existing_page:
                # Update existing page
                for key, value in page_data.items():
                    if key != 'page_name':
                        setattr(existing_page, key, value)
                print(f"Updated SEO settings for: {page_data['page_name']}")
            else:
                # Create new page
                new_page = SeoSettings(**page_data)
                db.session.add(new_page)
                print(f"Created SEO settings for: {page_data['page_name']}")
        
        # Commit all changes
        db.session.commit()
        print(f"\n✅ Successfully populated SEO settings for {len(all_pages)} pages!")
        
        # Show summary
        print("\n📊 SEO Settings Summary:")
        all_seo = SeoSettings.query.all()
        for seo in all_seo:
            print(f"  • {seo.page_name}: {seo.title[:50]}...")

if __name__ == '__main__':
    try:
        populate_seo_data()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

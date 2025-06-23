#!/usr/bin/env python3
"""
SEO Optimization Script for Lusan Sapkota Portfolio
This script creates optimal SEO data to achieve 100/100 SEO score
"""

from app import app
from models import db, SeoSettings
from datetime import datetime

def create_optimal_seo_data():
    """Create optimized SEO data for homepage"""
    
    with app.app_context():
        # Delete existing SEO data for homepage
        existing_seo = SeoSettings.query.filter_by(page_name='home').first()
        if existing_seo:
            db.session.delete(existing_seo)
            db.session.commit()
        
        # Create optimal SEO data
        optimal_seo = SeoSettings(
            page_name='home',
            
            # Optimal title (50-60 characters for best SEO)
            title='Lusan Sapkota | Expert Full Stack Developer & AI Engineer',
            
            # Optimal meta description (150-160 characters)
            meta_description='Expert Full Stack Developer & AI/ML Engineer from Nepal. Specializing in Python, JavaScript, React, Django. 5+ years experience building scalable web apps.',
            
            # Focused keywords
            meta_keywords='Lusan Sapkota, Full Stack Developer Nepal, Python Developer, AI Engineer, JavaScript Expert, React Developer, Django Developer, Web Development Nepal',
            
            # Open Graph optimization
            og_title='Lusan Sapkota | Expert Full Stack Developer & AI Engineer',
            og_description='Expert Full Stack Developer & AI/ML Engineer from Nepal. Specializing in Python, JavaScript, React, Django. 5+ years experience building scalable applications.',
            og_image='https://www.lusansapkota.com.np/static/assets/images/profile.jpg',
            og_url='https://www.lusansapkota.com.np/',
            og_type='profile',
            
            # Twitter Card optimization
            twitter_title='Lusan Sapkota | Expert Full Stack Developer & AI Engineer',
            twitter_description='Expert Full Stack Developer & AI/ML Engineer from Nepal. Python, JavaScript, React, Django specialist with 5+ years experience.',
            twitter_image='https://www.lusansapkota.com.np/static/assets/images/profile.jpg',
            twitter_url='https://www.lusansapkota.com.np/',
            twitter_card='summary_large_image',
            
            # Technical SEO
            canonical_url='https://www.lusansapkota.com.np/',
            robots='index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1',
            hreflang='en',
            
            # Structured data for rich snippets
            schema_markup='{"@context":"https://schema.org","@type":"Person","name":"Lusan Sapkota","jobTitle":"Full Stack Developer & AI Engineer","url":"https://www.lusansapkota.com.np","sameAs":["https://www.linkedin.com/in/lusan-sapkota-a08194284/","https://github.com/lusansapkota"],"address":{"@type":"PostalAddress","addressCountry":"Nepal","addressLocality":"Kathmandu"},"knowsAbout":["Python","JavaScript","React","Django","AI","Machine Learning","Web Development"],"alumniOf":"University","worksFor":{"@type":"Organization","name":"Freelance"}}',
            
            # Focus keywords for this page
            focus_keywords='Full Stack Developer, AI Engineer, Python Developer, JavaScript Expert, React Developer',
            
            # Author and publisher
            meta_author='Lusan Sapkota',
            meta_publisher='Lusan Sapkota',
            
            # Sitemap settings
            page_priority=1.0,  # Highest priority for homepage
            update_frequency='weekly',
            noindex=False
        )
        
        db.session.add(optimal_seo)
        db.session.commit()
        
        print("✅ Optimal SEO data created successfully!")
        print(f"✅ Title length: {len(optimal_seo.title)} characters (optimal: 50-60)")
        print(f"✅ Description length: {len(optimal_seo.meta_description)} characters (optimal: 150-160)")
        print("✅ All SEO fields optimized for 100/100 score")

if __name__ == '__main__':
    create_optimal_seo_data()

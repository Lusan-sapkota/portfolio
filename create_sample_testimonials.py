#!/usr/bin/env python3

from app import app
from database import db
from models import Testimonial

def create_sample_testimonials():
    with app.app_context():
        try:
            # Check if testimonials already exist
            existing_count = Testimonial.query.count()
            if existing_count > 0:
                print(f'✓ {existing_count} testimonials already exist')
                return True

            # Create sample testimonials with correct field names
            testimonials = [
                {
                    'client_name': 'Sarah Chen',
                    'client_title': 'CTO',
                    'client_company': 'TechFlow Inc.',
                    'testimonial_text': 'Lusan delivered an exceptional e-commerce platform that exceeded our expectations. His attention to detail and technical expertise made our project a huge success. The scalable architecture he designed has been handling our growing traffic flawlessly.',
                    'rating': 5,
                    'is_featured': True,
                    'project_related': 'E-commerce Platform'
                },
                {
                    'client_name': 'Michael Rodriguez',
                    'client_title': 'Product Manager',
                    'client_company': 'DataVision Corp',
                    'testimonial_text': 'Working with Lusan was a fantastic experience. He transformed our complex data requirements into an intuitive analytics dashboard. His ability to understand business needs and translate them into technical solutions is remarkable.',
                    'rating': 5,
                    'is_featured': True,
                    'project_related': 'Analytics Dashboard'
                },
                {
                    'client_name': 'Emma Thompson',
                    'client_title': 'Startup Founder',
                    'client_company': 'HealthTech Solutions',
                    'testimonial_text': 'Lusan built our entire healthcare management system from scratch. His expertise in both frontend and backend development, combined with his understanding of healthcare workflows, made him the perfect developer for our project.',
                    'rating': 5,
                    'is_featured': True,
                    'project_related': 'Healthcare Management System'
                },
                {
                    'client_name': 'James Wilson',
                    'client_title': 'IT Director',
                    'client_company': 'LogiCorp',
                    'testimonial_text': 'The logistics tracking system Lusan developed has revolutionized our operations. Real-time tracking, automated notifications, and comprehensive reporting - everything works seamlessly. Highly recommended!',
                    'rating': 5,
                    'is_featured': True,
                    'project_related': 'Logistics Tracking System'
                },
                {
                    'client_name': 'Dr. Lisa Kumar',
                    'client_title': 'Research Director',
                    'client_company': 'AI Research Lab',
                    'testimonial_text': 'Lusan\'s work on our machine learning pipeline was outstanding. His deep understanding of AI algorithms and ability to implement complex models efficiently saved us months of development time.',
                    'rating': 5,
                    'is_featured': True,
                    'project_related': 'ML Pipeline'
                },
                {
                    'client_name': 'Robert Davis',
                    'client_title': 'Business Owner',
                    'client_company': 'Local Restaurant Chain',
                    'testimonial_text': 'The restaurant management system Lusan created has streamlined our entire operation. From inventory management to customer orders, everything is now automated and efficient. Our revenue has increased by 30% since implementation.',
                    'rating': 5,
                    'is_featured': True,
                    'project_related': 'Restaurant Management System'
                }
            ]

            created_count = 0
            for testimonial_data in testimonials:
                testimonial = Testimonial(**testimonial_data)
                db.session.add(testimonial)
                created_count += 1

            db.session.commit()
            print(f'✓ Created {created_count} sample testimonials')

            # Show created testimonials
            all_testimonials = Testimonial.query.all()
            print(f'✓ Total testimonials in database: {len(all_testimonials)}')
            for t in all_testimonials:
                print(f'  - {t.client_name} ({t.client_company}): {t.rating} stars')

            return True

        except Exception as e:
            print(f'✗ Error creating testimonials: {e}')
            db.session.rollback()
            return False

if __name__ == "__main__":
    if create_sample_testimonials():
        print("\n🎉 Sample testimonials created successfully!")
    else:
        print("\n❌ Failed to create sample testimonials")

# Enhanced Portfolio Configuration

# Subdomain Configuration
SUBDOMAINS = {
    'wiki': {
        'url': 'https://wiki.lusansapkota.com.np',
        'title': 'Knowledge Wiki',
        'description': 'Comprehensive documentation, tutorials, and technical articles covering web development, AI/ML, and cutting-edge technologies.',
        'icon': 'fas fa-book-open',
        'enabled': True
    },
    'git': {
        'url': 'https://git.lusansapkota.com.np',
        'title': 'Code Repository', 
        'description': 'Browse through my open-source projects, code samples, and collaborative development work.',
        'icon': 'fab fa-git-alt',
        'enabled': True
    },
    'donation': {
        'url': 'https://donation.lusansapkota.com.np',
        'title': 'Support Platform',
        'description': 'Support my open-source work and community contributions.',
        'icon': 'fas fa-heart',
        'enabled': True
    },
    'store': {
        'url': 'https://store.lusansapkota.com.np',
        'title': 'Online Store',
        'description': 'Browse and purchase digital products, courses, and exclusive content.',
        'icon': 'fas fa-shopping-cart',
        'enabled': True
    }
}

# Theme Configuration
THEME_CONFIG = {
    'default_theme': 'light',
    'enable_dark_mode': True,
    'enable_auto_theme': True  # Based on system preference
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'enable_lazy_loading': True,
    'enable_preloading': True,
    'enable_compression': True,
    'cache_duration': 86400  # 24 hours
}

# Analytics Configuration
ANALYTICS_CONFIG = {
    'google_analytics_id': 'GTM-XXXX',  # Replace with actual ID
    'enable_performance_tracking': True,
    'enable_error_tracking': True
}

# SEO Configuration
SEO_CONFIG = {
    'site_name': 'Lusan Sapkota Portfolio',
    'default_title': 'Lusan Sapkota | Full Stack Software Developer from Nepal',
    'default_description': 'Full Stack Software Developer specializing in Python, JavaScript, React, Django, Flask, and AI/ML technologies.',
    'author': 'Lusan Sapkota',
    'keywords': ['Full Stack Developer', 'Software Developer', 'Python Developer', 'JavaScript Developer', 'Nepal Developer', 'AI ML Developer'],
    'social_media': {
        'facebook': 'https://web.facebook.com/lusan.sapkota.1',
        'github': 'https://github.com/Lusan-sapkota',
        'twitter': 'https://x.com/LusanSapkota',
        'linkedin': 'https://www.linkedin.com/in/lusan-sapkota-a08194284/',
        'instagram': 'https://www.instagram.com/sapkotalusan/',
        'email': 'sapkotalusan@gmail.com'
    }
}

# Contact Information
CONTACT_INFO = {
    'phone': 'Available upon request',
    'email': 'sapkotalusan@gmail.com',
    'website': 'https://www.lusansapkota.com.np',
    'location': {
        'city': 'Kathmandu',
        'country': 'Nepal',
        'coordinates': {
            'latitude': '27.7172',
            'longitude': '85.3240'
        }
    }
}

# Feature Flags
FEATURES = {
    'subdomain_navigation': True,
    'dark_mode_toggle': True,
    'smooth_scrolling': True,
    'parallax_effects': True,
    'loading_animations': True,
    'responsive_design': True,
    'accessibility_features': True,
    'progressive_web_app': False  # Set to True when PWA features are implemented
}

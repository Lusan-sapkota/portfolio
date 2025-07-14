#!/usr/bin/env python3
"""
Advanced SEO Enhancement Script for Lusan Sapkota Portfolio
Implements comprehensive SEO improvements for perfect scores
"""

import os
import re
import json
from datetime import datetime, timezone
import argparse

class SEOEnhancer:
    def __init__(self, base_path="/home/ubuntu/portfolio"):
        self.base_path = base_path
        
    def create_security_txt(self):
        """Create security.txt file for security policy"""
        security_content = """Contact: sapkotalusan@gmail.com
Expires: 2025-12-31T23:59:59.000Z
Encryption: https://www.lusansapkota.com.np/public-key.txt
Acknowledgments: https://www.lusansapkota.com.np/security-acknowledgments
Policy: https://www.lusansapkota.com.np/security-policy
Hiring: https://www.lusansapkota.com.np/jobs
"""
        
        security_dir = os.path.join(self.base_path, "static/.well-known")
        os.makedirs(security_dir, exist_ok=True)
        
        with open(os.path.join(security_dir, "security.txt"), 'w') as f:
            f.write(security_content)
            
        print("✅ Created security.txt")
        
    def create_humans_txt(self):
        """Create humans.txt file"""
        humans_content = """/* TEAM */
    Developer: Lusan Sapkota
    Contact: sapkotalusan@gmail.com
    Twitter: @LusanSapkota
    Location: Kathmandu, Nepal
    
/* THANKS */
    Thanks to all the open source contributors
    
/* SITE */
    Last update: 2024/12/23
    Language: English
    Doctype: HTML5
    IDE: VS Code
    Components: Python, Flask, JavaScript, Bootstrap
"""
        
        with open(os.path.join(self.base_path, "static/humans.txt"), 'w') as f:
            f.write(humans_content)
            
        print("✅ Created humans.txt")
        
    def enhance_manifest(self):
        """Enhance PWA manifest with additional SEO properties"""
        manifest_path = os.path.join(self.base_path, "static/manifest.json")
        
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                
            # Add missing properties for better SEO
            manifest.update({
                "dir": "ltr",
                "display_override": ["window-controls-overlay", "standalone"],
                "edge_side_panel": {
                    "preferred_width": 320
                },
                "scope": "/",
                "id": "/",
                "orientation": "any",
                "related_applications": [],
                "prefer_related_applications": False,
                "iarc_rating_id": "",
                "protocol_handlers": [
                    {
                        "protocol": "web+portfolio",
                        "url": "/?action=%s"
                    }
                ]
            })
            
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
                
            print("✅ Enhanced PWA manifest")
            
        except FileNotFoundError:
            print("❌ Manifest file not found")
            
    def create_browserconfig(self):
        """Create browserconfig.xml for Windows tiles"""
        browserconfig_content = """<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
    <msapplication>
        <tile>
            <square70x70logo src="/static/assets/logo/mstile-70x70.png"/>
            <square150x150logo src="/static/assets/logo/mstile-150x150.png"/>
            <square310x310logo src="/static/assets/logo/mstile-310x310.png"/>
            <wide310x150logo src="/static/assets/logo/mstile-310x150.png"/>
            <TileColor>#f39c12</TileColor>
        </tile>
    </msapplication>
</browserconfig>"""
        
        with open(os.path.join(self.base_path, "static/assets/logo/browserconfig.xml"), 'w') as f:
            f.write(browserconfig_content)
            
        print("✅ Created browserconfig.xml")
        
    def optimize_robots_txt(self):
        """Further optimize robots.txt"""
        robots_content = """# Robots.txt for Lusan Sapkota Portfolio
# https://www.lusansapkota.com.np/robots.txt

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/private/
Disallow: /.git/
Disallow: /__pycache__/
Disallow: /migrations/
Disallow: /venv/
Disallow: /.env
Disallow: /config.py
Disallow: /requirements.txt
Disallow: /test*
Disallow: /debug/
Disallow: /search?
Disallow: /tmp/
Disallow: /cache/

# Allow important resources
Allow: /static/
Allow: /assets/
Allow: /*.css
Allow: /*.js
Allow: /*.jpg
Allow: /*.png
Allow: /*.gif
Allow: /*.svg
Allow: /*.webp
Allow: /*.ico
Allow: /*.pdf
Allow: /*.txt
Allow: /manifest.json
Allow: /sw.js

# Crawl delay for respectful crawling
Crawl-delay: 1

# Sitemaps
Sitemap: https://www.lusansapkota.com.np/static/sitemap.xml
Sitemap: https://wiki.lusansapkota.com.np/sitemap.xml
Sitemap: https://git.lusansapkota.com.np/sitemap.xml
Sitemap: https://donation.lusansapkota.com.np/sitemap.xml

# Google specific directives
User-agent: Googlebot
Allow: /
Crawl-delay: 1

# Bing specific directives
User-agent: Bingbot
Allow: /
Crawl-delay: 1

# Social Media Crawlers
User-agent: facebookexternalhit
Allow: /

User-agent: Twitterbot
Allow: /

User-agent: LinkedInBot
Allow: /

User-agent: WhatsApp
Allow: /

User-agent: TelegramBot
Allow: /

# AI/ML Crawlers
User-agent: GPTBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: Claude-Web
Disallow: /

# Archive crawlers
User-agent: ia_archiver
Allow: /

User-agent: archive.org_bot
Allow: /"""

        with open(os.path.join(self.base_path, "static/robots.txt"), 'w') as f:
            f.write(robots_content)
            
        print("✅ Optimized robots.txt")
        
    def create_ads_txt(self):
        """Create ads.txt for advertising transparency"""
        ads_content = """# ads.txt file for lusansapkota.com.np
# This file is used to authorize digital advertising inventory
# Currently no advertising partnerships active
# Contact: sapkotalusan@gmail.com for advertising inquiries
"""
        
        with open(os.path.join(self.base_path, "static/ads.txt"), 'w') as f:
            f.write(ads_content)
            
        print("✅ Created ads.txt")
        
    def create_advanced_sitemap(self):
        """Create an advanced sitemap with more detailed structure"""
        from generate_sitemap import create_sitemap
        
        # Create main sitemap
        create_sitemap()
        
        # Create sitemap index
        sitemap_index = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap>
        <loc>https://www.lusansapkota.com.np/static/sitemap.xml</loc>
        <lastmod>{}</lastmod>
    </sitemap>
    <sitemap>
        <loc>https://wiki.lusansapkota.com.np/sitemap.xml</loc>
        <lastmod>{}</lastmod>
    </sitemap>
    <sitemap>
        <loc>https://git.lusansapkota.com.np/sitemap.xml</loc>
        <lastmod>{}</lastmod>
    </sitemap>
    <sitemap>
        <loc>https://donation.lusansapkota.com.np/sitemap.xml</loc>
        <lastmod>{}</lastmod>
    </sitemap>
</sitemapindex>""".format(*[datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')] * 4)

        with open(os.path.join(self.base_path, "static/sitemap-index.xml"), 'w') as f:
            f.write(sitemap_index)
            
        print("✅ Created advanced sitemap structure")
        
    def create_seo_meta_template(self):
        """Create a comprehensive SEO meta template"""
        seo_template = """<!-- Advanced SEO Meta Tags Template -->
<!-- Generated by SEO Enhancement Script -->

<!-- Core Meta Tags -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<meta http-equiv="X-UA-Compatible" content="IE=edge">

<!-- SEO Meta Tags -->
<title>{{ page_title }}</title>
<meta name="description" content="{{ page_description }}">
<meta name="keywords" content="{{ page_keywords }}">
<meta name="author" content="Lusan Sapkota">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">

<!-- Canonical URL -->
<link rel="canonical" href="{{ canonical_url }}">

<!-- Open Graph Meta Tags -->
<meta property="og:type" content="{{ og_type }}">
<meta property="og:title" content="{{ og_title }}">
<meta property="og:description" content="{{ og_description }}">
<meta property="og:image" content="{{ og_image }}">
<meta property="og:url" content="{{ og_url }}">
<meta property="og:site_name" content="Lusan Sapkota Portfolio">
<meta property="og:locale" content="en_US">

<!-- Twitter Meta Tags -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@LusanSapkota">
<meta name="twitter:creator" content="@LusanSapkota">
<meta name="twitter:title" content="{{ twitter_title }}">
<meta name="twitter:description" content="{{ twitter_description }}">
<meta name="twitter:image" content="{{ twitter_image }}">

<!-- Additional SEO Meta Tags -->
<meta name="theme-color" content="#f39c12">
<meta name="msapplication-TileColor" content="#f39c12">
<meta name="application-name" content="Lusan Sapkota Portfolio">
<meta name="apple-mobile-web-app-title" content="Lusan Portfolio">

<!-- Performance and Security -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:; font-src 'self' https:; connect-src 'self' https:;">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="DENY">
<meta http-equiv="X-XSS-Protection" content="1; mode=block">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">

<!-- Preconnect for Performance -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdnjs.cloudflare.com">
<link rel="dns-prefetch" href="https://github.com">"""

        seo_dir = os.path.join(self.base_path, "templates/seo")
        os.makedirs(seo_dir, exist_ok=True)
        
        with open(os.path.join(seo_dir, "meta-template.html"), 'w') as f:
            f.write(seo_template)
            
        print("✅ Created SEO meta template")
        
    def run_all_enhancements(self):
        """Run all SEO enhancements"""
        print("🚀 Starting advanced SEO enhancements...\n")
        
        self.create_security_txt()
        self.create_humans_txt()
        self.enhance_manifest()
        self.create_browserconfig()
        self.optimize_robots_txt()
        self.create_ads_txt()
        self.create_advanced_sitemap()
        self.create_seo_meta_template()
        
        print("\n✅ All SEO enhancements completed!")
        print("\n📈 Additional recommendations:")
        print("1. Add Google Analytics 4 and Google Search Console")
        print("2. Implement structured data for events and reviews")
        print("3. Add breadcrumb navigation")
        print("4. Optimize Core Web Vitals (LCP, FID, CLS)")
        print("5. Implement AMP for mobile performance")
        print("6. Add FAQ schema markup")
        print("7. Consider implementing WebP images")
        print("8. Add rel='noopener' to external links")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Advanced SEO Enhancement Tool')
    parser.add_argument('--path', default='/home/ubuntu/portfolio', help='Path to portfolio directory')
    
    args = parser.parse_args()
    
    enhancer = SEOEnhancer(args.path)
    enhancer.run_all_enhancements()

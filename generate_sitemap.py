#!/usr/bin/env python3
"""
Dynamic Sitemap Generator for Lusan Sapkota Portfolio
Generates XML sitemaps with proper priority and frequency settings
"""

import os
from datetime import datetime, timezone
from urllib.parse import urljoin
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import argparse

def create_sitemap(base_url="https://www.lusansapkota.com.np", output_file="static/sitemap.xml"):
    """Generate a comprehensive sitemap for the portfolio website"""
    
    # Create the root element
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    urlset.set('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
    
    # Current timestamp
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    # Define pages with their SEO properties
    pages = [
        {
            'url': '/',
            'priority': '1.0',
            'changefreq': 'weekly',
            'lastmod': now
        },
        {
            'url': '/#about',
            'priority': '0.9',
            'changefreq': 'monthly',
            'lastmod': now
        },
        {
            'url': '/#skills',
            'priority': '0.8',
            'changefreq': 'monthly',
            'lastmod': now
        },
        {
            'url': '/#portfolio',
            'priority': '0.9',
            'changefreq': 'weekly',
            'lastmod': now
        },
        {
            'url': '/#services',
            'priority': '0.8',
            'changefreq': 'monthly',
            'lastmod': now
        },
        {
            'url': '/#testimonials',
            'priority': '0.7',
            'changefreq': 'monthly',
            'lastmod': now
        },
        {
            'url': '/#contact',
            'priority': '0.8',
            'changefreq': 'monthly',
            'lastmod': now
        },
        {
            'url': '/privacy',
            'priority': '0.3',
            'changefreq': 'yearly',
            'lastmod': now
        }
    ]
    
    # Add subdomain pages
    subdomains = [
        {
            'url': 'https://wiki.lusansapkota.com.np/',
            'priority': '0.7',
            'changefreq': 'weekly',
            'lastmod': now
        },
        {
            'url': 'https://git.lusansapkota.com.np/',
            'priority': '0.6',
            'changefreq': 'weekly',
            'lastmod': now
        },
        {
            'url': 'https://donation.lusansapkota.com.np/',
            'priority': '0.5',
            'changefreq': 'monthly',
            'lastmod': now
        }
    ]
    
    # Create URL elements for main pages
    for page in pages:
        url_elem = SubElement(urlset, 'url')
        
        loc = SubElement(url_elem, 'loc')
        loc.text = urljoin(base_url, page['url']) if not page['url'].startswith('http') else page['url']
        
        lastmod = SubElement(url_elem, 'lastmod')
        lastmod.text = page['lastmod']
        
        changefreq = SubElement(url_elem, 'changefreq')
        changefreq.text = page['changefreq']
        
        priority = SubElement(url_elem, 'priority')
        priority.text = page['priority']
    
    # Add subdomain URLs
    for page in subdomains:
        url_elem = SubElement(urlset, 'url')
        
        loc = SubElement(url_elem, 'loc')
        loc.text = page['url']
        
        lastmod = SubElement(url_elem, 'lastmod')
        lastmod.text = page['lastmod']
        
        changefreq = SubElement(url_elem, 'changefreq')
        changefreq.text = page['changefreq']
        
        priority = SubElement(url_elem, 'priority')
        priority.text = page['priority']
    
    # Format the XML
    rough_string = tostring(urlset, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # Remove extra blank lines
    pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
    
    # Write to file
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"Sitemap generated successfully: {output_file}")
    return output_file

def create_robots_txt(base_url="https://www.lusansapkota.com.np", output_file="static/robots.txt"):
    """Update robots.txt with sitemap reference"""
    
    robots_content = f"""User-agent: *
Allow: /

# Prioritize important pages
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

# Block admin and sensitive areas
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

# Block search and temporary pages
Disallow: /search?
Disallow: /tmp/
Disallow: /cache/

# Crawl delay for respectful crawling
Crawl-delay: 1

# Sitemaps
Sitemap: {base_url}/static/sitemap.xml
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
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(robots_content)
    
    print(f"Robots.txt updated successfully: {output_file}")
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate SEO files for portfolio')
    parser.add_argument('--base-url', default='https://www.lusansapkota.com.np', help='Base URL for the website')
    parser.add_argument('--sitemap-output', default='static/sitemap.xml', help='Output path for sitemap')
    parser.add_argument('--robots-output', default='static/robots.txt', help='Output path for robots.txt')
    
    args = parser.parse_args()
    
    # Generate sitemap and robots.txt
    create_sitemap(args.base_url, args.sitemap_output)
    create_robots_txt(args.base_url, args.robots_output)
    
    print("SEO files generated successfully!")

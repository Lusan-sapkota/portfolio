#!/usr/bin/env python3
"""
Quick test script to verify SEO elements in subdomain templates
"""

import os
import re
from pathlib import Path

def check_template_seo(template_path):
    """Check if a template has comprehensive SEO implementation"""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {
        'open_graph': len(re.findall(r'<meta property="og:', content)),
        'twitter_cards': len(re.findall(r'<meta.*twitter:', content)),
        'structured_data': len(re.findall(r'@type', content)),
        'analytics_ga': 'google_analytics_id' in content,
        'analytics_gtm': 'google_tag_manager_id' in content,
        'analytics_fb': 'facebook_pixel_id' in content,
        'analytics_linkedin': 'linkedin_insight_tag' in content,
        'pwa_manifest': 'manifest.json' in content,
        'service_worker': 'serviceWorker' in content,
        'performance_monitoring': 'web-vitals' in content,
        'canonical_url': 'rel="canonical"' in content,
        'meta_description': 'meta_description' in content,
        'meta_keywords': 'meta_keywords' in content,
        'robots_meta': 'robots' in content.lower(),
        'schema_blocks': content.count('application/ld+json'),
        'theme_color': 'theme-color' in content,
        'favicon_tags': content.count('rel="icon"') + content.count('apple-touch-icon')
    }
    
    return results

def main():
    print("🔍 Subdomain SEO Verification")
    print("=" * 50)
    
    templates = [
        ('Donation', '/home/lusan/Documents/portfolio/donation/templates/base.html'),
        ('Wiki', '/home/lusan/Documents/portfolio/wiki/templates/wiki/base.html'),
        ('Git', '/home/lusan/Documents/portfolio/git/templates/git/base.html'),
        ('Main Site', '/home/lusan/Documents/portfolio/templates/index.html')
    ]
    
    for name, path in templates:
        if os.path.exists(path):
            print(f"\n📄 {name} Template Analysis:")
            print("-" * 30)
            
            results = check_template_seo(path)
            
            # Essential SEO Elements
            print(f"🏷️  Open Graph tags: {results['open_graph']}")
            print(f"🐦 Twitter Card tags: {results['twitter_cards']}")
            print(f"📊 Schema.org blocks: {results['schema_blocks']}")
            print(f"🔗 Canonical URL: {'✅' if results['canonical_url'] else '❌'}")
            print(f"📝 Meta description: {'✅' if results['meta_description'] else '❌'}")
            print(f"🏷️  Meta keywords: {'✅' if results['meta_keywords'] else '❌'}")
            print(f"🤖 Robots meta: {'✅' if results['robots_meta'] else '❌'}")
            
            # Analytics Integration
            print(f"\n📈 Analytics & Tracking:")
            print(f"   Google Analytics: {'✅' if results['analytics_ga'] else '❌'}")
            print(f"   Google Tag Manager: {'✅' if results['analytics_gtm'] else '❌'}")
            print(f"   Facebook Pixel: {'✅' if results['analytics_fb'] else '❌'}")
            print(f"   LinkedIn Insight: {'✅' if results['analytics_linkedin'] else '❌'}")
            
            # PWA & Performance
            print(f"\n🚀 PWA & Performance:")
            print(f"   PWA Manifest: {'✅' if results['pwa_manifest'] else '❌'}")
            print(f"   Service Worker: {'✅' if results['service_worker'] else '❌'}")
            print(f"   Performance Monitoring: {'✅' if results['performance_monitoring'] else '❌'}")
            print(f"   Theme Color: {'✅' if results['theme_color'] else '❌'}")
            print(f"   Favicon Tags: {results['favicon_tags']}")
            
            # Calculate SEO score for this template
            total_checks = 12
            passed_checks = sum([
                results['canonical_url'],
                results['meta_description'],
                results['meta_keywords'],
                results['robots_meta'],
                results['analytics_ga'],
                results['pwa_manifest'],
                results['service_worker'],
                results['performance_monitoring'],
                results['theme_color'],
                results['open_graph'] > 5,
                results['twitter_cards'] > 5,
                results['schema_blocks'] > 0
            ])
            
            score = (passed_checks / total_checks) * 100
            print(f"\n📊 SEO Score: {score:.1f}/100")
            
            if score >= 90:
                print("🏆 EXCELLENT! Comprehensive SEO implementation")
            elif score >= 75:
                print("👍 GOOD! Strong SEO foundation")
            elif score >= 50:
                print("⚠️  FAIR! Some SEO improvements needed")
            else:
                print("❌ POOR! Major SEO work required")
        
        else:
            print(f"\n❌ {name} template not found: {path}")
    
    print("\n" + "=" * 50)
    print("🎯 Summary: All subdomain templates should have comprehensive SEO")
    print("   including analytics, PWA features, and rich meta tags!")

if __name__ == "__main__":
    main()

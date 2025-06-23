#!/usr/bin/env python3
"""
SEO Audit Script - Verify all SEO implementations
"""
import sys
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import json

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

def audit_seo_implementation(base_url="http://127.0.0.1:5000"):
    """Comprehensive SEO audit"""
    
    print("🔍 Starting SEO Audit for Lusan Sapkota Portfolio")
    print("=" * 60)
    
    audit_results = {
        "passed": 0,
        "failed": 0,
        "warnings": 0,
        "details": []
    }
    
    try:
        # Test 1: Homepage accessibility
        print("\n1. Testing Homepage Accessibility...")
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Homepage accessible")
            audit_results["passed"] += 1
        else:
            print(f"❌ Homepage not accessible: {response.status_code}")
            audit_results["failed"] += 1
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Test 2: Title tag
        print("\n2. Testing Title Tag...")
        title = soup.find('title')
        if title and len(title.text) > 30 and len(title.text) < 60:
            print(f"✅ Title tag optimal: {title.text[:50]}...")
            audit_results["passed"] += 1
        elif title:
            print(f"⚠️  Title tag exists but length suboptimal: {len(title.text)} chars")
            audit_results["warnings"] += 1
        else:
            print("❌ No title tag found")
            audit_results["failed"] += 1
            
        # Test 3: Meta description
        print("\n3. Testing Meta Description...")
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and len(meta_desc.get('content', '')) > 120:
            print(f"✅ Meta description optimal: {meta_desc.get('content')[:50]}...")
            audit_results["passed"] += 1
        else:
            print("❌ Meta description missing or too short")
            audit_results["failed"] += 1
            
        # Test 4: Open Graph tags
        print("\n4. Testing Open Graph Tags...")
        og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        required_og = ['og:title', 'og:description', 'og:image', 'og:url']
        found_og = [tag.get('property') for tag in og_tags]
        
        if all(req in found_og for req in required_og):
            print(f"✅ All required OG tags present: {len(og_tags)} total")
            audit_results["passed"] += 1
        else:
            missing = [req for req in required_og if req not in found_og]
            print(f"❌ Missing OG tags: {missing}")
            audit_results["failed"] += 1
            
        # Test 5: Twitter Card tags
        print("\n5. Testing Twitter Card Tags...")
        twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
        if len(twitter_tags) >= 4:
            print(f"✅ Twitter Card tags present: {len(twitter_tags)} tags")
            audit_results["passed"] += 1
        else:
            print(f"⚠️  Limited Twitter Card tags: {len(twitter_tags)} tags")
            audit_results["warnings"] += 1
            
        # Test 6: Structured Data
        print("\n6. Testing Structured Data...")
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        if len(json_ld_scripts) >= 3:
            print(f"✅ Rich structured data present: {len(json_ld_scripts)} schemas")
            audit_results["passed"] += 1
            
            # Validate JSON-LD
            valid_schemas = 0
            for script in json_ld_scripts:
                try:
                    json.loads(script.string)
                    valid_schemas += 1
                except:
                    pass
            print(f"   Valid schemas: {valid_schemas}/{len(json_ld_scripts)}")
        else:
            print(f"❌ Insufficient structured data: {len(json_ld_scripts)} schemas")
            audit_results["failed"] += 1
            
        # Test 7: Canonical URL
        print("\n7. Testing Canonical URL...")
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            print(f"✅ Canonical URL present: {canonical.get('href')}")
            audit_results["passed"] += 1
        else:
            print("❌ No canonical URL found")
            audit_results["failed"] += 1
            
        # Test 8: Robots meta tag
        print("\n8. Testing Robots Meta Tag...")
        robots = soup.find('meta', attrs={'name': 'robots'})
        if robots and 'index' in robots.get('content', ''):
            print(f"✅ Robots tag allows indexing: {robots.get('content')}")
            audit_results["passed"] += 1
        else:
            print("⚠️  Robots tag missing or restrictive")
            audit_results["warnings"] += 1
            
        # Test 9: Sitemap.xml
        print("\n9. Testing Sitemap...")
        try:
            sitemap_response = requests.get(f"{base_url}/sitemap.xml", timeout=5)
            if sitemap_response.status_code == 200 and 'xml' in sitemap_response.headers.get('content-type', ''):
                print("✅ Sitemap.xml accessible and valid")
                audit_results["passed"] += 1
            else:
                print(f"❌ Sitemap issues: {sitemap_response.status_code}")
                audit_results["failed"] += 1
        except:
            print("❌ Sitemap not accessible")
            audit_results["failed"] += 1
            
        # Test 10: Robots.txt
        print("\n10. Testing Robots.txt...")
        try:
            robots_response = requests.get(f"{base_url}/robots.txt", timeout=5)
            if robots_response.status_code == 200:
                print("✅ Robots.txt accessible")
                audit_results["passed"] += 1
                if 'Sitemap:' in robots_response.text:
                    print("   ✅ Sitemap referenced in robots.txt")
                else:
                    print("   ⚠️  No sitemap reference in robots.txt")
            else:
                print(f"❌ Robots.txt not accessible: {robots_response.status_code}")
                audit_results["failed"] += 1
        except:
            print("❌ Robots.txt not accessible")
            audit_results["failed"] += 1
            
        # Test 11: PWA Manifest
        print("\n11. Testing PWA Manifest...")
        manifest_link = soup.find('link', rel='manifest')
        if manifest_link:
            try:
                manifest_response = requests.get(f"{base_url}/manifest.json", timeout=5)
                if manifest_response.status_code == 200:
                    manifest_data = manifest_response.json()
                    if 'name' in manifest_data and 'icons' in manifest_data:
                        print("✅ PWA Manifest valid and complete")
                        audit_results["passed"] += 1
                    else:
                        print("⚠️  PWA Manifest incomplete")
                        audit_results["warnings"] += 1
                else:
                    print("❌ PWA Manifest not accessible")
                    audit_results["failed"] += 1
            except:
                print("❌ PWA Manifest invalid or not accessible")
                audit_results["failed"] += 1
        else:
            print("❌ No PWA Manifest link found")
            audit_results["failed"] += 1
            
        # Test 12: Page Speed Indicators
        print("\n12. Testing Performance Indicators...")
        preconnect_links = soup.find_all('link', rel='preconnect')
        dns_prefetch_links = soup.find_all('link', rel='dns-prefetch')
        
        if len(preconnect_links) + len(dns_prefetch_links) >= 4:
            print(f"✅ Good performance optimization: {len(preconnect_links)} preconnect, {len(dns_prefetch_links)} dns-prefetch")
            audit_results["passed"] += 1
        else:
            print(f"⚠️  Limited performance optimization: {len(preconnect_links)} preconnect, {len(dns_prefetch_links)} dns-prefetch")
            audit_results["warnings"] += 1
            
        # Test 13: Mobile Optimization
        print("\n13. Testing Mobile Optimization...")
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport and 'width=device-width' in viewport.get('content', ''):
            print("✅ Mobile viewport configured")
            audit_results["passed"] += 1
        else:
            print("❌ Mobile viewport missing or misconfigured")
            audit_results["failed"] += 1
            
        # Test 14: Schema.org Validation
        print("\n14. Testing Schema.org Implementation...")
        person_schema = False
        website_schema = False
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    if data.get('@type') == 'Person' or (data.get('@graph') and any(item.get('@type') == 'Person' for item in data.get('@graph', []))):
                        person_schema = True
                    if data.get('@type') == 'WebSite' or (data.get('@graph') and any(item.get('@type') == 'WebSite' for item in data.get('@graph', []))):
                        website_schema = True
            except:
                continue
                
        if person_schema and website_schema:
            print("✅ Rich Person and Website schemas implemented")
            audit_results["passed"] += 1
        else:
            print(f"⚠️  Missing schemas - Person: {person_schema}, Website: {website_schema}")
            audit_results["warnings"] += 1
            
    except Exception as e:
        print(f"❌ Audit failed with error: {e}")
        audit_results["failed"] += 1
        
    # Final Score
    print("\n" + "=" * 60)
    print("📊 SEO AUDIT RESULTS")
    print("=" * 60)
    
    total_tests = audit_results["passed"] + audit_results["failed"] + audit_results["warnings"]
    score = (audit_results["passed"] / total_tests * 100) if total_tests > 0 else 0
    
    print(f"✅ Passed: {audit_results['passed']}")
    print(f"❌ Failed: {audit_results['failed']}")
    print(f"⚠️  Warnings: {audit_results['warnings']}")
    print(f"📈 SEO Score: {score:.1f}/100")
    
    if score >= 90:
        print("🎉 EXCELLENT! Your SEO implementation is outstanding!")
    elif score >= 80:
        print("👍 GREAT! Your SEO implementation is very good!")
    elif score >= 70:
        print("👌 GOOD! Your SEO implementation is solid with room for improvement!")
    else:
        print("⚠️  NEEDS WORK! Several SEO issues need attention!")
        
    print("\n🚀 SEO ENHANCEMENT RECOMMENDATIONS:")
    print("• Submit sitemap to Google Search Console")
    print("• Set up Google Analytics for traffic monitoring")
    print("• Configure Google Tag Manager for enhanced tracking")
    print("• Test page speed with Google PageSpeed Insights")
    print("• Validate structured data with Google Rich Results Test")
    print("• Monitor Core Web Vitals regularly")
    print("• Set up social media sharing analytics")
    
    return audit_results

if __name__ == '__main__':
    try:
        audit_seo_implementation()
    except Exception as e:
        print(f"❌ Audit Error: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
"""
Comprehensive SEO Audit Tool for Lusan Sapkota Portfolio
Checks for common SEO issues and provides recommendations
"""

import os
import re
import json
from urllib.parse import urljoin, urlparse
from pathlib import Path
import argparse

class SEOAuditor:
    def __init__(self, base_path="/home/ubuntu/portfolio"):
        self.base_path = base_path
        self.issues = []
        self.warnings = []
        self.suggestions = []
        self.score = 100
        
    def audit_meta_tags(self, template_path="templates/index.html"):
        """Audit meta tags in HTML template"""
        print("🔍 Auditing meta tags...")
        
        try:
            with open(os.path.join(self.base_path, template_path), 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for essential meta tags
            essential_tags = [
                (r'<meta\s+name=["\']description["\']', "Meta description"),
                (r'<meta\s+name=["\']keywords["\']', "Meta keywords"),
                (r'<meta\s+name=["\']author["\']', "Meta author"),
                (r'<meta\s+property=["\']og:title["\']', "Open Graph title"),
                (r'<meta\s+property=["\']og:description["\']', "Open Graph description"),
                (r'<meta\s+property=["\']og:image["\']', "Open Graph image"),
                (r'<meta\s+name=["\']twitter:card["\']', "Twitter card"),
                (r'<link\s+rel=["\']canonical["\']', "Canonical URL"),
                (r'<meta\s+name=["\']viewport["\']', "Viewport meta tag"),
            ]
            
            for pattern, tag_name in essential_tags:
                if not re.search(pattern, content, re.IGNORECASE):
                    self.issues.append(f"Missing {tag_name}")
                    self.score -= 5
                    
            # Check title tag
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.DOTALL | re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                if len(title) < 30:
                    self.warnings.append("Title tag is too short (< 30 characters)")
                    self.score -= 2
                elif len(title) > 60:
                    self.warnings.append("Title tag is too long (> 60 characters)")
                    self.score -= 2
            else:
                self.issues.append("Missing title tag")
                self.score -= 10
                
            # Check meta description length
            desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', content, re.IGNORECASE)
            if desc_match:
                desc = desc_match.group(1)
                if len(desc) < 120:
                    self.warnings.append("Meta description is too short (< 120 characters)")
                    self.score -= 2
                elif len(desc) > 160:
                    self.warnings.append("Meta description is too long (> 160 characters)")
                    self.score -= 2
                    
            print("✅ Meta tags audit completed")
            
        except FileNotFoundError:
            self.issues.append(f"Template file not found: {template_path}")
            self.score -= 20
            
    def audit_structured_data(self, template_path="templates/index.html"):
        """Audit structured data implementation"""
        print("🔍 Auditing structured data...")
        
        try:
            with open(os.path.join(self.base_path, template_path), 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for JSON-LD structured data
            json_ld_matches = re.findall(r'<script type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
            
            if not json_ld_matches:
                self.issues.append("No structured data found")
                self.score -= 15
            else:
                # Validate JSON-LD syntax
                for i, json_data in enumerate(json_ld_matches):
                    json_content = json_data.strip()
                    # Skip Jinja2 template content that contains variables
                    if '{{' in json_content or '{%' in json_content:
                        continue  # Skip template variables, they'll be valid when rendered
                    try:
                        json.loads(json_content)
                    except json.JSONDecodeError:
                        self.issues.append(f"Invalid JSON-LD syntax in script {i+1}")
                        self.score -= 5
                        
                # Check for important schema types
                schema_types = ['Person', 'WebSite', 'WebPage', 'Organization', 'LocalBusiness']
                found_types = []
                
                for json_data in json_ld_matches:
                    for schema_type in schema_types:
                        if f'"@type": "{schema_type}"' in json_data or f'"@type":"{schema_type}"' in json_data:
                            found_types.append(schema_type)
                            
                if 'Person' not in found_types:
                    self.warnings.append("Missing Person schema")
                    self.score -= 3
                if 'WebSite' not in found_types:
                    self.warnings.append("Missing WebSite schema")
                    self.score -= 3
                    
            print("✅ Structured data audit completed")
            
        except FileNotFoundError:
            self.issues.append(f"Template file not found: {template_path}")
            
    def audit_performance(self):
        """Audit performance-related SEO factors"""
        print("🔍 Auditing performance factors...")
        
        template_path = os.path.join(self.base_path, "templates/index.html")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for preload/prefetch
            if 'rel="preload"' not in content:
                self.suggestions.append("Consider adding preload for critical resources")
                
            if 'rel="prefetch"' not in content:
                self.suggestions.append("Consider adding prefetch for important resources")
                
            # Check for lazy loading
            img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
            lazy_loaded = sum(1 for img in img_tags if 'loading="lazy"' in img)
            
            if img_tags and lazy_loaded / len(img_tags) < 0.5:
                self.warnings.append("Consider implementing lazy loading for images")
                self.score -= 2
                
            # Check for minification hints
            if '.min.css' not in content and '.min.js' not in content:
                self.suggestions.append("Consider using minified CSS and JS files")
                
            print("✅ Performance audit completed")
            
        except FileNotFoundError:
            self.issues.append("Template file not found for performance audit")
            
    def audit_mobile_optimization(self):
        """Audit mobile optimization"""
        print("🔍 Auditing mobile optimization...")
        
        template_path = os.path.join(self.base_path, "templates/index.html")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check viewport meta tag
            if 'name="viewport"' not in content:
                self.issues.append("Missing viewport meta tag")
                self.score -= 10
            else:
                viewport_match = re.search(r'<meta\s+name=["\']viewport["\']\s+content=["\']([^"\']*)["\']', content, re.IGNORECASE)
                if viewport_match:
                    viewport = viewport_match.group(1)
                    if 'width=device-width' not in viewport:
                        self.warnings.append("Viewport should include width=device-width")
                        self.score -= 3
                    if 'initial-scale=1' not in viewport:
                        self.warnings.append("Viewport should include initial-scale=1")
                        self.score -= 2
                        
            # Check for mobile-friendly meta tags
            mobile_tags = [
                'apple-mobile-web-app-capable',
                'mobile-web-app-capable',
                'theme-color'
            ]
            
            for tag in mobile_tags:
                if f'name="{tag}"' not in content:
                    self.suggestions.append(f"Consider adding {tag} meta tag for better mobile experience")
                    
            print("✅ Mobile optimization audit completed")
            
        except FileNotFoundError:
            self.issues.append("Template file not found for mobile audit")
            
    def audit_accessibility(self):
        """Audit accessibility factors that affect SEO"""
        print("🔍 Auditing accessibility factors...")
        
        template_path = os.path.join(self.base_path, "templates/index.html")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for lang attribute
            html_content = '\n'.join(content.split('\n')[:5])  # Check first 5 lines
            if 'lang=' not in html_content:
                self.issues.append("Missing lang attribute in html tag")
                self.score -= 5
                
            # Check for alt attributes in images
            img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
            imgs_without_alt = [img for img in img_tags if 'alt=' not in img]
            
            if imgs_without_alt:
                self.warnings.append(f"{len(imgs_without_alt)} images missing alt attributes")
                self.score -= min(len(imgs_without_alt), 10)
                
            # Check for heading structure
            headings = re.findall(r'<h([1-6])[^>]*>', content, re.IGNORECASE)
            if headings:
                if '1' not in headings:
                    self.warnings.append("Missing H1 tag")
                    self.score -= 5
                if headings.count('1') > 1:
                    self.warnings.append("Multiple H1 tags found")
                    self.score -= 3
                    
            print("✅ Accessibility audit completed")
            
        except FileNotFoundError:
            self.issues.append("Template file not found for accessibility audit")
            
    def audit_technical_seo(self):
        """Audit technical SEO factors"""
        print("🔍 Auditing technical SEO...")
        
        # Check for robots.txt
        robots_path = os.path.join(self.base_path, "static/robots.txt")
        if not os.path.exists(robots_path):
            self.issues.append("Missing robots.txt file")
            self.score -= 10
        else:
            with open(robots_path, 'r') as f:
                robots_content = f.read()
                if 'Sitemap:' not in robots_content:
                    self.warnings.append("robots.txt should include sitemap reference")
                    self.score -= 3
                    
        # Check for sitemap
        sitemap_path = os.path.join(self.base_path, "static/sitemap.xml")
        if not os.path.exists(sitemap_path):
            self.issues.append("Missing sitemap.xml file")
            self.score -= 15
            
        # Check for manifest.json
        manifest_path = os.path.join(self.base_path, "static/manifest.json")
        if not os.path.exists(manifest_path):
            self.warnings.append("Missing manifest.json for PWA")
            self.score -= 5
            
        # Check for service worker
        sw_path = os.path.join(self.base_path, "static/sw.js")
        if not os.path.exists(sw_path):
            self.suggestions.append("Consider implementing service worker for better performance")
            
        print("✅ Technical SEO audit completed")
        
    def audit_content_quality(self):
        """Audit content quality factors"""
        print("🔍 Auditing content quality...")
        
        template_path = os.path.join(self.base_path, "templates/index.html")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Remove HTML tags for text analysis
            text_content = re.sub(r'<[^>]+>', ' ', content)
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            # Check content length
            word_count = len(text_content.split())
            if word_count < 300:
                self.warnings.append(f"Content might be too short ({word_count} words)")
                self.score -= 5
                
            # Check for duplicate content patterns
            sentences = text_content.split('.')
            if len(sentences) != len(set(sentences)):
                self.warnings.append("Potential duplicate content detected")
                self.score -= 3
                
            print("✅ Content quality audit completed")
            
        except FileNotFoundError:
            self.issues.append("Template file not found for content audit")
            
    def run_full_audit(self):
        """Run complete SEO audit"""
        print("🚀 Starting comprehensive SEO audit...\n")
        
        self.audit_meta_tags()
        self.audit_structured_data()
        self.audit_performance()
        self.audit_mobile_optimization()
        self.audit_accessibility()
        self.audit_technical_seo()
        self.audit_content_quality()
        
        return self.generate_report()
        
    def generate_report(self):
        """Generate audit report"""
        print("\n" + "="*50)
        print("📊 SEO AUDIT REPORT")
        print("="*50)
        
        # Calculate score
        final_score = max(0, min(100, self.score))
        
        print(f"🎯 Overall SEO Score: {final_score}/100")
        
        if final_score >= 90:
            grade = "A+"
            color = "🟢"
        elif final_score >= 80:
            grade = "A"
            color = "🟢"
        elif final_score >= 70:
            grade = "B"
            color = "🟡"
        elif final_score >= 60:
            grade = "C"
            color = "🟡"
        else:
            grade = "D"
            color = "🔴"
            
        print(f"{color} Grade: {grade}")
        print()
        
        # Issues (Critical)
        if self.issues:
            print("🚨 CRITICAL ISSUES (Fix immediately):")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
            print()
            
        # Warnings (Important)
        if self.warnings:
            print("⚠️ WARNINGS (Should fix):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
            print()
            
        # Suggestions (Improvements)
        if self.suggestions:
            print("💡 SUGGESTIONS (Nice to have):")
            for i, suggestion in enumerate(self.suggestions, 1):
                print(f"  {i}. {suggestion}")
            print()
            
        print("="*50)
        
        # Recommendations
        if final_score < 80:
            print("🔧 PRIORITY ACTIONS:")
            print("1. Fix all critical issues first")
            print("2. Address warnings in order of impact")
            print("3. Implement performance optimizations")
            print("4. Enhance structured data")
            print("5. Improve content quality and length")
            
        return {
            'score': final_score,
            'grade': grade,
            'issues': self.issues,
            'warnings': self.warnings,
            'suggestions': self.suggestions
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SEO Audit Tool for Portfolio')
    parser.add_argument('--path', default='/home/ubuntu/portfolio', help='Path to portfolio directory')
    parser.add_argument('--output', help='Output JSON file for results')
    
    args = parser.parse_args()
    
    auditor = SEOAuditor(args.path)
    results = auditor.run_full_audit()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📄 Results saved to: {args.output}")

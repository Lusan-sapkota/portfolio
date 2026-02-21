#!/usr/bin/env python3
"""
Comprehensive SEO Audit Script
Validates structured data, meta tags, performance hints, and more.
"""
import sys
import json
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:5000"

VALID_SCHEMA_TYPES = {
    "Person", "WebSite", "WebPage", "ProfilePage", "Organization",
    "ImageObject", "CollegeOrUniversity", "Occupation", "Country", "Place",
    "PostalAddress", "SearchAction", "BreadcrumbList", "ListItem",
    "OfferCatalog", "Offer", "Service", "ProfessionalService",
    "ItemList", "SoftwareSourceCode", "LocalBusiness", "GeoCoordinates",
    "OpeningHoursSpecification", "FAQPage", "Question", "Answer",
    "DefinedTerm", "EducationalOccupationalCredential",
    "EducationalOrganization", "EducationalOccupationalProgram",
    "Course", "Event", "VirtualLocation", "ContactPage", "ContactPoint",
    "AggregateRating", "Review", "Rating", "MonetaryAmountDistribution",
    "City", "DonateAction", "EmployeeRole", "OrganizationRole",
}

PAGES = [
    ("/", "Homepage"),
    ("/wiki/", "Wiki"),
    ("/donation/", "Donation"),
    ("/git/", "Git"),
]

passed = 0
failed = 0
warnings = 0
details = []

def log_pass(msg):
    global passed
    passed += 1
    print(f"  PASS  {msg}")

def log_fail(msg):
    global failed
    failed += 1
    print(f"  FAIL  {msg}")
    details.append(("FAIL", msg))

def log_warn(msg):
    global warnings
    warnings += 1
    print(f"  WARN  {msg}")
    details.append(("WARN", msg))

def validate_json_ld(script_tag, page_name, index):
    prefix = f"[{page_name} schema #{index}]"
    raw = script_tag.string
    if not raw or not raw.strip():
        log_fail(f"{prefix} Empty JSON-LD block")
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        log_fail(f"{prefix} Invalid JSON: {e}")
        lines = raw.split('\n')
        err_line = e.lineno - 1
        start = max(0, err_line - 2)
        end = min(len(lines), err_line + 3)
        for i in range(start, end):
            marker = ">>>" if i == err_line else "   "
            print(f"        {marker} L{i+1}: {lines[i].rstrip()}")
        return
    log_pass(f"{prefix} Valid JSON syntax")
    if isinstance(data, dict):
        validate_schema_object(data, prefix)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            validate_schema_object(item, f"{prefix}[{i}]")

def validate_schema_object(data, prefix):
    if not isinstance(data, dict):
        return
    ctx = data.get("@context")
    if ctx and ctx != "https://schema.org":
        log_warn(f"{prefix} Non-standard @context: {ctx}")
    schema_type = data.get("@type")
    if schema_type and schema_type not in VALID_SCHEMA_TYPES:
        log_fail(f"{prefix} Unknown/invalid @type: \"{schema_type}\"")
    elif schema_type:
        log_pass(f"{prefix} Valid @type: {schema_type}")
    if "@graph" in data:
        for i, item in enumerate(data["@graph"]):
            validate_schema_object(item, f"{prefix}/@graph[{i}]")
    for key, value in data.items():
        if key.startswith("@"):
            continue
        if isinstance(value, dict) and "@type" in value:
            validate_schema_object(value, f"{prefix}/{key}")
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict) and "@type" in item:
                    validate_schema_object(item, f"{prefix}/{key}[{i}]")

def audit_page(url, page_name):
    print(f"\n{'='*70}")
    print(f"  AUDITING: {page_name} ({url})")
    print(f"{'='*70}")
    try:
        resp = requests.get(url, timeout=10)
    except requests.RequestException as e:
        log_fail(f"[{page_name}] Cannot fetch page: {e}")
        return
    if resp.status_code != 200:
        log_fail(f"[{page_name}] HTTP {resp.status_code}")
        return
    log_pass(f"[{page_name}] HTTP 200 OK")
    soup = BeautifulSoup(resp.content, 'html.parser')

    print(f"\n  -- Meta Tags --")
    title = soup.find('title')
    if title and title.text.strip():
        tlen = len(title.text.strip())
        if 30 <= tlen <= 65:
            log_pass(f"[{page_name}] Title tag ({tlen} chars)")
        elif tlen > 65:
            log_warn(f"[{page_name}] Title too long ({tlen} chars)")
        else:
            log_warn(f"[{page_name}] Title too short ({tlen} chars)")
    else:
        log_fail(f"[{page_name}] Missing title tag")

    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        dlen = len(meta_desc.get('content', ''))
        if 120 <= dlen <= 160:
            log_pass(f"[{page_name}] Meta description ({dlen} chars)")
        elif dlen > 160:
            log_warn(f"[{page_name}] Meta description too long ({dlen} chars)")
        elif dlen > 0:
            log_warn(f"[{page_name}] Meta description short ({dlen} chars)")
        else:
            log_fail(f"[{page_name}] Empty meta description")
    else:
        log_fail(f"[{page_name}] Missing meta description")

    canonical = soup.find('link', rel='canonical')
    if canonical and canonical.get('href'):
        log_pass(f"[{page_name}] Canonical URL")
    else:
        log_fail(f"[{page_name}] Missing canonical URL")

    robots = soup.find('meta', attrs={'name': 'robots'})
    if robots:
        content = robots.get('content', '')
        if 'noindex' in content:
            log_warn(f"[{page_name}] Robots blocks indexing")
        else:
            log_pass(f"[{page_name}] Robots meta OK")
    else:
        log_warn(f"[{page_name}] No robots meta tag")

    viewport = soup.find('meta', attrs={'name': 'viewport'})
    if viewport and 'width=device-width' in viewport.get('content', ''):
        log_pass(f"[{page_name}] Mobile viewport configured")
    else:
        log_fail(f"[{page_name}] Missing viewport")

    charset = soup.find('meta', charset=True) or soup.find('meta', attrs={'http-equiv': 'Content-Type'})
    if charset:
        log_pass(f"[{page_name}] Charset declared")
    else:
        log_warn(f"[{page_name}] No charset meta tag")

    print(f"\n  -- Open Graph Tags --")
    required_og = ['og:title', 'og:description', 'og:image', 'og:url', 'og:type']
    og_tags = {tag.get('property'): tag.get('content') for tag in soup.find_all('meta', property=True) if tag.get('property', '').startswith('og:')}
    for req in required_og:
        if req in og_tags and og_tags[req]:
            log_pass(f"[{page_name}] {req}")
        else:
            log_fail(f"[{page_name}] Missing {req}")

    print(f"\n  -- Twitter Card Tags --")
    required_tw = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image']
    tw_tags = {}
    for tag in soup.find_all('meta'):
        name = tag.get('name') or tag.get('property', '')
        if name.startswith('twitter:'):
            tw_tags[name] = tag.get('content')
    for req in required_tw:
        if req in tw_tags and tw_tags[req]:
            log_pass(f"[{page_name}] {req}")
        else:
            log_warn(f"[{page_name}] Missing {req}")

    print(f"\n  -- Structured Data (JSON-LD) --")
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    if json_ld_scripts:
        log_pass(f"[{page_name}] {len(json_ld_scripts)} JSON-LD block(s)")
        for i, script in enumerate(json_ld_scripts, 1):
            validate_json_ld(script, page_name, i)
    else:
        log_fail(f"[{page_name}] No JSON-LD structured data")

    print(f"\n  -- Heading Structure --")
    h1s = soup.find_all('h1')
    if len(h1s) == 1:
        log_pass(f"[{page_name}] Single H1")
    elif len(h1s) == 0:
        log_fail(f"[{page_name}] No H1 tag")
    else:
        log_warn(f"[{page_name}] Multiple H1 tags ({len(h1s)})")

    headings = soup.find_all(re.compile(r'^h[1-6]$'))
    if headings:
        levels = [int(h.name[1]) for h in headings]
        skips = []
        for i in range(1, len(levels)):
            if levels[i] > levels[i-1] + 1:
                skips.append(f"H{levels[i-1]}->H{levels[i]}")
        if skips:
            log_warn(f"[{page_name}] Heading skips: {', '.join(skips[:3])}")
        else:
            log_pass(f"[{page_name}] Heading hierarchy OK")

    print(f"\n  -- Image SEO --")
    images = soup.find_all('img')
    if images:
        missing_alt = [img for img in images if not img.get('alt')]
        if missing_alt:
            log_warn(f"[{page_name}] {len(missing_alt)}/{len(images)} images missing alt")
        else:
            log_pass(f"[{page_name}] All {len(images)} images have alt text")
        missing_lazy = [img for img in images if not img.get('loading')]
        if missing_lazy and len(missing_lazy) > 3:
            log_warn(f"[{page_name}] {len(missing_lazy)} images missing loading attr")
        else:
            log_pass(f"[{page_name}] Images have loading attributes")
    else:
        log_pass(f"[{page_name}] No inline images")

    print(f"\n  -- Link SEO --")
    ext_links = soup.find_all('a', href=re.compile(r'^https?://'))
    noopener_missing = []
    for link in ext_links:
        rel = link.get('rel', [])
        if isinstance(rel, str):
            rel = rel.split()
        if 'noopener' not in rel and 'noreferrer' not in rel:
            noopener_missing.append(link.get('href', '')[:50])
    if noopener_missing:
        log_warn(f"[{page_name}] {len(noopener_missing)} external links missing rel=noopener")
    else:
        log_pass(f"[{page_name}] External links have rel=noopener")

    print(f"\n  -- Performance Hints --")
    preconnects = soup.find_all('link', rel='preconnect')
    dns_prefetch = soup.find_all('link', rel='dns-prefetch')
    if preconnects:
        log_pass(f"[{page_name}] {len(preconnects)} preconnect hint(s)")
    else:
        log_warn(f"[{page_name}] No preconnect hints")
    if dns_prefetch:
        log_pass(f"[{page_name}] {len(dns_prefetch)} dns-prefetch hint(s)")

    print(f"\n  -- Security Headers --")
    security_headers = {
        'X-Content-Type-Options': resp.headers.get('X-Content-Type-Options'),
        'X-Frame-Options': resp.headers.get('X-Frame-Options'),
        'X-XSS-Protection': resp.headers.get('X-XSS-Protection'),
        'Content-Security-Policy': resp.headers.get('Content-Security-Policy'),
        'Strict-Transport-Security': resp.headers.get('Strict-Transport-Security'),
    }
    for header, value in security_headers.items():
        if value:
            log_pass(f"[{page_name}] {header}")
        else:
            log_warn(f"[{page_name}] Missing {header}")

    return soup

def audit_global():
    print(f"\n{'='*70}")
    print(f"  GLOBAL FILES")
    print(f"{'='*70}")

    print(f"\n  -- robots.txt --")
    try:
        resp = requests.get(f"{BASE_URL}/robots.txt", timeout=5)
        if resp.status_code == 200:
            log_pass("robots.txt accessible")
            if 'Sitemap:' in resp.text:
                log_pass("robots.txt references sitemap")
            else:
                log_warn("robots.txt missing Sitemap directive")
            if 'User-agent:' in resp.text:
                log_pass("robots.txt has User-agent directives")
            else:
                log_warn("robots.txt missing User-agent")
        else:
            log_fail(f"robots.txt returned HTTP {resp.status_code}")
    except Exception as e:
        log_fail(f"Cannot fetch robots.txt: {e}")

    print(f"\n  -- sitemap.xml --")
    try:
        resp = requests.get(f"{BASE_URL}/sitemap.xml", timeout=5)
        if resp.status_code == 200:
            ct = resp.headers.get('content-type', '')
            if 'xml' in ct or resp.text.strip().startswith('<?xml'):
                log_pass("sitemap.xml accessible and valid XML")
                urls_count = resp.text.count('<url>')
                if urls_count > 0:
                    log_pass(f"sitemap.xml contains {urls_count} URL(s)")
                else:
                    log_warn("sitemap.xml empty")
            else:
                log_fail(f"sitemap.xml wrong content-type: {ct}")
        else:
            log_fail(f"sitemap.xml returned HTTP {resp.status_code}")
    except Exception as e:
        log_fail(f"Cannot fetch sitemap.xml: {e}")

    print(f"\n  -- manifest.json (PWA) --")
    try:
        resp = requests.get(f"{BASE_URL}/manifest.json", timeout=5)
        if resp.status_code == 200:
            try:
                data = resp.json()
                for field in ['name', 'short_name', 'icons', 'start_url', 'display']:
                    if field in data:
                        log_pass(f"manifest.json has '{field}'")
                    else:
                        log_warn(f"manifest.json missing '{field}'")
                if 'theme_color' in data:
                    log_pass(f"manifest.json has theme_color")
                if 'background_color' in data:
                    log_pass(f"manifest.json has background_color")
            except json.JSONDecodeError:
                log_fail("manifest.json invalid JSON")
        else:
            log_fail(f"manifest.json returned HTTP {resp.status_code}")
    except Exception as e:
        log_fail(f"Cannot fetch manifest.json: {e}")

    print(f"\n  -- security.txt --")
    found = False
    for path in ['/.well-known/security.txt', '/security.txt']:
        try:
            resp = requests.get(f"{BASE_URL}{path}", timeout=5)
            if resp.status_code == 200:
                log_pass(f"security.txt accessible at {path}")
                found = True
                break
        except:
            pass
    if not found:
        log_warn("security.txt not found")

    print(f"\n  -- Favicon --")
    try:
        resp = requests.get(f"{BASE_URL}/favicon.ico", timeout=5)
        if resp.status_code == 200:
            log_pass("favicon.ico accessible")
        else:
            log_warn(f"favicon.ico HTTP {resp.status_code}")
    except:
        log_warn("favicon.ico not accessible")

def print_report():
    total = passed + failed + warnings
    score = (passed / total * 100) if total > 0 else 0

    print(f"\n{'='*70}")
    print(f"  SEO AUDIT REPORT")
    print(f"{'='*70}")
    print(f"  Total checks:  {total}")
    print(f"  Passed:        {passed}")
    print(f"  Failed:        {failed}")
    print(f"  Warnings:      {warnings}")
    print(f"  SEO Score:     {score:.1f}%")
    print(f"{'='*70}")

    if details:
        print(f"\n  ISSUES:")
        print(f"  {'-'*66}")
        for severity, msg in details:
            marker = "!!" if severity == "FAIL" else "??"
            print(f"  {marker} {msg}")

    print(f"\n{'='*70}")
    if score == 100:
        print("  PERFECT! 100% SEO score achieved!")
    elif score >= 95:
        print("  OUTSTANDING! Near-perfect SEO implementation.")
    elif score >= 90:
        print("  EXCELLENT! SEO implementation is outstanding.")
    elif score >= 80:
        print("  GREAT! Strong SEO with minor improvements possible.")
    else:
        print("  GOOD! Solid foundation with room for improvement.")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  COMPREHENSIVE SEO AUDIT - lusansapkota.com.np")
    print("  Target: " + BASE_URL)
    print("="*70)
    for path, name in PAGES:
        url = f"{BASE_URL}{path}"
        try:
            audit_page(url, name)
        except Exception as e:
            log_fail(f"[{name}] Audit crashed: {e}")
    audit_global()
    print_report()

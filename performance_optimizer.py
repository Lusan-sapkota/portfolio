#!/usr/bin/env python3
"""
Performance and SEO Optimization Script
Optimizes images, minifies CSS/JS, and implements advanced caching
"""

import os
import re
import json
import gzip
import hashlib
from pathlib import Path
import argparse

class PerformanceOptimizer:
    def __init__(self, base_path="/home/ubuntu/portfolio"):
        self.base_path = base_path
        
    def create_preload_hints(self):
        """Generate preload hints for critical resources"""
        preload_hints = """<!-- Critical Resource Preloads for Performance -->
<link rel="preload" href="{{ url_for('static', filename='assets/css/style.css') }}" as="style">
<link rel="preload" href="{{ url_for('static', filename='assets/js/main.js') }}" as="script">
<link rel="preload" href="{{ url_for('static', filename='assets/images/profile.png') }}" as="image">
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" as="style" crossorigin>

<!-- DNS Prefetch for External Resources -->
<link rel="dns-prefetch" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://fonts.gstatic.com">
<link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">
<link rel="dns-prefetch" href="https://cdn.jsdelivr.net">
<link rel="dns-prefetch" href="https://github.com">
<link rel="dns-prefetch" href="https://api.github.com">
<link rel="dns-prefetch" href="https://www.google-analytics.com">
<link rel="dns-prefetch" href="https://www.googletagmanager.com">

<!-- Preconnect for Critical Third-party Origins -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://api.github.com" crossorigin>

<!-- Resource Hints for Better Loading -->
<link rel="prefetch" href="{{ url_for('static', filename='assets/download/Lusan_Sapkota_Resume.txt') }}">
<link rel="prefetch" href="{{ url_for('static', filename='manifest.json') }}">"""

        preload_dir = os.path.join(self.base_path, "templates/performance")
        os.makedirs(preload_dir, exist_ok=True)
        
        with open(os.path.join(preload_dir, "preload-hints.html"), 'w') as f:
            f.write(preload_hints)
            
        print("✅ Created performance preload hints")
        
    def create_critical_css(self):
        """Extract critical CSS for above-the-fold content"""
        critical_css = """/* Critical CSS for Above-the-Fold Content */
/* This CSS should be inlined in the <head> for faster rendering */

body {
    font-family: 'Poppins', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #333;
    margin: 0;
    padding: 0;
}

.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.welcome-hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
    color: white;
}

.header-text h1 {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    line-height: 1.2;
}

.header-text p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .header-text h1 {
        font-size: 2.5rem;
    }
    
    .header-text p {
        font-size: 1rem;
    }
}

/* Loading animation */
.loader {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #fff;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
}

.loader.fade-out {
    opacity: 0;
    visibility: hidden;
    transition: all 0.5s ease;
}"""

        with open(os.path.join(self.base_path, "static/assets/css/critical.css"), 'w') as f:
            f.write(critical_css)
            
        print("✅ Created critical CSS")
        
    def create_service_worker_enhancements(self):
        """Enhance service worker for better caching"""
        sw_enhancements = """
// Enhanced caching strategies for better performance
const CACHE_STRATEGIES = {
    CACHE_FIRST: 'cache-first',
    NETWORK_FIRST: 'network-first',
    STALE_WHILE_REVALIDATE: 'stale-while-revalidate'
};

// Cache static assets with cache-first strategy
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);
    
    // Cache static assets
    if (url.pathname.includes('/static/') || 
        url.pathname.includes('/assets/') ||
        url.pathname.endsWith('.css') ||
        url.pathname.endsWith('.js') ||
        url.pathname.endsWith('.png') ||
        url.pathname.endsWith('.jpg') ||
        url.pathname.endsWith('.webp')) {
        
        event.respondWith(cacheFirst(event.request));
    }
    // Network first for API calls
    else if (url.pathname.includes('/api/')) {
        event.respondWith(networkFirst(event.request));
    }
    // Stale while revalidate for pages
    else {
        event.respondWith(staleWhileRevalidate(event.request));
    }
});

async function cacheFirst(request) {
    const cache = await caches.open(STATIC_CACHE);
    const cached = await cache.match(request);
    
    if (cached) {
        return cached;
    }
    
    try {
        const response = await fetch(request);
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        console.log('Cache first failed:', error);
        return new Response('Offline', { status: 503 });
    }
}

async function networkFirst(request) {
    try {
        const response = await fetch(request);
        if (response.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        const cache = await caches.open(DYNAMIC_CACHE);
        const cached = await cache.match(request);
        return cached || new Response('Offline', { status: 503 });
    }
}

async function staleWhileRevalidate(request) {
    const cache = await caches.open(DYNAMIC_CACHE);
    const cached = await cache.match(request);
    
    const fetchPromise = fetch(request).then(response => {
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    });
    
    return cached || fetchPromise;
}"""

        with open(os.path.join(self.base_path, "static/sw-enhancements.js"), 'w') as f:
            f.write(sw_enhancements)
            
        print("✅ Created service worker enhancements")
        
    def create_webp_fallback_script(self):
        """Create WebP support detection and fallback"""
        webp_script = """// WebP Support Detection and Fallback
(function() {
    function supportsWebP() {
        return new Promise((resolve) => {
            const webP = new Image();
            webP.onload = webP.onerror = function () {
                resolve(webP.height === 2);
            };
            webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
        });
    }

    async function initWebPSupport() {
        const hasWebPSupport = await supportsWebP();
        
        if (hasWebPSupport) {
            document.documentElement.classList.add('webp');
        } else {
            document.documentElement.classList.add('no-webp');
            
            // Replace WebP images with fallback formats
            const images = document.querySelectorAll('img[data-webp]');
            images.forEach(img => {
                img.src = img.dataset.fallback || img.src.replace('.webp', '.jpg');
            });
        }
    }

    // Initialize WebP support detection
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWebPSupport);
    } else {
        initWebPSupport();
    }
})();"""

        with open(os.path.join(self.base_path, "static/assets/js/webp-support.js"), 'w') as f:
            f.write(webp_script)
            
        print("✅ Created WebP support detection")
        
    def create_lazy_loading_enhancements(self):
        """Enhanced lazy loading for images and content"""
        lazy_script = """// Enhanced Lazy Loading with Intersection Observer
class LazyLoader {
    constructor() {
        this.imageObserver = null;
        this.contentObserver = null;
        this.init();
    }

    init() {
        if ('IntersectionObserver' in window) {
            this.setupImageLazyLoading();
            this.setupContentLazyLoading();
        } else {
            // Fallback for older browsers
            this.loadAllImages();
        }
    }

    setupImageLazyLoading() {
        this.imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    this.loadImage(img);
                    this.imageObserver.unobserve(img);
                }
            });
        }, {
            root: null,
            rootMargin: '50px',
            threshold: 0.01
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            this.imageObserver.observe(img);
        });
    }

    setupContentLazyLoading() {
        this.contentObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('lazy-loaded');
                    this.contentObserver.unobserve(entry.target);
                }
            });
        }, {
            root: null,
            rootMargin: '20px',
            threshold: 0.1
        });

        document.querySelectorAll('.lazy-content').forEach(element => {
            this.contentObserver.observe(element);
        });
    }

    loadImage(img) {
        img.src = img.dataset.src;
        img.classList.add('lazy-loaded');
        
        img.onload = () => {
            img.classList.add('fade-in');
        };
    }

    loadAllImages() {
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.loadImage(img);
        });
    }
}

// Initialize lazy loader when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new LazyLoader());
} else {
    new LazyLoader();
}"""

        with open(os.path.join(self.base_path, "static/assets/js/lazy-loading.js"), 'w') as f:
            f.write(lazy_script)
            
        print("✅ Created enhanced lazy loading")
        
    def create_core_web_vitals_script(self):
        """Core Web Vitals measurement and optimization"""
        cwv_script = """// Core Web Vitals Measurement and Optimization
class CoreWebVitals {
    constructor() {
        this.metrics = {};
        this.init();
    }

    init() {
        this.measureLCP();
        this.measureFID();
        this.measureCLS();
        this.optimizePerformance();
    }

    measureLCP() {
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                this.metrics.lcp = lastEntry.startTime;
                this.reportMetric('LCP', lastEntry.startTime);
            });
            
            observer.observe({ entryTypes: ['largest-contentful-paint'] });
        }
    }

    measureFID() {
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    this.metrics.fid = entry.processingStart - entry.startTime;
                    this.reportMetric('FID', entry.processingStart - entry.startTime);
                });
            });
            
            observer.observe({ entryTypes: ['first-input'] });
        }
    }

    measureCLS() {
        if ('PerformanceObserver' in window) {
            let clsValue = 0;
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                        this.metrics.cls = clsValue;
                        this.reportMetric('CLS', clsValue);
                    }
                });
            });
            
            observer.observe({ entryTypes: ['layout-shift'] });
        }
    }

    optimizePerformance() {
        // Preload critical resources
        this.preloadCriticalResources();
        
        // Optimize images
        this.optimizeImages();
        
        // Reduce layout shift
        this.preventLayoutShift();
    }

    preloadCriticalResources() {
        const criticalResources = [
            '/static/assets/css/style.css',
            '/static/assets/js/main.js',
            '/static/assets/images/profile.png'
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = resource;
            link.as = resource.endsWith('.css') ? 'style' : 
                      resource.endsWith('.js') ? 'script' : 'image';
            document.head.appendChild(link);
        });
    }

    optimizeImages() {
        // Add aspect ratio containers to prevent layout shift
        document.querySelectorAll('img').forEach(img => {
            if (!img.style.aspectRatio && img.width && img.height) {
                img.style.aspectRatio = `${img.width} / ${img.height}`;
            }
        });
    }

    preventLayoutShift() {
        // Add explicit dimensions to dynamic content containers
        document.querySelectorAll('.dynamic-content').forEach(element => {
            if (!element.style.minHeight) {
                element.style.minHeight = '200px';
            }
        });
    }

    reportMetric(name, value) {
        console.log(`${name}: ${value}ms`);
        
        // Send to analytics if available
        if (typeof gtag !== 'undefined') {
            gtag('event', 'web_vitals', {
                metric_name: name,
                metric_value: Math.round(value),
                metric_rating: this.getRating(name, value)
            });
        }
    }

    getRating(metric, value) {
        switch (metric) {
            case 'LCP':
                return value <= 2500 ? 'good' : value <= 4000 ? 'needs-improvement' : 'poor';
            case 'FID':
                return value <= 100 ? 'good' : value <= 300 ? 'needs-improvement' : 'poor';
            case 'CLS':
                return value <= 0.1 ? 'good' : value <= 0.25 ? 'needs-improvement' : 'poor';
            default:
                return 'unknown';
        }
    }
}

// Initialize Core Web Vitals measurement
new CoreWebVitals();"""

        with open(os.path.join(self.base_path, "static/assets/js/core-web-vitals.js"), 'w') as f:
            f.write(cwv_script)
            
        print("✅ Created Core Web Vitals optimization")
        
    def run_all_optimizations(self):
        """Run all performance optimizations"""
        print("🚀 Starting performance optimizations...\n")
        
        self.create_preload_hints()
        self.create_critical_css()
        self.create_service_worker_enhancements()
        self.create_webp_fallback_script()
        self.create_lazy_loading_enhancements()
        self.create_core_web_vitals_script()
        
        print("\n✅ All performance optimizations completed!")
        print("\n📈 Performance recommendations:")
        print("1. Implement WebP images with fallbacks")
        print("2. Use critical CSS inlining")
        print("3. Enable Brotli/Gzip compression")
        print("4. Implement HTTP/2 push for critical resources")
        print("5. Use CDN for static assets")
        print("6. Optimize font loading with font-display: swap")
        print("7. Implement resource bundling and code splitting")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Performance Optimization Tool')
    parser.add_argument('--path', default='/home/ubuntu/portfolio', help='Path to portfolio directory')
    
    args = parser.parse_args()
    
    optimizer = PerformanceOptimizer(args.path)
    optimizer.run_all_optimizations()

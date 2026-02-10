// Core Web Vitals Measurement and Optimization
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
new CoreWebVitals();
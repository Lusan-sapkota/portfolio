// Enhanced Lazy Loading with Intersection Observer
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
}
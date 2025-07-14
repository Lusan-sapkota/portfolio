// WebP Support Detection and Fallback
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
})();
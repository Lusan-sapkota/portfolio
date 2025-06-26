// Service Worker Cache Update Script
// Add this to your main JavaScript file or run in browser console

async function updateServiceWorker() {
    if ('serviceWorker' in navigator) {
        try {
            // Get all registrations
            const registrations = await navigator.serviceWorker.getRegistrations();
            
            // Unregister old service workers
            for (let registration of registrations) {
                await registration.unregister();
                console.log('Unregistered old service worker');
            }
            
            // Clear old caches
            const cacheNames = await caches.keys();
            for (let cacheName of cacheNames) {
                if (cacheName.includes('lusan-portfolio-v1.0.0') || cacheName.includes('lusan-static-v1.0.0') || cacheName.includes('lusan-dynamic-v1.0.0')) {
                    await caches.delete(cacheName);
                    console.log('Deleted old cache:', cacheName);
                }
            }
            
            // Register new service worker
            const registration = await navigator.serviceWorker.register('/static/sw.js');
            console.log('New service worker registered successfully');
            
            // Force update
            if (registration.waiting) {
                registration.waiting.postMessage({ action: 'skipWaiting' });
            }
            
            // Reload page to use new service worker
            window.location.reload();
            
        } catch (error) {
            console.error('Error updating service worker:', error);
        }
    }
}

// Run the update
updateServiceWorker();

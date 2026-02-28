// Service Worker for Lusan Sapkota Portfolio PWA
// Version 1.1.0 - Fixed POST request caching issue

const CACHE_NAME = 'lusan-portfolio-v1.1.0';
const STATIC_CACHE = 'lusan-static-v1.1.0';
const DYNAMIC_CACHE = 'lusan-dynamic-v1.1.0';

// Resources to cache
const STATIC_ASSETS = [
    '/',
    '/static/assets/css/style.css',
    '/static/assets/css/animate.css',
    '/static/assets/css/responsive.css',
    '/static/assets/js/main.js',
    '/static/assets/logo/logo.png',
    '/static/assets/images/profile.webp',
    '/static/assets/images/profile.png',
    '/static/manifest.json',
    '/offline.html'
];

// API endpoints that should be cached
const API_CACHE_ENDPOINTS = [
    '/api/projects',
    '/api/skills',
    '/api/testimonials'
];

// Install event - cache static assets
self.addEventListener('install', event => {
    console.log('Service Worker: Installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Service Worker: Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('Service Worker: Skip waiting...');
                return self.skipWaiting();
            })
            .catch(err => {
                console.log('Service Worker: Cache failed', err);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker: Activating...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cache => {
                        if (cache !== STATIC_CACHE && cache !== DYNAMIC_CACHE) {
                            console.log('Service Worker: Clearing old cache', cache);
                            return caches.delete(cache);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker: Claiming clients...');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip cross-origin requests
    if (url.origin !== location.origin) return;
    
    // Skip non-GET requests for admin routes
    if (request.method !== 'GET' && (url.pathname.includes('/admin/') || url.pathname.includes('/api/'))) {
        return; // Let the browser handle it normally
    }
    
    // Handle different types of requests
    if (request.destination === 'document') {
        // HTML pages - Network first, fallback to cache
        event.respondWith(handleDocumentRequest(request));
    } else if (request.destination === 'image') {
        // Images - Cache first
        event.respondWith(handleImageRequest(request));
    } else if (request.url.includes('/api/')) {
        // API requests - Network first with cache fallback
        event.respondWith(handleApiRequest(request));
    } else if (request.url.includes('/admin/')) {
        // Admin routes - Always go to network, don't cache
        event.respondWith(fetch(request));
    } else {
        // Static assets - Cache first
        event.respondWith(handleStaticRequest(request));
    }
});

// Handle document requests (HTML pages)
async function handleDocumentRequest(request) {
    try {
        const networkResponse = await fetch(request);
        // Only cache GET requests
        if (request.method === 'GET') {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        const cachedResponse = await caches.match(request);
        return cachedResponse || caches.match('/offline.html');
    }
}

// Handle image requests
async function handleImageRequest(request) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
        return cachedResponse;
    }
    
    try {
        const networkResponse = await fetch(request);
        const cache = await caches.open(DYNAMIC_CACHE);
        cache.put(request, networkResponse.clone());
        return networkResponse;
    } catch (error) {
        // Return placeholder image or cached version
        return cachedResponse;
    }
}

// Handle API requests
async function handleApiRequest(request) {
    // For non-GET requests, always go to network
    if (request.method !== 'GET') {
        return fetch(request);
    }
    
    try {
        const networkResponse = await fetch(request);
        
        // Cache API responses only for GET requests and specific endpoints
        if (request.method === 'GET' && API_CACHE_ENDPOINTS.some(endpoint => request.url.includes(endpoint))) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Return offline response for API
        return new Response(JSON.stringify({
            error: 'Offline',
            message: 'This content is not available offline'
        }), {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

// Handle static asset requests
async function handleStaticRequest(request) {
    // Only handle GET requests for caching
    if (request.method !== 'GET') {
        return fetch(request);
    }
    
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
        return cachedResponse;
    }
    
    try {
        const networkResponse = await fetch(request);
        // Only cache successful GET responses
        if (networkResponse.ok && request.method === 'GET') {
            const cache = await caches.open(STATIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        return cachedResponse || new Response('Network error', { status: 503 });
    }
}

// Background sync for form submissions
self.addEventListener('sync', event => {
    if (event.tag === 'contact-form-sync') {
        event.waitUntil(syncContactForm());
    }
});

// Sync contact form when back online
async function syncContactForm() {
    try {
        const cache = await caches.open(DYNAMIC_CACHE);
        const requests = await cache.keys();
        
        for (const request of requests) {
            if (request.url.includes('/contact') && request.method === 'POST') {
                try {
                    await fetch(request);
                    await cache.delete(request);
                    console.log('Service Worker: Contact form synced');
                } catch (error) {
                    console.log('Service Worker: Sync failed', error);
                }
            }
        }
    } catch (error) {
        console.log('Service Worker: Background sync failed', error);
    }
}

// Push notification handling
self.addEventListener('push', event => {
    const options = {
        body: event.data ? event.data.text() : 'New update available!',
        icon: '/static/assets/logo/logo.png',
        badge: '/static/assets/logo/logo.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'Explore',
                icon: '/static/assets/icons/checkmark.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/static/assets/icons/xmark.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('Lusan Sapkota Portfolio', options)
    );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('https://www.lusansapkota.com.np')
        );
    }
});

// Message event for skip waiting
self.addEventListener('message', event => {
    if (event.data && event.data.action === 'skipWaiting') {
        self.skipWaiting();
    }
});

// Message handling from main thread
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

console.log('Service Worker: Loaded successfully');

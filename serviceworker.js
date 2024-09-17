var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/',
    '/offline',
    'static/portal/img/icons/icon-72x72.png',
    'static/portal/img/icons/icon-96x96.png',
    'static/portal/img/icons/icon-128x128.png',
    'static/portal/img/icons/icon-144x144.png',
    'static/portal/img/icons/icon-152x152.png',
    'static/portal/img/icons/icon-192x192.png',
    'static/portal/img/icons/icon-384x384.png',
    'static/portal/img/icons/icon-512x512.png',
    '/static/portal/img/icons/splash-bportal-1242x2688.png',
    '/static/portal/img/icons/app-screenshot_476x744.png'
];

// Cache on install
self.addEventListener("install", event => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    );
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .then(async response => {
                    // const cache = await caches.open(staticCacheName);
                    // cache.put(event.request, response.clone());
                    return response;
                })
                .catch(async () => {
                    return caches.match('/');
                })
        );
    } else {
        event.respondWith(
            caches.match(event.request).then(response => {
                return response || fetch(event.request);
            }).catch(() => {
                return caches.match('/');
            })
        );
    }
});

const CACHE_NAME = 'byte-ai-v1';
const URLS_TO_CACHE = [
  '/',
  '/index.html'
];

// Install: Cache essential files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(URLS_TO_CACHE).catch(() => {
        // Gracefully handle missing files
        return Promise.resolve();
      });
    })
  );
  self.skipWaiting();
});

// Activate: Clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch: Network first, fall back to cache
self.addEventListener('fetch', event => {
  const { request } = event;

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // For Wikipedia API calls, use network first
  if (request.url.includes('wikipedia.org')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          if (response.ok) {
            // Cache successful API responses
            const cache = caches.open(CACHE_NAME).then(c => {
              c.put(request, response.clone());
            });
          }
          return response;
        })
        .catch(() => {
          // Fall back to cache if offline
          return caches.match(request);
        })
    );
    return;
  }

  // For everything else, try cache first, then network
  event.respondWith(
    caches.match(request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(request).then(response => {
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(request, responseToCache);
          });
          return response;
        });
      })
      .catch(() => {
        // Offline fallback
        return new Response('Offline - cached content not available', {
          status: 503,
          statusText: 'Service Unavailable',
          headers: new Headers({
            'Content-Type': 'text/plain'
          })
        });
      })
  );
});

// Handle messages from client
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

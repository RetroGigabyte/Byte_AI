const CACHE_NAME = 'byte-ai-v2.8';
const VERSION = '2.8.0';
const URLS_TO_CACHE = [
  '/',
  '/index.html'
];

// Install: Cache essential files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(URLS_TO_CACHE).catch(() => {
        return Promise.resolve();
      });
    })
  );
  self.skipWaiting();
});

// Activate: Clean up old caches and notify clients of update
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

  // Notify all clients about the update
  self.clients.matchAll().then(clients => {
    clients.forEach(client => {
      client.postMessage({
        type: 'UPDATE_AVAILABLE',
        version: VERSION
      });
    });
  });
});

// Fetch: Network first for Wikipedia, cache first for static
self.addEventListener('fetch', event => {
  const { request } = event;

  if (request.method !== 'GET') {
    return;
  }

  // Wikipedia API: Network first
  if (request.url.includes('wikipedia.org')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          if (response.ok) {
            caches.open(CACHE_NAME).then(c => {
              c.put(request, response.clone());
            });
          }
          return response;
        })
        .catch(() => {
          return caches.match(request);
        })
    );
    return;
  }

  // Static content: Cache first
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

// Check for updates periodically
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'CHECK_UPDATE') {
    checkForUpdate();
  }
});

function checkForUpdate() {
  fetch('/index.html', { cache: 'no-store' })
    .then(response => response.text())
    .then(html => {
      const versionMatch = html.match(/const APP_VERSION = ['"]([^'"]+)['"]/);
      if (versionMatch && versionMatch[1] !== VERSION) {
        // New version available, update the cache
        caches.open(CACHE_NAME).then(cache => {
          cache.add('/index.html');

          // Notify all clients
          self.clients.matchAll().then(clients => {
            clients.forEach(client => {
              client.postMessage({
                type: 'UPDATE_AVAILABLE',
                version: versionMatch[1]
              });
            });
          });
        });
      }
    })
    .catch(() => {
      // Offline, skip update check
    });
}

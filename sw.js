// Service Worker for Solus Core PWA (Genesis Gem That Thormilnus)
// This file is required for the "standalone" PWA mode to bypass protocol restrictions.

self.addEventListener('fetch', function(e) {
    // For a minimal terminal app, we simply let the network handle all requests.
    // GitHub Pages requires the SW file to exist for PWA installation to work.
    console.log('[SW] Fetching resource:', e.request.url);
});

self.addEventListener('install', (e) => {
    console.log('[SW] Installation successful.');
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    console.log('[SW] Activation successful.');
    e.waitUntil(clients.claim());
});

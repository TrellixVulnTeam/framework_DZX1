self.addEventListener("install", function () { self.skipWaiting() });
self.addEventListener("fetch", function () { e.respondWith(fetch(e.request))}); // FetchEvent
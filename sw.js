// R+ Study — Service Worker (PWA offline)
const CACHE = 'rplus-v2';
const PRECACHE = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './icon-180.png',
  'https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.js',
  'https://cdn.jsdelivr.net/npm/dexie@4/dist/dexie.min.js',
  'https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js',
  'https://www.gstatic.com/firebasejs/10.12.2/firebase-auth-compat.js',
  'https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.allSettled(PRECACHE.map(u => c.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return; // não intercepta POST (ex.: Firestore)

  // Documento/navegação: network-first (sempre mais novo online), cai pro cache offline
  if (req.mode === 'navigate' || req.destination === 'document') {
    e.respondWith(
      fetch(req)
        .then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put('./index.html', cp)); return r; })
        .catch(() => caches.match('./index.html').then(r => r || caches.match('./')))
    );
    return;
  }

  // Bibliotecas (CDN), ícones, etc.: cache-first, com atualização em segundo plano
  e.respondWith(
    caches.match(req).then(cached => {
      const network = fetch(req).then(r => {
        if (r && r.status === 200) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); }
        return r;
      }).catch(() => cached);
      return cached || network;
    })
  );
});

/* JARVIS: la app si apre anche senza rete (mostra l'ultima versione salvata).
   Prima prova la rete, poi la copia salvata. I dati del database non vengono salvati qui. */
const CACHE = "jarvis-v15";
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "../fonts/cinzel.woff", "../fonts/worksans.woff"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== CACHE).map(x => caches.delete(x)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  // sempre la versione più recente dal server (no-cache), la copia salvata solo senza rete
  e.respondWith(fetch(e.request, { cache: "no-cache" }).then(r => { if (r.ok) { const c = r.clone(); caches.open(CACHE).then(x => x.put(e.request, c)); } return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match("./index.html"))));
});

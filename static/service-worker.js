/**
 * Service Worker - Locutores IA PWA
 * Habilita funcionamento offline e cache
 */

const CACHE_NAME = 'locutores-ia-v1';
const STATIC_ASSETS = [
  '/',
  '/static/styles.css',
  '/static/script.js',
  '/static/voxcraft_integration.js',
  '/static/manifest.json',
  '/static/icon-192.png',
  '/static/icon-512.png'
];

// Instalação - cache assets estáticos
self.addEventListener('install', function(event) {
  console.log('[SW] Instalando Service Worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('[SW] Cache aberto');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(function() {
        return self.skipWaiting();
      })
  );
});

// Ativação - limpa caches antigos
self.addEventListener('activate', function(event) {
  console.log('[SW] Ativando Service Worker...');
  
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(cacheName) {
          return cacheName.startsWith('locutores-ia-') && cacheName !== CACHE_NAME;
        }).map(function(cacheName) {
          console.log('[SW] Deletando cache antigo:', cacheName);
          return caches.delete(cacheName);
        })
      );
    }).then(function() {
      return self.clients.claim();
    })
  );
});

// Fetch - estratégia Cache First, then Network
self.addEventListener('fetch', function(event) {
  const { request } = event;
  const url = new URL(request.url);
  
  // Ignora requisições para API (não cacheia)
  if (url.pathname.startsWith('/api/')) {
    return;
  }
  
  // Ignora requisições não GET
  if (request.method !== 'GET') {
    return;
  }
  
  event.respondWith(
    caches.match(request).then(function(cachedResponse) {
      // Retorna cache se existir
      if (cachedResponse) {
        // Atualiza cache em background
        fetch(request).then(function(networkResponse) {
          if (networkResponse.ok) {
            caches.open(CACHE_NAME).then(function(cache) {
              cache.put(request, networkResponse);
            });
          }
        }).catch(function() {
          // Falha silenciosa em background
        });
        
        return cachedResponse;
      }
      
      // Se não tem cache, busca na rede
      return fetch(request).then(function(networkResponse) {
        if (!networkResponse || networkResponse.status !== 200) {
          return networkResponse;
        }
        
        // Cacheia a resposta
        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(request, responseToCache);
        });
        
        return networkResponse;
      });
    }).catch(function(error) {
      console.log('[SW] Fetch falhou:', error);
      
      // Retorna página offline se existir
      if (request.destination === 'document') {
        return caches.match('/');
      }
      
      throw error;
    })
  );
});

// Mensagens do cliente
self.addEventListener('message', function(event) {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
});

console.log('[SW] Service Worker carregado!');

/**
 * Solus Core Interface - Service Worker (Full Version)
 * Version: 1.0.0
 */

const CACHE_NAME = 'solus-core-v1';

// รายการไฟล์ที่จะเก็บไว้ใช้งานแบบ Offline
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest_solus.webmanifest',
  'https://cdn.tailwindcss.com',
  'https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap'
];

// 1. Install Event: สร้าง Cache และเก็บไฟล์ที่จำเป็น
self.addEventListener('install', (event) => {
  console.log('[SW] Installing New Service Worker...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Pre-caching offline assets');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => self.skipWaiting()) // บังคับให้เริ่มทำงานทันทีไม่ต้องรอ
  );
});

// 2. Activate Event: ล้าง Cache เก่าที่ไม่ได้ใช้แล้ว (สำคัญมากเมื่อมีการอัปเดตเวอร์ชัน)
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating Service Worker...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log('[SW] Removing old cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim()) // ควบคุมหน้าเว็บทั้งหมดทันที
  );
});

// 3. Fetch Event: กลยุทธ์ "Cache First, Falling Back to Network"
// ตรวจสอบข้อมูลในแคชก่อน ถ้าไม่มีค่อยไปดึงจากอินเทอร์เน็ต
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // พบไฟล์ในแคช -> ส่งคืนไฟล์นั้น
        if (response) {
          return response;
        }

        // ไม่พบไฟล์ในแคช -> ไปดึงจาก Network
        return fetch(event.request).then((networkResponse) => {
          // ถ้าเป็น request ปกติ (ไม่ใช่ไฟล์ข้ามโดเมนที่ซับซ้อน) ให้เก็บลงแคชไว้ด้วย
          if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
            return networkResponse;
          }

          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });

          return networkResponse;
        });
      }).catch(() => {
        // กรณีออฟไลน์และไม่มีไฟล์ในแคช (เช่น หน้าเว็บที่ไม่ได้อยู่ในรายการ ASSETS)
        console.error('[SW] Fetch failed; user is offline and asset not cached.');
      })
  );
});
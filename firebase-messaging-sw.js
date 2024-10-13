// Import Firebase scripts for Firebase Cloud Messaging
importScripts('https://www.gstatic.com/firebasejs/9.1.3/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/9.1.3/firebase-messaging.js');

// Firebase-konfigurasjon - samme som du har i index.html
const firebaseConfig = {
  apiKey: 'DIN_FIREBASE_API_KEY',
  authDomain: 'DIN_FIREBASE_AUTH_DOMAIN',
  projectId: 'DIN_FIREBASE_PROJECT_ID',
  storageBucket: 'DIN_FIREBASE_STORAGE_BUCKET',
  messagingSenderId: 'DIN_FIREBASE_MESSAGING_SENDER_ID',
  appId: 'DIN_FIREBASE_APP_ID',
  measurementId: 'DIN_FIREBASE_MEASUREMENT_ID'
};

// Initialiser Firebase
firebase.initializeApp(firebaseConfig);

// Få tilgang til Firebase Cloud Messaging
const messaging = firebase.messaging();

// Lytt etter meldinger i bakgrunnen
messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Mottok bakgrunnsmelding: ', payload);

  // Tilpass varseltittel og alternativer basert på meldingen fra backend
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: '/firebase-logo.png'  // Sett din egen ikon her om ønskelig
  };

  // Vis varselet
  self.registration.showNotification(notificationTitle, notificationOptions);
});

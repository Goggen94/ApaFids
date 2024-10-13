// firebase-messaging-sw.js
importScripts('https://www.gstatic.com/firebasejs/9.1.3/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/9.1.3/firebase-messaging.js');

const firebaseConfig = {
    apiKey: "DIN_FIREBASE_API_KEY",
    authDomain: "DIN_FIREBASE_AUTH_DOMAIN",
    projectId: "DIN_FIREBASE_PROJECT_ID",
    storageBucket: "DIN_FIREBASE_STORAGE_BUCKET",
    messagingSenderId: "DIN_FIREBASE_MESSAGING_SENDER_ID",
    appId: "DIN_FIREBASE_APP_ID",
    measurementId: "DIN_FIREBASE_MEASUREMENT_ID"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

// Lytt etter bakgrunnsvarsler
messaging.onBackgroundMessage(function(payload) {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/firebase-logo.png'  // Sett til ikonet for nettsiden din eller en egen fil
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});

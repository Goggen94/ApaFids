importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging.js');

// Initialize Firebase in the service worker
const firebaseConfig = {
    apiKey: "AIzaSyDebqZBQtfPbR6Nx84HnfN6qLX7LrLMWJY",
    authDomain: "paxbot-2b8b2.firebaseapp.com",
    projectId: "paxbot-2b8b2",
    storageBucket: "paxbot-2b8b2.appspot.com",
    messagingSenderId: "315115333501",
    appId: "1:315115333501:web:f9503954d0b067fb2ece14",
    measurementId: "G-S0Y63P27KG"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

// Handle background messages
messaging.onBackgroundMessage(function(payload) {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/firebase-logo.png'
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});

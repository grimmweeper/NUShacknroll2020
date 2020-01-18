const admin = require('firebase-admin');

let serviceAccount = require('./schedulo-18432-621fa7d3e711.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

export let db = admin.firestore();



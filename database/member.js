import {db} from initialise.js;

function createCollection(db){
    // let docRef = db.ref('member/omnifarter');
    let docRef = db.collection('member').doc('grimweeper');

    let setAda = docRef.set({
    name: 'Weeping',
    emoji: '&#x1F971;',
    colour: '#00FF00'
    });
}
createCollection(db);
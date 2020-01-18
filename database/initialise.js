const admin = require('firebase-admin');
let serviceAccount = require('./schedulo-18432-621fa7d3e711.json');

function initialise() {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
  });
  
  let db = admin.firestore();
  return db;
}

function createCollection(db){
    // let docRef = db.ref('member/omnifarter');
    let docRef = db.collection('member').doc('grimweeper');

    let setAda = docRef.set({
    name: 'Weeping',
    emoji: '&#x1F971;',
    colour: '#00FF00'
    });
}

export function createBoard(db,boardName){
  let coll = db.collection(boardName);
  let todo = coll.doc("todo");
  let doing = coll.doc("doing");
  let done = coll.doc("done");

  let todoConfig = {
    title: "todo",
    color: "red",
    height: 300,
    width: 100,
    left: 200,
    top: 100,
    body: {
      msg1: "emoji",
      msg2: "emoji"
    }
  }

  let doingConfig = {
    title: "doing",
    color: "blue",
    height: 300,
    width: 100,
    left: 200,
    top: 100,
    body: {
      msg1: "emoji",
      msg2: "emoji"
    }
  }

  let doneConfig = {
    title: "done",
    color: "black",
    height: 300,
    width: 100,
    left: 200,
    top: 100,
    body: {
      msg1: "emoji",
      msg2: "emoji"
    }
  }

  todo.set(todoConfig);
  doing.set(doingConfig);
  done.set(doneConfig);
}

export function hello(){
  console.log("hello");
}

export {initialise,createCollection};


let db = initialise();

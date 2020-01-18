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

function initBoard(db,boardName){
  let coll = db.collection(boardName);

  // Setting sections document
  let sections = coll.doc("sections");

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

  sections.set({
    todo: todoConfig,
    doing: doingConfig,
    done: doneConfig
  });
  
  // creating other documents (empty for now)
  coll.doc("members").set({});
  coll.doc("agenda").set({});
}

function editDoc(coll,document,data){
  coll.document.set(data);
}

function readDoc(db,collName,docName) {
  return db.collection(collName).doc(docName).get();
}

function mainCall() {
  let db = initialise();
  // initBoard(db,"test2");
  let print = readDoc(db,"test2","members");
  console.log(print);
  return print;
}


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os import path
from flask import Flask, render_template, request

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, ".", ".", "schedulo-18432-621fa7d3e711.json"))

# Use a service account
cred = credentials.Certificate(filepath)

class DB:
    def __init__(self):
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    class Board:
        def __init__(self,outer_instance,board_name):
            self.outer_instance = outer_instance
            self.db = outer_instance.db
            coll = self.db.collection(board_name)

            sections = coll.document("sections")

            todoData = {
                "title": "todo",
                "color": "red",
                "height": 300,
                "width": 100,
                "left": 200,
                "top": 100,
                "body": {
                "msg1": "emoji",
                "msg2": "emoji"
                }
            }
            doingData = {
                "title": "doing",
                "color": "grey",
                "height": 300,
                "width": 100,
                "left": 200,
                "top": 100,
                "body": {
                "msg1": "emoji",
                "msg2": "emoji"
                }
            }
            doneData = {
                "title": "done",
                "color": "black",
                "height": 300,
                "width": 100,
                "left": 200,
                "top": 100,
                "body": {
                "msg1": "emoji",
                "msg2": "emoji"
                }
            }

            sections.set({
                "todo": todoData,
                "doing": doingData,
                "done": doneData
            })

            coll.document("members").set({})
            coll.document("agenda").set({})

db = DB()
board = db.Board(db,"test4")

app = Flask(__name__)

@app.route('/<boardID>/',methods=["GET,POST"])
def echo():
    if request.method == "POST":
        print(request.data)
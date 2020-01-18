import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os import path
# from flask import Flask, render_template, request

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, ".", ".", "schedulo-18432-621fa7d3e711.json"))

# Use a service account
cred = credentials.Certificate(filepath)

class DB:
    def __init__(self):
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def check_if_board_populated(self,board_name):
        docs = self.db.collection(board_name).stream()
        populated = False
        for doc in docs:
            populated = True
            break
        return populated

    class Board:
        def __init__(self,outer_instance,board_name):
            self.outer_instance = outer_instance
            self.db = outer_instance.db
            self.board = self.db.collection(board_name)

        def create_from_template(self):
            coll = self.board
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

        def read_document(self,document_name):
            return self.board.document(document_name).get().to_dict()

        def read_members(self):
            return self.read_document("members")

        def read_tasks(self):
            return self.read_document("sections")

        def write_document(self, document_name, data):
            self.board.document(document_name).set(data)

        def add_task(self, section_name, msg, emoji):
            data = self.read_tasks
            section = data[section_name]
            section[msg] = emoji
            self.write_document("sections", data)

        def add_member(self, handle, name, color="white", emoji):
            data = self.read_members()
            data[handle] = {
                'name': name,
                'color': color,
                'emoji': emoji
            }
            self.write_document("members", data)

# db = DB()
# print(db.check_if_board_populated("test4"))
#
# board = db.Board(db, "test4")
# data = board.read_document("sections")
# print(data['done']['body'])

# app = Flask(__name__)
#
# @app.route('/<boardID>/',methods=["GET,POST"])
# def echo():
#     if request.method == "POST":
#         print(request.data)
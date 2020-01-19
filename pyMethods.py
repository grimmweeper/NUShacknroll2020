#!/usr/bin/env python
# -*- coding: utf-8 -*-

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os import path
from flask import Flask, render_template, request
import json

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, ".", ".", "schedulo-18432-621fa7d3e711.json"))

# Use a service account
cred = credentials.Certificate(filepath)

class DB:
    def __init__(self):
        try: 
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        except:
            firebase_admin.get_app()
            self.db = firestore.client()

    def board_ref(self,board_name):
        return self.Board(self,board_name)


    class Board:
        def __init__(self,outer_instance,board_name):
            self.outer_instance = outer_instance
            self.db = outer_instance.db
            self.board = self.db.collection(board_name)

        def create_from_template(self):
            
            sections = self.board.document("sections")

            todoData = {
                "title": "todo",
                "color": "red",
                "height": "300px",
                "width": "100px",
                "left": "200px",
                "top": "100px",
                "body": {
                "msg1": "emoji",
                "msg2": "emoji"
                }
            }
            doingData = {
                "title": "doing",
                "color": "grey",
                "height": "300px",
                "width": "100px",
                "left": "200px",
                "top": "100px",
                "body": {
                "msg1": "emoji",
                "msg2": "emoji"
                }
            }
            doneData = {
                "title": "done",
                "color": "black",
                "height": "300px",
                "width": "100px",
                "left": "200px",
                "top": "100px",
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

            self.board.document("members").set({})
            self.board.document("agenda").set({})

        def read_document(self,document_name):
            return self.board.document(document_name).get().to_dict()

        def read_members(self):
            return self.read_document("members")

        def read_tasks(self):
            return self.read_document("sections")

        def write_document(self, document_name, data):
            self.board.document(document_name).set(data)

        def overwrite_sections(self,data):
            self.write_document("sections",data)

        def add_task(self, section_name, msg, emoji = ""):
            data = self.read_tasks()
            section = data[section_name]
            section[msg] = emoji
            self.write_document("sections", data)
            print(msg)

        def add_member(self, name, emoji, color="white"):
            data = self.read_members()
            data[name] = {
                'name': name,
                'color': color,
                'emoji': emoji
            }
            self.write_document("members", data)

        def delete_task(self, section_name, msg):
            data = self.read_tasks()
            section = data[section_name]
            del section[msg]
            self.write_document("sections", data)

        def move_task(self, section_from, section_to, msg):
            data = self.read_tasks()
            section_from = data[section_from]
            section_to = data[section_to]
            section_to[msg] = section_from[msg]

            del section_from[msg]

        def assign_task(self, section_name, msg, emoji):
            data = self.read_tasks()
            section = data[section_name]
            section[msg] = emoji

db2 = DB()
db = DB()
board = db.Board(db,"test3")
board.create_from_template()
# print(board.read_members())
# board.add_member("@hihithisisme","lexuan","smilely")
# print(board.read_members())
# print("=======================================================================")
# board.add_task("todo","HELLO THERE","frown")
# print(board.read_tasks())
# board.delete_task("todo","HELLO THERE")
# print(board.read_tasks())


app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def echo():
    if request.method == "POST":
        print("next is requesting data")
        data = request.get_data().decode("utf-8")
        print(data)
        board = DB().board_ref(data)
        print(board.read_document("sections"))
        return board.read_document("sections")
    else:
        return {"title": "To-Do","body":["lexy","gab","weepz"],"color":"red","height":"300px","width":"100px","left":"200px","top":"100px"}

@app.route('/addTask/',methods=["GET","POST"])
def update_sections_flask():
    if request.method == "POST":
        print("adding task now")
        data = json.loads(request.get_data().decode("utf-8"))
        print(data)
        board = DB().board_ref(data['board_name'])
        board.overwrite_sections(data['data'])
        print("added successfully")
    return None

@app.route('/index/',methods=["GET","POST"])
def ind():
    return render_template("main.html")


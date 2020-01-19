#!/usr/bin/env python
# -*- coding: utf-8 -*-

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from os import path
from flask import Flask, render_template, request,session, redirect
import json
import os

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

        def check_if_empty(self):
            docs = self.board.stream()
            empty = True
            for doc in docs:
                empty = False
            return empty

        def create_from_template(self):
            
            sections = self.board.document("sections")

            todoData = {
                "title": "todo",
                "color": "red",
                "height": "300px",
                "width": "100px",
                "left": "200px",
                "top": "100px",
                "body": {}
            }
            doingData = {
                "title": "doing",
                "color": "grey",
                "height": "300px",
                "width": "100px",
                "left": "200px",
                "top": "100px",
                "body": {}
            }
            doneData = {
                "title": "done",
                "color": "black",
                "height": "300px",
                "width": "100px",
                "left": "200px",
                "top": "100px",
                "body": {}
            }

            sections.set({
                "todo": todoData,
                "doing": doingData,
                "done": doneData
            })

            self.board.document("members").set({})
            self.board.document("pinned").set({})

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
            section_body = data[section_name]["body"]
            section_body[msg] = emoji
            self.write_document("sections", data)

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
            section_body = data[section_name]["body"]
            del section_body[msg]
            self.write_document("sections", data)

        def move_task(self, section_from, section_to, msg):
            data = self.read_tasks()
            section_from = data[section_from]["body"]
            section_to = data[section_to]["body"]
            section_to[msg] = section_from[msg]

            del section_from[msg]
            self.write_document("sections", data)


        def assign_task(self, section_name, msg, emoji):
            data = self.read_tasks()
            section_body = data[section_name]["body"]
            section_body[msg] = emoji
            self.write_document("sections", data)

        def read_pinned(self):
            return self.read_document("pinned")['data']

        def add_pinned(self,add_data):
            data = self.read_pinned()
            data.append(add_data)
            print(data)
            data_write = {'data':data}
            self.write_document("pinned",data_write)

        def del_pinned(self,del_msg):
            pinned = self.read_pinned()
            del pinned[pinned.index(del_msg)]
            data_write = {'data':pinned}
            self.write_document("pinned",data_write)
            

#db2 = DB()
db = DB()
board = db.Board(db,"test10")
board.move_task("todo","doing","hihinoticemesenpai!")
# print(board.read_pinned())
# board.add_pinned("hello there!!")
# board.del_pinned("msg2")
#board.create_from_template()
# print(board.read_members())
# board.add_member("@hihithisisme","lexuan","smilely")
# print(board.read_members())
# print("=======================================================================")
# board.add_task("todo","HELLO THERE","frown")
# print(board.read_tasks())
# board.delete_task("todo","HELLO THERE")
# print(board.read_tasks())



app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/',methods=["GET","POST"])
def echo():
    board = session['board']
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
    board = session['board']
    if request.method == "POST":
        print("adding task now")
        data = json.loads(request.get_data().decode("utf-8"))
        print(data)
        board = DB().board_ref(data['board_name'])
        board.overwrite_sections(data['data'])
        print("added successfully")
    return "hello"

@app.route('/index/',methods=["GET","POST"])
def ind():
    board_name = session['board']
    board = DB().board_ref(board_name)
    pinned_data = board.read_pinned()
    return render_template("main.html",board = board,pinned_data = pinned_data)

@app.route('/login/', methods=["GET","POST"])
def login():
    if request.method == "POST":
        print("posting info")
        db = DB()
        board = db.board_ref(board_name)
        if board.check_if_empty():
            board.create_from_template()
        session['board'] = board_name

        return redirect('/index/')

    return render_template("login.html")
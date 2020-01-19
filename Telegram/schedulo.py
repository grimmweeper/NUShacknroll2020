#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This bot manages projects through Telegram

It provides updates on how project members are working on different tasks of the projects, helps set meeting timings and agendas.
"""
import logging
import telegram
from pyMethods import DB

from telegram.error import NetworkError, Unauthorized
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler,PicklePersistence)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

update_id = None

PROJECT_NAME, MEMBERS,MEMBERS2, EMOJI, LAST_EMOJI, START_PROJECT = range(6)
user_data = dict()

def start(update, context):
    db = DB()
    user_data['board'] = db.Board(db, "test2")
    update.message.reply_text(
        "Hello! Let's start a project! What would you like to name this project?"
    )
    return PROJECT_NAME




def project_name(update, context):
    name = update.message.text
    logger.info("Project name: %s", name)
    update.message.reply_text(
        "Okay, Project " + name + " started!\n"
         "How many members do you have inside your project?",
    )

    return MEMBERS


def add_members(update, context):
    user_data['members'] = int(update.message.text)
    user_data['members_list'] = []
    user_data['emoji_list'] = []
    update.message.reply_text("Who's in the project?")
    return MEMBERS2

def add_members2(update,context):
    members_list = user_data.get('members_list')
    members_list.append(update.message.text)
    members = user_data.get('members') -1
    user_data['members'] = members
    update.message.reply_text("What is {}'s emoji?".format(members_list[-1]))
    if members>0:
        return EMOJI
    else:
        return START_PROJECT


def add_emoji(update,context):
    emoji_list = user_data.get('emoji_list')
    emoji_list.append(update.message.text)
    members_list = user_data.get('members_list')
    board = user_data['board'].add_member(name=members_list[-1], emoji=emoji_list[-1])
    update.message.reply_text("Alright! Who's the next members?")
    return MEMBERS2

def add_last_emoji(update,context):
    update.message.reply_text("What is {}'s emoji?".format(members_list[-1]))
    return START_PROJECT

def start_project(update, context):
    emoji_list = user_data.get('emoji_list')
    emoji_list.append(update.message.text)
    members_list = user_data.get('members_list')
    board = user_data['board'].add_member(name=members_list[-1], emoji=update.message.text)
    update.message.reply_text("Here's your project code: #1234\n")
    return -1

def show_tasks(update,context):
    data = user_data.get('board').read_tasks()
    reply_text = "*Doing*\n"
    doing = data['doing']['body']
    for x in doing :
        reply_text += x + ": " + doing.get(x)+ "\n"

    reply_text += "*Todo*\n"
    doing = data['todo']['body']
    for x in doing :
        reply_text += x + ": " + doing.get(x)+ "\n"
    reply_text += "\n"

    reply_text += "*Done*\n"
    doing = data['done']['body']
    for x in doing :
        reply_text += x + ": " + doing.get(x)+ "\n"
    update.message.reply_text(reply_text,ParseMode.MARKDOWN)
    reply_text += "\n"

def show_members(update,context):
    data = user_data.get('board').read_members()
    reply_text = ""
    for x in data:
        reply_text += x + ": "+ data.get(x)['emoji']+ "\n"

    update.message.reply_text(reply_text)

#def add_task(update,context):
    #nothning




def cancel(update, context):
    print("there was some problem")


def main():
    """Run the bot."""
    global update_id


    # Telegram Bot Authorization Token
    updater = Updater('941751379:AAELtiX3GIR_tvj1ibksOWa-a5dm6X8ZTJw', use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PROJECT_NAME: [MessageHandler(Filters.text, project_name)],
            MEMBERS: [MessageHandler(Filters.text, add_members)],
            MEMBERS2: [MessageHandler(Filters.text,add_members2)],
            EMOJI: [MessageHandler(Filters.text,add_emoji)],
            LAST_EMOJI: [MessageHandler(Filters.text,add_last_emoji)],
            START_PROJECT: [MessageHandler(None, start_project)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("showTasks", show_tasks))
    dp.add_handler(CommandHandler("showMembers", show_members))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

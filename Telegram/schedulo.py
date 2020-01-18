"""This bot manages projects through Telegram

It provides updates on how project members are working on different tasks of the projects, helps set meeting timings and agendas.
"""
import logging
import telegram
from database.pyMethods import DB

from telegram.error import NetworkError, Unauthorized
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler,PicklePersistence)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

update_id = None

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
PROJECT_NAME, MEMBERS,MEMBERS2, START_PROJECT = range(4)
user_data = dict()

def start(update, context):
    update.message.reply_text(
        "Hello! Let's start a project! What would you like to name this project?"
    )
    return PROJECT_NAME




def project_name(update, context):
    user = update.message.from_user
    name = update.message.text
    logger.info("Project name: %s", name)
    update.message.reply_text(
        "Okay, " + user.first_name + ", Project " + name + " started!\n"
         "How many members do you have inside your project?",
    )

    return MEMBERS


def add_members(update, context):
    user_data['members'] = int(update.message.text) -1
    user_data['members_list'] = []
    update.message.reply_text("Who's in the project?")
    return MEMBERS2

def add_members2(update,context):
    members_list = user_data.get('members_list')
    members_list.append(update.message.text)
    update.message.reply_text("Alright! Who's the next members?")
    members = user_data.get('members') -1
    user_data['members'] = members
    if members>0:
        return MEMBERS2
    else:
        return START_PROJECT

def start_project(update, context):
    update.message.reply_text("Here's your project code: #1234\n")
    db = DB()
    user_data['board'] = db.Board(db, "test4")
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
            MEMBERS2 : [MessageHandler(Filters.text,add_members2)],
            START_PROJECT: [MessageHandler(None, start_project)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("showTasks", show_tasks))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

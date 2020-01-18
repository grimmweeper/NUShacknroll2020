"""This bot manages projects through Telegram

It provides updates on how project members are working on different tasks of the projects, helps set meeting timings and agendas.
"""
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


update_id = None

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_NAME, MEMBERS, START_PROJECT = range(3)


def start(update,context):
    update.message.reply_text(
        "Hello! Let's start a project! What would you like to name this project?"
    )
    return PROJECT_NAME

def project_name(update,context):
    reply_keyboard = [['Join','Start Project']]
    user = update.message.from_user
    name =update.message.text
    logger.info("Project name: %s",name)
    update.message.reply_text(
        "Okay, " + user.first_name +", Project "+ name +" started!\n"
        "How many members do you have inside your project?",
        reply_markup =ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=False)
    )

    return MEMBERS




def add_members(update,context):
    member_list = []
    while True:
        user = update.message.from_user
        if update.message.text == "Join":
            if user.first_name not in member_list:
                print(user.first_name)
                member_list.append(user.first_name)
        elif update.message.text == "Start Project":
            print("Project Started")
            update.message.reply_text(
                "Here are your members: "+
                member_list)
            return START_PROJECT

def button(update,context):
    query = update.callback_query

    query.edit_message_text(text="Selected option: {}".format(query.user.first_name))

def start_project(update,context):
    update.message.reply_text("Project Started"

    )


def cancel(update,context):
    print("there was some problem")



def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    updater = Updater('941751379:AAELtiX3GIR_tvj1ibksOWa-a5dm6X8ZTJw',use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PROJECT_NAME: [MessageHandler(Filters.text,project_name)],
            MEMBERS: [MessageHandler(Filters.text, add_members)],
            START_PROJECT : [MessageHandler(None, start_project)]

        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)


    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()

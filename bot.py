from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from time import gmtime, strftime
import logging
import fincalc

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log')

token_file_path = 'token/token.txt'

with open(token_file_path) as token_file:
    token = token_file.read()


def main():
    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

def start(bot, update):
    reply_keyboard = [['Payment']]
    text_file_path = 'texts/start.txt'
    with open(text_file_path) as text_file:
        text = text_file.read()
    logging.info('User command: start')
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

# def talk_with_user(bot,update):
#     user_text1 = update.message.text
#     logging.info(user_text1)
#     update.message.reply_text(user_text1[::-1])

main()
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from time import gmtime, strftime
import logging
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log')

token = settings.TELEGRAM_API_KEY

def main():
    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

def start(bot, update):
    text = 'Bot started'
    logging.info('User command: start')
    update.message.reply_text(text)

# def talk_with_user(bot,update):
#     user_text1 = update.message.text
#     logging.info(user_text1)
#     update.message.reply_text(user_text1[::-1])

main()
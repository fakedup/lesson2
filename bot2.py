from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from time import gmtime, strftime
import logging
import settings  # тут токен
import ephem
from textwrap import dedent
import re
from collections import Counter

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log')

token = settings.TELEGRAM_API_KEY
START, FUNC_CHOICE = range(2)

def main():
    updater = Updater(token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],

        states = {
        FUNC_CHOICE:[   CommandHandler('wordcount', wordcount), 
                        CommandHandler('calc', calc),
                        RegexHandler(r'^(С|с)колько будет \w?', word_calc),
                        RegexHandler(r'^[Пп]олнолуние после (\d{4})/(\d{2})/(\d{2})', full_moon, pass_groups = True),
                        MessageHandler(Filters.text, unknown_message)
                    ]
        },
        fallbacks =  [CommandHandler('cancel', cancel)],

        allow_reentry = True
        )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

def start(bot, update):
    text = dedent('''
    Бот для второго занятия.
    Выполняет команды: /wordcount и /calc. 
    Также отвечает на строчные числовые вопросы и предсказывает полнолуние.''')
    update.message.reply_text(text)
    return FUNC_CHOICE

def cancel(bot, update):
    update.message.reply_text('Maybe next time.')
    return ConversationHandler.END

def wordcount(bot, update):
    '''
    Команда /wordcount считает сова в присланной фразе, заключенной в двойные кавычки.
    '''
    text = update.message.text
    if re.search(r'"[\w ]*"', text):
        update.message.reply_text ('{} words.'.format(len(re.findall(r'\w+', text))-1))
    else:
        update.message.reply_text('Enter /wordcount and text in double quotes pair (/wordcount "your text").')
    return FUNC_CHOICE

def calc(bot, update):
    '''
    Команда выполняет основные арифметические действия с числами, если прислать выражение вида 1+2=
    '''
    text = update.message.text
    expression = re.search (r'[0-9]+(\+|\-|\*|\/)[0-9]+=$', text)   
    if not expression:
        update.message.reply_text('Expression should be in the form: 2+2=')
    else:
        update.message.reply_text(str(eval(expression.group(0)[:-1])))
    return FUNC_CHOICE

def word_calc(bot, update):
    '''
    Dычисляет математические выражения с целыми числами от одного до десяти, заданные словами.
    Например, “сколько будет три минус два”
    '''
    text = update.message.text
    digits_ops_dict = {
    'один': '1',
    'два': '2',
    'три': '3',
    'четыре':'4',
    'пять':'5',
    'шесть':'6',
    'семь':'7',
    'восемь':'8',
    'девять':'9',
    'ноль':'0',
    'плюс':'+',
    'минус':'-',
    'разделить':'/',
    'делить':'/',
    'умножить':'*',
    'и':'.'
    }
    tokens = text.split()
    expression_list = []
    for word in tokens:
        if word in digits_ops_dict.keys():
            expression_list.append(digits_ops_dict[word])
    try:
        update.message.reply_text(str(eval(''.join(expression_list))))
    except ZeroDivisionError:
        update.message.reply_text('На ноль делить нельзя!')
    return FUNC_CHOICE

def full_moon(bot, update, groups):
    '''
    Отвечает на вопрос: Полнолуние после 2016/10/01
    '''
    datestring = '{}/{}/{}'.format(groups[0], groups[1], groups[2])
    update.message.reply_text(str(ephem.next_full_moon(datestring)))
    return FUNC_CHOICE

def unknown_message(bot, update):
    update.message.reply_text('Это я не понимаю.')
    return FUNC_CHOICE

if __name__ == '__main__':

    main()
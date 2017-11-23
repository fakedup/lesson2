'''
Установите модуль ephem
Добавьте в бота команду /planet, которая будет принимать на вход название планеты на английском.
При помощи условного оператора if и ephem.constellation научите бота отвечать, в каком созвездии сегодня находится планета.
'''
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from time import gmtime, strftime
import logging
import settings  # тут токен
import ephem
from textwrap import dedent

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log')

token = settings.TELEGRAM_API_KEY

PLANET_ENTER = 1  # константа для входа в функцию расчета

def main():
    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('planet', start_planet_enter)],

        states = {
        PLANET_ENTER: [MessageHandler(Filters.text, get_planet_constellation)]
        },

        fallbacks = [CommandHandler('cancel', cancel)],

        allow_reentry = True

        )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

def start(bot, update):
    text = dedent('''\
    This is astrology bot. It can say in which constellation there is any solar system planet.

    Enter command /planet to start computation.''')
    reply_keyboard = [['/planet']]  # кнопка, чтобы не вводить команду вручную
    logging.info('User command: start')
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)) #кнопка добавляется

def start_planet_enter(bot, update):
    text = 'Enter solar system planet name (except of Earth).'
    update.message.reply_text(text)
    return PLANET_ENTER

def cancel(bot, update):
    update.message.reply_text('Maybe next time.')
    return ConversationHandler.END

def get_planet_constellation(bot, update):
    planets = {
    'mercury': ephem.Mercury, 
    'venus': ephem.Venus,  
    'mars': ephem.Mars, 
    'jupiter': ephem.Jupiter, 
    'saturn': ephem.Saturn, 
    'uranus': ephem.Uranus, 
    'neptune': ephem.Neptune
    }
    planet_name = update.message.text
            
    if planet_name.lower() in planets.keys():
        planet = planets[planet_name.lower()]()  # создается объект по введенному названию планеты
        planet.compute()  # расчет положения в созвездии
        update.message.reply_text ('{} is now in {}.'.format(planet.name, ephem.constellation(planet)[1]))
        return ConversationHandler.END  # завершение диалога
    else:
        text = 'Please enter correct planet name (except of Earth) or /cancel.'
        update.message.reply_text(text)
        return PLANET_ENTER  # типа go to заново

if __name__ == '__main__':

    main()
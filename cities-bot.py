from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import logging
import settings  # тут токен
from textwrap import dedent

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log')

token = settings.TELEGRAM_API_KEY

GAME_TURN = 1

cities_file_path = 'texts/cities.txt'
prop_cities_file_path = 'texts/propose_cities.txt'

in_game_cities_lists = {}
in_game_letter_to_begin = {}
in_game_used_cities = {}

def main():
    updater = Updater(token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start, pass_user_data = True)],

        states = {
        GAME_TURN:   [   
                        MessageHandler(Filters.text, turn, pass_user_data = True)
                ]
        },
        fallbacks =  [CommandHandler('cancel', cancel, pass_user_data = True)],

        allow_reentry = True
        )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

def start(bot, update, user_data):
    cities_list = []
    with open(cities_file_path, 'r', encoding = 'UTF-8') as cities_file_obj:
        for ln in cities_file_obj:
            cities_list.append(ln.lower().rstrip())
    in_game_cities_lists[update.message.from_user.id] = cities_list[:]
    in_game_used_cities[update.message.from_user.id] = []
    in_game_letter_to_begin[update.message.from_user.id] = ''
    text = dedent('''
    Бот для игры в города.
    Называйте город.''')
    update.message.reply_text(text)
    return GAME_TURN

def turn(bot, update, user_data):
    print (in_game_cities_lists[update.message.from_user.id])
    user_city_attempt = update.message.text.lower()  # city that user calls
    if user_city_attempt in in_game_used_cities[update.message.from_user.id]:  # list of cities used in this game (with this user)
        update.message.reply_text ('Такой город уже был!')
        return GAME_TURN
    elif in_game_letter_to_begin[update.message.from_user.id] and user_city_attempt[0] != in_game_letter_to_begin[update.message.from_user.id]:  # if it's wrong first leter
        update.message.reply_text (
        'Неправильно! Нужно называть город, который начинается на {}.'
        .format(in_game_letter_to_begin[update.message.from_user.id])
        )
        return GAME_TURN
    elif user_city_attempt not in in_game_cities_lists[update.message.from_user.id]:  # if it's unknown city
        update.message.reply_text ('Это какой-то неизвестный город!')
        return GAME_TURN
    else:
        update.message.reply_text ('Принято.')
        in_game_cities_lists[update.message.from_user.id].remove(user_city_attempt)
        in_game_used_cities[update.message.from_user.id].append(user_city_attempt)
        for city_element in in_game_cities_lists[update.message.from_user.id]:
            if city_element[0] == user_city_attempt[-1]:
                in_game_cities_lists[update.message.from_user.id].remove(city_element)
                in_game_used_cities[update.message.from_user.id].append(city_element)
                in_game_letter_to_begin[update.message.from_user.id] = city_element[-1]
                update.message.reply_text(city_element.capitalize())
                return GAME_TURN
        else:
            update.message.reply_text('Ты победил, я не знаю больше городов!')
            del in_game_letter_to_begin[update.message.from_user.id]
            del in_game_used_cities[update.message.from_user.id]
            del in_game_cities_lists[update.message.from_user.id]
            return ConversationHandler.END


def cancel(bot, update, user_data):
    del in_game_letter_to_begin[update.message.from_user.id]
    del in_game_used_cities[update.message.from_user.id]
    del in_game_cities_lists[update.message.from_user.id]
    update.message.reply_text('Good luck.')
    return ConversationHandler.END



if __name__ == '__main__':

    main()
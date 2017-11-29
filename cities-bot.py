from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import logging
import settings  # тут токен
from textwrap import dedent

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log')

token = settings.TELEGRAM_API_KEY

# constant to define conversation state
GAME_TURN = 1

cities_file_path = 'texts/cities.txt'
# prop_cities_file_path = 'texts/propose_cities.txt'

# dict to hold cities, used cities and letter to begin for different bot users
in_game_states = {}

def load_cities(file_path):
    """
    Function to load cities list from file once before the main func
    """
    cities_list = []
    with open(file_path, 'r', encoding = 'UTF-8') as cities_file_obj:
        for ln in cities_file_obj:
            # read from file in low register without new lines
            cities_list.append(ln.lower().rstrip())
    return cities_list

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
    """
    Initiate lists of known cities, used cities and letter for user to call city
    """
    in_game_states[update.message.from_user.id] = {
        'letter_to_begin' : '',
        'used_cities' : [],
        'remaining_cities' : common_cities_for_all[:]
    }
    text = dedent('''
    Бот для игры в города.
    Называйте город.''')
    update.message.reply_text(text)
    return GAME_TURN

def turn(bot, update, user_data):
    """
    Game turn: if user's city is suitable, call another city from list
    """
    # city that user calls
    user_city_attempt = update.message.text.lower()
    uid = update.message.from_user.id
    used_cities = in_game_states[uid]['used_cities']
    letter_to_begin = in_game_states[uid]['letter_to_begin']
    remaining_cities = in_game_states[uid]['remaining_cities']
    # check the list of cities used in this game (with this user)
    if user_city_attempt in used_cities:
        update.message.reply_text ('Такой город уже был!')
        return GAME_TURN
    # check if it's wrong first leter
    elif letter_to_begin and user_city_attempt[0] != letter_to_begin:
        update.message.reply_text (
        'Неправильно! Нужно называть город, который начинается на {}.'
        .format(letter_to_begin)
        )
        return GAME_TURN
    # check if it's unknown city
    elif user_city_attempt not in remaining_cities:
        update.message.reply_text ('Это какой-то неизвестный город!')
        return GAME_TURN
    else:
        update.message.reply_text ('Принято.')
        accept_city (uid, user_city_attempt)
        # check the list for new city
        for city_element in remaining_cities:
            if city_element[0] == user_city_attempt[-1]:
                accept_city (uid, city_element)
                letter_to_begin = city_element[-1]
                update.message.reply_text(city_element.capitalize())
                # exit from loop without else block run
                return GAME_TURN
        else:
            update.message.reply_text('Ты победил, я не знаю больше городов!')
            del in_game_states[uid]  # clear dict for this user to free memory
            return ConversationHandler.END

def accept_city (user_id, city):
    in_game_states[user_id]['remaining_cities'].remove(city)
    in_game_states[user_id]['used_cities'].append(city)


def cancel(bot, update, user_data):
    del in_game_states[update.message.from_user.id]  # clear dict to free memory
    update.message.reply_text('Good luck.')
    return ConversationHandler.END



if __name__ == '__main__':

    common_cities_for_all = load_cities(cities_file_path)
    main()
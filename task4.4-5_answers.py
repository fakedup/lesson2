'''
При помощи функции get_answer() отвечать на вопросы пользователя в ask_user(), пока он не скажет “Пока!”

Переписать функцию ask_user(), добавив обработку exception-ов
Добавить перехват ctrl+C и прощание
'''


from random import randint
from json import load

ANSWERS_FILE = 'answers.json'

with open(ANSWERS_FILE) as a_file:
  answers = load(a_file)

def get_answer(question, answers = answers):
  answers_list = answers.get(question.lower())
  try:
    answer = answers_list[randint(0,len(answers_list)-1)]
  except IndexError:
    answer = 'Я тебя не понимаю'
  return answer


def ask_user():
    user_answer=''
    while user_answer!='Пока!':
        try:
            user_answer = input('Bot: Ну что?\n')
            print ('Bot:',get_answer(user_answer))
        except KeyboardInterrupt:
            print (get_answer('Пока!'))
            break

ask_user()
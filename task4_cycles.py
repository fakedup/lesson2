#task 4.1 + 4.2
names = ["Вася", "Валера", "Маша", "Петя", "Саша", "Даша"]
name_to_search = "Валера"

def search_name_in_list (name_to_search, names):
	while name_to_search in names and len(names)>0:
		current_name = names.pop()
		if current_name == name_to_search:
			print (current_name, "нашелся!")
		else:
			print ('Это не', name_to_search)

search_name_in_list (name_to_search, names)

#task 4.3
def ask_user():
	user_answer=''
	while user_answer!='Хорошо':
		user_answer = input('Как дела?\n')

ask_user()
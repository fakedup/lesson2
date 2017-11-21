'''
Сравнение строк

Написать функцию, которая принимает на вход две строки.
Если строки одинаковые, возвращает 1.
Если строки разные и первая длиннее, возвращает 2.
Если строки разные и вторая строка 'learn', возвращает 3.
'''

def string_comparison(string1, string2):
	if string1 == string2:
		return 1
	elif len(string1) > len(string2):
		return 2
	elif string2 == 'learn':
		return 3
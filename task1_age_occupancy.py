'''
Попросить пользователя ввести возраст.
По возрасту определить, чем он должен заниматься: учиться в детском саду, школе, ВУЗе или работать.
Вывести занятие на экран.
'''

user_age = int(input('Enter your age: '))

if user_age < 0:
	print ('Еще не родился')
elif user_age < 7:
	print ('Детский сад')
elif user_age < 18:
	print ('Школа')
elif user_age <23:
	print ('Университет')
else:
	print ('Раобта')
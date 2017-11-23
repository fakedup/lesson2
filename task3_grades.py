'''
Оценки

Создать список с оценками учеников разных классов школы вида [{'school_class': '4a', 'scores': [3,4,4,5,2]}, ...]
Посчитать и вывести средний балл по всей школе.
Посчитать и вывести средний балл по каждому классу.
'''


school_journal = [
{'school_class': '4а', 'scores': [5,5,5,5,5]}, 
{'school_class': '4б', 'scores': [3,4,4,5,2]},
{'school_class': '4в', 'scores': [3,4,4,5,2]},
{'school_class': '5а', 'scores': [5,4,5,5,2]},
{'school_class': '5б', 'scores': [3,4,3,5,2]},
{'school_class': '5г', 'scores': [3,3,2,5,4]}
]

all_grades_sum = 0
all_grades_count = 0

for class_journal in school_journal:
    all_grades_sum += sum(class_journal['scores'])
    all_grades_count += len(class_journal['scores'])
    current_class = class_journal['school_class']
    current_class_avg_grade = sum(class_journal['scores'])/len(class_journal['scores'])
    print ('Средний балл {0} класса: {1:.3}'.format(current_class, current_class_avg_grade))
else:
    print ('Средний балл в школе: {:.3}'.format(all_grades_sum/all_grades_count))
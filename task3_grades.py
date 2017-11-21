school_journal = [ \
{'school_class': '4а', 'scores': [5,5,5,5,5]}, 
{'school_class': '4б', 'scores': [3,4,4,5,2]},
{'school_class': '4в', 'scores': [3,4,4,5,2]},
{'school_class': '5а', 'scores': [5,4,5,5,2]},
{'school_class': '5б', 'scores': [3,4,3,5,2]},
{'school_class': '5г', 'scores': [3,3,2,5,4]}
]

all_grades = []

for class_journal in school_journal:
    all_grades += class_journal['scores']
    current_class = class_journal['school_class']
    current_class_avg_grade = sum(class_journal['scores'])/len(class_journal['scores'])
    print ('Средний балл {0} класса: {1:.3}'.format(current_class, current_class_avg_grade))
else:
    print ('Средний балл в школе: {:.3}'.format(sum(all_grades)/len(all_grades)))
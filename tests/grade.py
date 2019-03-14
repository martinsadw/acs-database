import numpy as np
import matplotlib.pyplot as plt

from database.read import open_students, open_suggestions, open_grades
from database.students import get_students_index, get_students_suggestions, get_students_grades, get_distances_matrix
from utils.misc import grade_distance


##PARAMS########################################################################
subject = 8
################################################################################


students_db = open_students()
suggestions_db = open_suggestions()
grades_db = open_grades()

students_index = get_students_index(students_db, filter_group=1)

students_suggestions = get_students_suggestions(subject, students_index, suggestions_db)
students_grades = get_students_grades(subject, students_index, grades_db)

filtered_grades = students_grades[~students_grades.mask]

grades_distance = get_distances_matrix(filtered_grades, grade_distance)

################################################################################

fig = plt.figure()
# fig.suptitle('Diferença de nota - Disciplina %d' % (disciplina))
fig.suptitle('Nota dos alunos - Disciplina %d' % (subject))
ax = fig.add_subplot(111)
cmap = ax.imshow(grades_distance, interpolation='nearest', origin='lowest', cmap='gray', vmin=0, vmax=1)
plt.show()

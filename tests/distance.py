import numpy as np
import matplotlib.pyplot as plt

from database.read import open_students, open_suggestions, open_grades
from database.students import get_students_index, get_students_suggestions, get_distances_matrix
from utils.misc import hamming_distance, cosine_distance


##PARAMS########################################################################
subject = 8
distance_metric = 'cosine'
################################################################################


students_db = open_students()
suggestions_db = open_suggestions()

students_index = get_students_index(students_db, filter_group=1)

students_suggestions = get_students_suggestions(subject, students_index, suggestions_db)

if distance_metric == 'hamming':
    suggestions_distances = get_distances_matrix(students_suggestions, hamming_distance)
elif distance_metric == 'cosine':
    suggestions_distances = get_distances_matrix(students_suggestions, cosine_distance)

################################################################################

fig = plt.figure()
if distance_metric == 'hamming':
    fig.suptitle('Distância de hamming - Disciplina %d' % (subject))
elif distance_metric == 'cosine':
    fig.suptitle('Distância do cosseno - Disciplina %d' % (subject))
ax = fig.add_subplot(111)
cmap = ax.imshow(suggestions_distances, interpolation='nearest', origin='lowest', cmap='gray', vmin=0)
plt.show()

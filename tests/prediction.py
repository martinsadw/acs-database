import numpy as np
import matplotlib.pyplot as plt

from database.read import open_students, open_suggestions, open_grades
from database.students import get_students_index, get_students_id, get_students_suggestions, get_students_grades, get_distances_matrix, get_grades_prediction, DEBUG_get_grades_prediction
from utils.misc import hamming_distance, cosine_distance, array_interleave
from utils.output import save_csv


##PARAMS########################################################################
subject = 8
distance_name = 'hamming'
folder_name = 'results/2019-03-14 - Previsão de nota'
################################################################################
if distance_name == 'hamming':
    distance_show_name = 'Hamming'
    distance_function = hamming_distance
elif distance_name == 'cosine':
    distance_show_name = 'Cosseno'
    distance_function = cosine_distance
################################################################################

students_db = open_students()
suggestions_db = open_suggestions()
grades_db = open_grades()

students_index = get_students_index(students_db, filter_group=1)
students_id = get_students_id(students_index)

students_suggestions = get_students_suggestions(subject, students_index, suggestions_db)
students_grades = get_students_grades(subject, students_index, grades_db)

suggestions_distances = get_distances_matrix(students_suggestions, distance_function)

filtered_distances = suggestions_distances[~students_grades.mask][:, ~students_grades.mask]
filtered_grades = students_grades[~students_grades.mask]
filtered_id = students_id[~students_grades.mask]

grades_prediction = get_grades_prediction(filtered_grades, filtered_distances)

grades_diference = np.abs(grades_prediction - filtered_grades)

################################################################################

sort_values = np.argsort(filtered_grades)
# sort_values = np.arange(filtered_grades.shape[0])
sorted_grades = filtered_grades[sort_values]
sorted_prediction = grades_prediction[sort_values]
sorted_similarity = grades_diference[sort_values]

fig = plt.figure()
fig.suptitle('Diferença de nota - %s - Disciplina %d' % (distance_show_name, subject))
plt.ylim(0, 1)
plt.plot(sorted_similarity, color='r', label="Similaridade")
# plt.plot(sorted_prediction, color='r', label="Previsão")
# plt.plot(sorted_grades, color='g', label="Notas")
plt.plot(np.full(grades_diference.shape, grades_diference.mean()), color='b', linewidth=0.5, label="Média de similaridade")
plt.legend(loc=1)
plt.savefig(folder_name + "/prediction_%s_%d.png" % (distance_name, subject))
plt.show()

(DEBUG_grades_prediction, DEBUG_students_distance, DEBUG_students_id) = DEBUG_get_grades_prediction(filtered_grades, filtered_distances, filtered_id)
DEBUG_students = array_interleave((DEBUG_students_id, DEBUG_grades_prediction, DEBUG_students_distance), axis=1)

DEBUG_print = np.concatenate([filtered_id[..., np.newaxis], filtered_grades[..., np.newaxis], DEBUG_students, grades_prediction[..., np.newaxis], grades_diference[..., np.newaxis]], axis=1)
save_csv(folder_name + "/prediction_%s_%d.csv" % (distance_name, subject), DEBUG_print)

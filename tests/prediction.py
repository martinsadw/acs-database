import numpy as np
import matplotlib.pyplot as plt

from database.read import open_students, open_suggestions, open_grades
from database.students import get_students_index, get_students_suggestions, get_students_grades, get_distances_matrix, get_grades_prediction
from utils.misc import hamming_distance, cosine_distance


##PARAMS########################################################################
subject = 8
distance_metric = 'cosine'
################################################################################


students_db = open_students()
suggestions_db = open_suggestions()
grades_db = open_grades()

students_index = get_students_index(students_db, filter_group=1)

students_suggestions = get_students_suggestions(subject, students_index, suggestions_db)
students_grades = get_students_grades(subject, students_index, grades_db)

if distance_metric == 'hamming':
    suggestions_distances = get_distances_matrix(students_suggestions, hamming_distance)
elif distance_metric == 'cosine':
    suggestions_distances = get_distances_matrix(students_suggestions, cosine_distance)

filtered_distances = suggestions_distances[~students_grades.mask][:, ~students_grades.mask]
filtered_grades = students_grades[~students_grades.mask]

grades_prediction = get_grades_prediction(filtered_grades, filtered_distances)

grades_similarity = np.abs(grades_prediction - filtered_grades)

################################################################################

sort_values = np.argsort(filtered_grades)
# sort_values = np.arange(filtered_grades.shape[0])
sorted_grades = filtered_grades[sort_values]
sorted_prediction = grades_prediction[sort_values]
sorted_similarity = grades_similarity[sort_values]


fig = plt.figure()
fig.suptitle('Diferença de nota - Disciplina %d' % (subject))
plt.ylim(0, 1)
plt.plot(sorted_similarity, color='r', label="Similaridade")
# plt.plot(sorted_prediction, color='r', label="Previsão")
# plt.plot(sorted_grades, color='g', label="Notas")
plt.plot(np.full(grades_similarity.shape, grades_similarity.mean()), color='b', linewidth=0.5, label="Média de similaridade")
plt.legend(loc=1)
plt.show()

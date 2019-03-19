import numpy as np
import matplotlib.pyplot as plt

from database.read import open_students, open_suggestions, open_grades, open_abilities, open_styles
from database.students import get_students_index, get_students_id
from database.filters import filter_students_by_id, filter_students_by_style
from database.get_data import get_students_suggestions, get_students_abilities, get_students_grades, get_students_styles
from database.process_data import get_distances_matrix, get_grades_prediction, DEBUG_get_grades_prediction

from utils.misc import hamming_distance, cosine_distance, array_interleave
from utils.output import save_csv


##PARAMS########################################################################
subject = 1
distance_name = 'cosine'  # ['cosine', 'hamming']
value_used = 'grade'  # ['grade', 'ability', 'improvement']
# style_filter = None
style_filter = ['glo']  # None, ['ati', 'ref', 'sem', 'int', 'vis', 'ver', 'seq', 'glo']
folder_name = 'results/2019-03-19 - Previsão de nota por estilo'
################################################################################
if distance_name == 'hamming':
    distance_show_name = 'Hamming'
    distance_function = hamming_distance
elif distance_name == 'cosine':
    distance_show_name = 'Cosseno'
    distance_function = cosine_distance

if value_used == 'grade':
    value_show_name = 'Diferença de nota'
elif value_used == 'ability':
    value_show_name = 'Diferença de habilidade'
elif value_used == 'improvement':
    value_show_name = 'Diferença de melhoria'

if style_filter is None:
    filter_show_name = ''
    filter_file = 'all'
else:
    filter_show_name = ' - (' + ' | '.join(style_filter) + ')'
    filter_file = ';'.join(style_filter)
################################################################################


students_db = open_students()
suggestions_db = open_suggestions()
grades_db = open_grades()
abilities_db = open_abilities()
styles_db = open_styles()

# Obtem um dicionário com todos os alunos
students_index = get_students_index(students_db, filter_group=1)

# Filtra os alunos utilizando o estilo de aprendizado
students_styles = get_students_styles(students_index, styles_db)
students_index = filter_students_by_style(students_index, students_styles, style_filter)
students_id = get_students_id(students_index)

# Obtem uma lista de sugestões, notas e habilidades de cada aluno
students_suggestions = get_students_suggestions(subject, students_index, suggestions_db)
students_grades = get_students_grades(subject, students_index, grades_db)
students_abilities = get_students_abilities(subject, students_index, abilities_db)

# Calcula a distância entre cada aluno utilizando os materiais sugeridos
suggestions_distances = get_distances_matrix(students_suggestions, distance_function)

# Remove os alunos que não possuem notas
filtered_distances = suggestions_distances[~students_grades.mask][:, ~students_grades.mask]
filtered_grades = students_grades[~students_grades.mask]
filtered_abilities = students_abilities[~students_grades.mask]
filtered_id = students_id[~students_grades.mask]

if value_used == 'grade':
    students_values = filtered_grades
elif value_used == 'ability':
    students_values = filtered_abilities
elif value_used == 'improvement':
    students_values = filtered_grades - filtered_abilities

# Calcula a previsão do valor utilizado
grades_prediction = get_grades_prediction(students_values, filtered_distances)

grades_difference = np.abs(grades_prediction - students_values)

################################################################################

sort_values = np.argsort(students_values)
# sort_values = np.arange(filtered_grades.shape[0])
sorted_values = students_values[sort_values]
sorted_prediction = grades_prediction[sort_values]
sorted_difference = grades_difference[sort_values]

print(students_id)
sorted_ids = students_id[sort_values]
print(sorted_difference.mean()*2)
print(sorted_ids[sorted_difference > sorted_difference.mean()*2])


fig = plt.figure()
fig.suptitle('%s - %s - Disciplina %d%s' % (value_show_name, distance_show_name, subject, filter_show_name))
plt.ylim(0, 1)
plt.plot(sorted_difference, color='r', label="Similaridade")
# plt.plot(sorted_prediction, color='r', label="Previsão")
# plt.plot(sorted_values, color='g', label="Notas")
plt.plot(np.full(grades_difference.shape, grades_difference.mean()), color='b', linewidth=0.5, label="Média de similaridade")
plt.legend(loc=1)
plt.savefig(folder_name + "/prediction_%d_%s_%s_%s.png" % (subject, value_used, filter_file, distance_name))
# plt.show()

# (DEBUG_grades_prediction, DEBUG_students_distance, DEBUG_students_id) = DEBUG_get_grades_prediction(students_values, filtered_distances, filtered_id)
# DEBUG_students = array_interleave((DEBUG_students_id, DEBUG_grades_prediction, DEBUG_students_distance), axis=1)
#
# DEBUG_print = np.concatenate([filtered_id[..., np.newaxis], filtered_grades[..., np.newaxis], DEBUG_students, grades_prediction[..., np.newaxis], grades_difference[..., np.newaxis]], axis=1)
# save_csv(folder_name + "/prediction_%d_%s_%s_%s.csv" % (subject, value_used, filter_file, distance_name), DEBUG_print)

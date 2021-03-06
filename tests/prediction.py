import os

import numpy as np
import matplotlib.pyplot as plt

from database.read import open_students, open_suggestions, open_grades, open_abilities, open_styles
from database.students import get_students_index, get_students_id
from database.filters import filter_students_by_id, filter_students_by_style
from database.get_data import get_students_suggestions, get_students_abilities, get_students_grades, get_students_styles
from database.process_data import get_distances_matrix, get_grades_prediction, get_grades_regression, DEBUG_get_grades_prediction

from utils.misc import hamming_distance, cosine_distance, array_interleave
from utils.output import save_csv


##PARAMS########################################################################
base_path = 'results/2019-04-12 - Similaridade de materiais/'

graphic_type = 'scatter'  # ['scatter', 'difference', 'values', 'none']
graphic_save = True
graphic_show = False
graphics_folder_name = base_path + 'graphics'

csv_type = 'values'  # ['values', 'none']
csv_folder_name = base_path + 'csv'
################################################################################


def prediction(subject, distance_name, prediction_type, value_used, style_filter, out_info=None):
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

    if not style_filter:
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

    # max_materials = 30
    # # materials_distances = get_distances_matrix(students_suggestions.T, hamming_distance)
    # # materials_distances = get_distances_matrix(students_suggestions.T, cosine_distance)
    # # materials_distances = get_distances_matrix(students_suggestions.T, lambda a, b: np.logical_and(a, b).sum())
    # materials_distances = get_distances_matrix(students_suggestions.T, lambda a, b: (a != b).sum())
    # np.fill_diagonal(materials_distances, 0)
    # for i in range(students_suggestions.shape[1] - max_materials):
    #     max_index = np.unravel_index(np.argmax(materials_distances), materials_distances.shape)
    #     materials_distances = np.delete(materials_distances, max_index[0], axis=0)
    #     materials_distances = np.delete(materials_distances, max_index[0], axis=1)
    #     students_suggestions = np.delete(students_suggestions, max_index[0], axis=1)

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
    if prediction_type in ('kneighbors', 'gradient'):
        filtered_suggestions = students_suggestions[~students_grades.mask]
        grades_prediction = get_grades_regression(filtered_suggestions, students_values, regressor_name=prediction_type)
    else:
        grades_prediction = get_grades_prediction(students_values, filtered_distances, prediction_type=prediction_type)
    # grades_prediction = get_grades_prediction(students_values, filtered_distances, prediction_type=prediction_type)

    grades_difference = np.abs(grades_prediction - students_values)

    ################################################################################

    sort_values = np.argsort(students_values)
    # sort_values = np.arange(filtered_grades.shape[0])
    sorted_values = students_values[sort_values]
    sorted_prediction = grades_prediction[sort_values]
    sorted_difference = grades_difference[sort_values]

    values_correlation = np.corrcoef(sorted_values, sorted_prediction)[1, 0]
    values_mean = grades_difference.mean()
    values_error = (grades_difference ** 2).mean()

    if out_info is not None:
        out_info['quant_students'] = len(grades_difference)
        out_info['correlation'] = values_correlation
        out_info['mean_difference'] = values_mean
        out_info['error'] = values_error
        out_info['mean_ability'] = np.mean(filtered_abilities)
        out_info['deviation_ability'] = np.std(filtered_abilities)
        out_info['mean_grade'] = np.mean(filtered_grades)
        out_info['deviation_grade'] = np.std(filtered_grades)
        out_info['mean_prediction'] = np.mean(grades_prediction)
        out_info['deviation_prediction'] = np.std(grades_prediction)

    if graphic_type in ['scatter', 'difference', 'values']:
        fig = plt.figure()
        fig.suptitle('%s - %s - %s - Disciplina %d%s' % (value_show_name, distance_show_name, prediction_type, subject, filter_show_name))
        ax = fig.add_subplot(111)

        if graphic_type == 'scatter':
            if value_used == 'improvement':
                plt.ylim(-1, 1)
                plt.xlim(-1, 1)
            else:
                plt.ylim(0, 1)
                plt.xlim(0, 1)

            ax.set_xlabel('Notas')
            ax.set_ylabel('Previsões')
            plt.scatter(sorted_values, sorted_prediction, color='r', s=20)
        elif graphic_type == 'difference':
            plt.ylim(0, 1)
            plt.plot(sorted_difference, color='r', label="Similaridade")
            plt.plot(np.full(grades_difference.shape, grades_difference.mean()), color='b', linewidth=0.5, label="Média de similaridade")
            plt.legend(loc=1)
        elif graphic_type == 'values':
            plt.ylim(0, 1)
            plt.plot(sorted_prediction, color='r', label="Previsão")
            plt.plot(sorted_values, color='g', label="Notas")
            plt.plot(np.full(grades_difference.shape, grades_difference.mean()), color='b', linewidth=0.5, label="Média de similaridade")
            plt.legend(loc=1)

        if graphic_save:
            plt.savefig(graphics_folder_name + "/prediction_%s_%s_%s_%s_%s_%d.png" % (value_used, filter_file, distance_name, prediction_type, graphic_type, subject))
        if graphic_show:
            plt.show()

        plt.close()

    if csv_type in ['values']:
        (DEBUG_grades_prediction, DEBUG_students_distance, DEBUG_students_id) = DEBUG_get_grades_prediction(students_values, filtered_distances, filtered_id)
        DEBUG_students = array_interleave((DEBUG_students_id, DEBUG_grades_prediction, DEBUG_students_distance), axis=1)

        DEBUG_print = np.concatenate([filtered_id[..., np.newaxis], filtered_grades[..., np.newaxis], DEBUG_students, grades_prediction[..., np.newaxis], grades_difference[..., np.newaxis]], axis=1)
        save_csv(csv_folder_name + "/prediction_%s_%s_%s_%s_%s_%d.csv" % (value_used, filter_file, distance_name, prediction_type, csv_type, subject), DEBUG_print)


# tests_subject = [1, 2, 4, 5, 7, 8]
# tests_distance_name = ['cosine', 'hamming']
# tests_value_used = ['grade', 'ability', 'improvement']
# tests_style_filter = [[], ['ati'], ['ref'], ['sem'], ['int'], ['vis'], ['ver'], ['seq'], ['glo']]
# tests_prediction_type = ['uniform', 'distance', 'kneighbors', 'gradient']

tests_subject = [1, 2, 4, 5, 7, 8]
tests_distance_name = ['cosine']
tests_value_used = ['grade', 'improvement']
tests_style_filter = [[], ['ati'], ['ref'], ['sem'], ['int'], ['vis'], ['ver'], ['seq'], ['glo']]
tests_prediction_type = ['uniform', 'distance', 'kneighbors', 'gradient']

# tests_subject = [1, 2, 4, 5, 7, 8]
# tests_distance_name = ['cosine']
# tests_value_used = ['improvement']
# tests_style_filter = [[]]
# tests_prediction_type = ['uniform']

a = 0
# total = len(tests_subject) * len(tests_distance_name) * len(tests_prediction_type) * len(tests_value_used) * len(tests_style_filter)
total = len(tests_distance_name) * len(tests_prediction_type) * len(tests_value_used) * len(tests_style_filter)

results = []
# results.append(['Disciplina', 'Tipo de distância', 'Tipo de valor', 'Filtro de estilo', 'Tipo de previsão', 'Quantidade de alunos', 'Correlação', 'Diferença média', 'Erro', 'Média habilidade', 'Desvio habilidade', 'Média nota', 'Desvio nota', 'Média previsão', 'Desvio previsão'])
results.append(['Tipo de distância', 'Tipo de valor', 'Filtro de estilo', 'Tipo de previsão', 'Nº alunos', 'Correlação', 'Erro', 'Nº alunos', 'Correlação', 'Erro', 'Nº alunos', 'Correlação', 'Erro', 'Nº alunos', 'Correlação', 'Erro', 'Nº alunos', 'Correlação', 'Erro', 'Nº alunos', 'Correlação', 'Erro'])

os.makedirs(graphics_folder_name, exist_ok=True)
os.makedirs(csv_folder_name, exist_ok=True)

for distance_name in tests_distance_name:
    for value_used in tests_value_used:
        for style_filter in tests_style_filter:
            for prediction_type in tests_prediction_type:
                filter_name = ';'.join(style_filter) or 'all'
                new_result = [distance_name, value_used, filter_name, prediction_type]

                for subject in tests_subject:

                    out_info = {}
                    prediction(subject, distance_name, prediction_type, value_used, style_filter, out_info)
                    new_result.append(out_info['quant_students'])
                    new_result.append("%7.3f" % out_info['correlation'])
                    # new_result.append("%7.3f" % out_info['mean_difference'])
                    new_result.append("%7.3f" % out_info['error'])
                    # new_result.append("%7.3f" % out_info['mean_ability'])
                    # new_result.append("%7.3f" % out_info['deviation_ability'])
                    # new_result.append("%7.3f" % out_info['mean_grade'])
                    # new_result.append("%7.3f" % out_info['deviation_grade'])
                    # new_result.append("%7.3f" % out_info['mean_prediction'])
                    # new_result.append("%7.3f" % out_info['deviation_prediction'])

                results.append(new_result)

                a += 1
                print('%d / %d' % (a, total))

np.savetxt(base_path + 'results.csv', results, fmt="%s", delimiter=", ", encoding="utf8")

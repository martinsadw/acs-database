import numpy as np
from sklearn import neighbors, ensemble


def get_distances_matrix(data, distance_function, *args, discretization=None, **kwargs):
    quant_data = data.shape[0]

    distance_matrix = np.empty((quant_data, quant_data))

    for i in range(quant_data):
        for j in range(quant_data):
            distance_matrix[i, j] = distance_function(data[i], data[j], *args, **kwargs)

    if discretization is not None:
        ratio = discretization / np.amax(distance_matrix)
        distance_matrix = np.floor(distance_matrix * ratio) / ratio

    return distance_matrix


def get_grades_prediction(students_grades, suggestions_distances, prediction_type='distance', quant_similar=3):
    quant_students = len(students_grades)
    grade_prediction = np.empty((quant_students,))

    # print(students_grades.tolist())
    # print("------------------")
    # print(suggestions_distances.tolist())
    # print("==================")

    if prediction_type == 'kneighbors':
        distances = suggestions_distances.copy()
        np.fill_diagonal(distances, 1000)

        knn = neighbors.KNeighborsRegressor(quant_similar, metric='precomputed')
        grade_prediction[:] = knn.fit(suggestions_distances, students_grades).predict(distances)
    else:
        for i in range(quant_students):
            distances = np.concatenate((suggestions_distances[i, :i], suggestions_distances[i, i+1:]))
            grades = np.concatenate((students_grades[:i], students_grades[i+1:]))

            # distances = suggestions_distances[i].copy()
            # distances[i] = 1000
            # grades = students_grades.copy()

            sorted_indices = np.argsort(distances)

            similar_distances = distances[sorted_indices[:quant_similar]]
            similar_grades = grades[sorted_indices[:quant_similar]]

            if prediction_type == 'uniform':
                grade_prediction[i] = similar_grades.mean()
            elif prediction_type == 'distance':
                # grade_prediction[i] = np.average(similar_grades, weights=(1 / (similar_distances+0.01)))
                grade_prediction[i] = np.average(similar_grades, weights=(1 - similar_distances + 0.01))

    return grade_prediction


def DEBUG_get_grades_prediction(students_grades, suggestions_distances, students_id, quant_similar=5):
    quant_students = len(students_grades)
    grade_prediction = np.empty((quant_students, quant_similar))
    suggested_students_distance = np.empty((quant_students, quant_similar))
    suggested_students_id = np.empty((quant_students, quant_similar))

    for i in range(quant_students):
        distances = np.concatenate((suggestions_distances[i, :i], suggestions_distances[i, i+1:]))
        grades = np.concatenate((students_grades[:i], students_grades[i+1:]))
        ids = np.concatenate((students_id[:i], students_id[i+1:]))
        sorted_indices = np.argsort(distances)

        grade_prediction[i] = grades[sorted_indices[:quant_similar]]
        suggested_students_distance[i] = distances[sorted_indices[:quant_similar]]
        suggested_students_id[i] = ids[sorted_indices[:quant_similar]]

    return (grade_prediction, suggested_students_distance, suggested_students_id)


def get_grades_regression(students_suggestions, students_grades, regressor_name='kneighbors'):
    quant_students = len(students_grades)
    grade_prediction = np.empty((quant_students,))

    regressor = None
    if regressor_name == 'kneighbors':
        regressor = neighbors.KNeighborsRegressor(metric='matching')
    elif regressor_name == 'gradient':
        regressor = ensemble.GradientBoostingRegressor()

    for i in range(quant_students):
        suggestions = np.concatenate((students_suggestions[:i], students_suggestions[i+1:]))
        grades = np.concatenate((students_grades[:i], students_grades[i+1:]))

        grade_prediction[i] = regressor.fit(suggestions, grades).predict(students_suggestions[i:i+1])

    return grade_prediction

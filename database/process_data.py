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


def get_grades_prediction(students_grades, suggestions_distances, prediction_weight='distance', quant_similar=3):
    quant_students = len(students_grades)
    grade_prediction = np.empty((quant_students,))

    # print(students_grades.tolist())
    # print("------------------")
    # print(suggestions_distances.tolist())
    # print("==================")

    if prediction_weight == 'kneighbors':
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

            if prediction_weight == 'uniform':
                grade_prediction[i] = similar_grades.mean()
            elif prediction_weight == 'distance':
                # grade_prediction[i] = np.average(similar_grades, weights=(1 / (similar_distances+0.01)))
                grade_prediction[i] = np.average(similar_grades, weights=(1 - similar_distances + 0.01))

    return grade_prediction


def get_grades_regression(students_suggestions, students_grades, prediction_weight='distance', quant_similar=3):
    quant_students = len(students_grades)
    grade_prediction = np.empty((quant_students,))

    print(students_suggestions)
    if prediction_weight == 'kneighbors':
        knn = neighbors.KNeighborsRegressor(quant_similar, metric='matching')
        grade_prediction[:] = knn.fit(students_suggestions, students_grades).predict(students_suggestions)
    elif prediction_weight == 'gradient':
        clf = ensemble.GradientBoostingRegressor()
        grade_prediction[:] = clf.fit(students_suggestions, students_grades).predict(students_suggestions)

    return grade_prediction

def DEBUG_get_grades_prediction(students_grades, suggestions_distances, students_id, quant_similar=3):
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

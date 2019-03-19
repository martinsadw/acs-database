import numpy as np

from utils.misc import hamming_distance
from database.consts import quant_materials_subjects, quant_concepts_subjects, concept_subject


def get_students_index(students_db, filter_group=None):
    students_index = {}
    quant_students = 0

    for id, student in students_db.items():
        if (filter_group is None or student["identificador_grupo"] == filter_group):
            students_index[int(id)] = quant_students
            quant_students += 1

    return students_index


def get_students_id(students_index):
    students_id = np.zeros(len(students_index.items()))

    for id, index in students_index.items():
        students_id[index] = id

    return students_id

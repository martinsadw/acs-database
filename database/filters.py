import numpy as np


def filter_students_by_id(students_index, filter=None):
    if filter is None:
        return students_index

    new_student_index = {}
    quant_students = 0

    for id, index in students_index.items():
        if id not in filter:
            continue

        new_student_index[id] = quant_students
        quant_students += 1

    return new_student_index


def filter_students_by_style(students_index, students_styles, filter=None):
    if filter is None:
        filter = []

    new_student_index = {}
    quant_students = 0

    for id, index in students_index.items():
        style = students_styles[index]

        if "ati" in filter and style[0] > 0:
            continue
        if "ref" in filter and style[0] < 0:
            continue

        if "sem" in filter and style[1] > 0:
            continue
        if "int" in filter and style[1] < 0:
            continue

        if "vis" in filter and style[2] > 0:
            continue
        if "ver" in filter and style[2] < 0:
            continue

        if "seq" in filter and style[3] > 0:
            continue
        if "glo" in filter and style[3] < 0:
            continue

        new_student_index[id] = quant_students
        quant_students += 1

    return new_student_index

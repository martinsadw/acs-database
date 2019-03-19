import numpy as np

from database.consts import quant_materials_subjects, quant_concepts_subjects, concept_subject


def get_students_suggestions(subject, students_index, suggestions_db):
    quant_students = len(students_index)
    quant_materials = quant_materials_subjects[subject]

    students_suggestions = np.ma.empty((quant_students, quant_materials), dtype=bool)
    students_suggestions[:] = np.ma.masked

    for id, suggestion in suggestions_db.items():
        if suggestion["id_aluno"] not in students_index or suggestion["id_disciplina"] != subject:
            continue

        student = students_index[suggestion["id_aluno"]]

        students_suggestions[student] = False

        for material in suggestion["materiais_selecionados"]:
            if material != 128:  # Aparentemente tem uma entrada errada. Esse id não existe na base de materiais
                students_suggestions[student, material] = True

    return students_suggestions


def get_students_abilities(subject, students_index, abilities_db, normalize=True):
    quant_students = len(students_index)
    quant_concepts = quant_concepts_subjects[subject]

    students_abilities = np.ma.empty((quant_students,))
    students_abilities[:] = np.ma.masked

    for id, ability in abilities_db.items():
        ability_subject = concept_subject[ability["id_conceito"]]

        if ability["id_aluno"] not in students_index or ability_subject != subject:
            continue

        student = students_index[ability["id_aluno"]]

        if np.ma.is_masked(students_abilities[student]):
            students_abilities[student] = 0

        students_abilities[student] += ability["habilidade"]

    students_abilities /= quant_concepts

    if normalize:
        students_abilities /= 5

    return students_abilities


def get_students_grades(subject, students_index, grade_db, normalize=True):
    quant_students = len(students_index)

    students_grades = np.ma.empty((quant_students,))
    students_grades[:] = np.ma.masked

    for id, grade in grade_db.items():
        if grade["id_aluno"] not in students_index or grade["id_disciplina"] != subject:
            continue

        student = students_index[grade["id_aluno"]]

        if normalize:
            students_grades[student] = grade["pontuacao"] / grade["pontuacao_maxima"]
        else:
            students_grades[student] = grade["pontuacao"]

    return students_grades


def get_students_styles(students_index, styles_db):
    quant_students = len(students_index)

    students_styles = np.ma.empty((quant_students, 4))
    # students_styles = np.ma.empty((quant_students, 4), dtype=bool)
    students_styles[:] = np.ma.masked

    for id, style in styles_db.items():
        if style["id_aluno"] not in students_index:
            continue

        student = students_index[style["id_aluno"]]

        # students_styles[student, 0] = 0 if style["atiref"] < 0 else 1
        # students_styles[student, 1] = 0 if style["semint"] < 0 else 1
        # students_styles[student, 2] = 0 if style["visver"] < 0 else 1
        # students_styles[student, 3] = 0 if style["seqglo"] < 0 else 1

        students_styles[student, 0] = style["atiref"]
        students_styles[student, 1] = style["semint"]
        students_styles[student, 2] = style["visver"]
        students_styles[student, 3] = style["seqglo"]

    return students_styles

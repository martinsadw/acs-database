import json


def open_students():
    with open('data/aluno.json', encoding='utf-8') as f:
        students = json.load(f)

    return students


def open_students_ability():
    with open('data/aluno_conceito.json', encoding='utf-8') as f:
        open_students_ability = json.load(f)

    return open_students_ability


def open_logs():
    with open('data/aluno_disciplina_log.json', encoding='utf-8') as f:
        logs = json.load(f)

    return logs


def open_suggestions():
    with open('data/aluno_disciplina_materiais.json', encoding='utf-8') as f:
        suggestions = json.load(f)

    return suggestions


def open_grades():
    with open('data/aluno_disciplina_pontuacao.json', encoding='utf-8') as f:
        grades = json.load(f)

    return grades


def open_satisfactions():
    with open('data/aluno_disciplina_satisfacao.json', encoding='utf-8') as f:
        satisfactions = json.load(f)

    return satisfactions


def open_concepts():
    with open('data/conceito.json', encoding='utf-8') as f:
        concepts = json.load(f)

    return concepts


def open_subjects():
    with open('data/disciplina.json', encoding='utf-8') as f:
        subjects = json.load(f)

    return subjects


def open_styles():
    with open('data/estilo_de_aprendizagem.json', encoding='utf-8') as f:
        styles = json.load(f)

    return styles


def open_pretests():
    with open('data/questionario.json', encoding='utf-8') as f:
        open_pretests = json.load(f)

    return pretests

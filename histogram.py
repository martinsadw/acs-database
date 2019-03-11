import json
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt


with open('data/aluno_disciplina_materiais.json', encoding='utf-8') as f:
    sugestoes = json.load(f)

with open('data/aluno.json', encoding='utf-8') as f:
    alunos = json.load(f)

quant0 = defaultdict(lambda: defaultdict(int))
quant1 = defaultdict(lambda: defaultdict(int))
quant2 = defaultdict(lambda: defaultdict(int))
quant_materiais = defaultdict(int)
for id, sugestao in sugestoes.items():
    grupo = alunos[str(sugestao["id_aluno"])]["identificador_grupo"]

    disciplina = sugestao["id_disciplina"]
    for material in sugestao["materiais_selecionados"]:
        quant_materiais[disciplina] = max(material, quant_materiais[disciplina])
        if grupo == 0:
            quant0[disciplina][material] += 1
        elif grupo == 1:
            quant1[disciplina][material] += 1
        elif grupo == 2:
            quant2[disciplina][material] += 1

quant1[1].pop(128)  # Aparentemente tem uma entrada errada. Esse id não existe na base de materiais
quant_materiais[1] = 61

disciplinas0 = {}
for disciplina, materiais in quant0.items():
    disciplinas0[disciplina] = np.zeros(quant_materiais[disciplina] + 1)
    for material, freq in materiais.items():
        disciplinas0[disciplina][material] = freq

disciplinas1 = {}
for disciplina, materiais in quant1.items():
    disciplinas1[disciplina] = np.zeros(quant_materiais[disciplina] + 1)
    for material, freq in materiais.items():
        disciplinas1[disciplina][material] = freq

disciplinas2 = {}
for disciplina, materiais in quant2.items():
    disciplinas2[disciplina] = np.zeros(quant_materiais[disciplina] + 1)
    for material, freq in materiais.items():
        disciplinas2[disciplina][material] = freq

for disciplina in disciplinas1:
    print("\nDisciplina: %d" % (disciplina))
    print("-----------------")
    print("Número de materiais: %d" % (disciplinas1[disciplina].shape[0]))
    print("Material mais frequente: %d (%d)" % (disciplinas1[disciplina].argmax(), disciplinas1[disciplina].max()))
    print("=================\n")
    print(disciplinas1[disciplina])

    # fig = plt.figure()
    # fig.suptitle('Frequência de materiais - Disciplina %d' % (disciplina))
    # plt.ylim((0, 130))
    # p1 = plt.bar(range(disciplinas1[disciplina].shape[0]), disciplinas1[disciplina])
    # p0 = plt.bar(range(disciplinas0[disciplina].shape[0]), disciplinas0[disciplina], bottom=disciplinas1[disciplina])
    # p2 = plt.bar(range(disciplinas2[disciplina].shape[0]), disciplinas2[disciplina], bottom=(disciplinas0[disciplina] + disciplinas1[disciplina]))
    # plt.legend((p0[0], p1[0], p2[0]), ('Grupo 0', 'Grupo 1', 'Grupo 2'))
    # plt.show()

    fig = plt.figure()
    plt.ylim((0, 62))
    fig.suptitle('Histograma de materiais - Disciplina %d' % (disciplina))
    plt.hist(disciplinas1[disciplina], bins=16, range=(0, 80))
    plt.show()

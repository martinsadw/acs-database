import json

###############################################################################

print("aluno.json")
print("==========")
with open('data/aluno.json', encoding='utf-8') as f:
    alunos = json.load(f)

size = len(alunos)
t_min = 0
t_max = 0
exp = 0
hab = 0
for id, aluno in alunos.items():
    t_min += aluno["tempo_disponivel_min"]
    t_max += aluno["tempo_disponivel_max"]
    exp += aluno["experiencia"]
    hab += aluno["habilidade"]

print('Tempo disponível mínimo médio: %f' % (t_min / size))
print('Tempo disponível máximo médio: %f' % (t_max / size))
print('Experiência média: %f' % (exp / size))
print(' Habilidade média: %f' % (hab / size))

###############################################################################

print("")
print("")
print("aluno_conceito.json")
print("===================")
with open('data/aluno_conceito.json', encoding='utf-8') as f:
    alunos_conceitos = json.load(f)

size = len(alunos_conceitos)
hab = 0
for id, aluno_conceito in alunos_conceitos.items():
    hab += aluno_conceito["habilidade"]

print('Habilidade média: %f' % (hab / size))

###############################################################################

print("")
print("")
print("aluno_disciplina_log.json")
print("=========================")
with open('data/aluno_disciplina_log.json', encoding='utf-8') as f:
    logs = json.load(f)

diff = 0
for id, log in logs.items():
    if log["entrada"]:
        hab += 1
    else:
        hab -= 1

print('Diff Entradas/Saidas: %d' % (diff))

###############################################################################

print("")
print("")
print("aluno_disciplina_materiais.json")
print("===============================")
with open('data/aluno_disciplina_materiais.json', encoding='utf-8') as f:
    sugestoes = json.load(f)

size = len(sugestoes)
quant = 0
for id, sugestao in sugestoes.items():
    quant += len(sugestao["materiais_selecionados"])

print('Quantidade média de materiais: %f' % (quant / size))

###############################################################################

print("")
print("")
print("aluno_disciplina_pontuacao.json")
print("===============================")
with open('data/aluno_disciplina_pontuacao.json', encoding='utf-8') as f:
    pontuacoes = json.load(f)

size = len(pontuacoes)
size0 = 0
size1 = 0
size2 = 0
notas = 0
notas0 = 0
notas1 = 0
notas2 = 0
for id, pontuacao in pontuacoes.items():
    notas += pontuacao["pontuacao"] / pontuacao["pontuacao_maxima"]

    grupo = alunos[str(pontuacao["id_aluno"])]["identificador_grupo"]
    if grupo == 0:
        size0 += 1
        notas0 += pontuacao["pontuacao"] / pontuacao["pontuacao_maxima"]
    elif grupo == 1:
        size1 += 1
        notas1 += pontuacao["pontuacao"] / pontuacao["pontuacao_maxima"]
    elif grupo == 2:
        size2 += 1
        notas2 += pontuacao["pontuacao"] / pontuacao["pontuacao_maxima"]

print('Nota média: %f' % ((notas / size) * 100))
print('Nota média grupo 0: %f' % ((notas0 / size0) * 100))
print('Nota média grupo 1: %f' % ((notas1 / size1) * 100))
print('Nota média grupo 2: %f' % ((notas2 / size2) * 100))

###############################################################################

print("")
print("")
print("aluno_disciplina_satisfacao.json")
print("================================")
with open('data/aluno_disciplina_satisfacao.json', encoding='utf-8') as f:
    satisfacoes = json.load(f)

size = len(satisfacoes)
dificuldade = 0
tempo = 0
questionario = 0
estilo_aprendizagem = 0
for id, satisfacao in satisfacoes.items():
    dificuldade += satisfacao["dificuldade"]
    tempo += satisfacao["tempo"]
    questionario += satisfacao["questionario"]
    estilo_aprendizagem += satisfacao["estilo_de_aprendizagem"]

print('           Dificuldade média: %f' % (dificuldade / size))
print('                 Tempo médio: %f' % (tempo / size))
print('          Questionário médio: %f' % (questionario / size))
print('Estilo de aprendizagem médio: %f' % (estilo_aprendizagem / size))

###############################################################################

print("")
print("")
print("conceito.json")
print("=============")
with open('data/conceito.json', encoding='utf-8') as f:
    conceitos = json.load(f)

size = len(conceitos)
for id, conceito in conceitos.items():
    pass

print('Quantidade de conceitos: %d' % (size))

###############################################################################

print("")
print("")
print("disciplina.json")
print("===============")
with open('data/disciplina.json', encoding='utf-8') as f:
    disciplinas = json.load(f)

size = len(disciplinas)
for id, disciplina in disciplinas.items():
    pass

print('Quantidade de disciplinas: %d' % (size))

###############################################################################

print("")
print("")
print("estilo_de_aprendizagem.json")
print("===========================")
with open('data/estilo_de_aprendizagem.json', encoding='utf-8') as f:
    estilos = json.load(f)

quant_ati = 0
quant_ref = 0
quant_sem = 0
quant_int = 0
quant_vis = 0
quant_ver = 0
quant_seq = 0
quant_glo = 0
for id, estilo in estilos.items():
    if estilo["atiref"] < 0:
        quant_ati += 1
    else:
        quant_ref += 1

    if estilo["semint"] < 0:
        quant_sem += 1
    else:
        quant_int += 1

    if estilo["visver"] < 0:
        quant_vis += 1
    else:
        quant_ver += 1

    if estilo["seqglo"] < 0:
        quant_seq += 1
    else:
        quant_glo += 1

print('     ativo | reflexivo: %d | %d' % (quant_ati, quant_ref))
print(' sensitivo | intuitivo: %d | %d' % (quant_sem, quant_int))
print('    visual |    verbal: %d | %d' % (quant_vis, quant_ver))
print('sequencial |    global: %d | %d' % (quant_seq, quant_glo))

###############################################################################

print("")
print("")
print("questionario.json")
print("=================")
with open('data/questionario.json', encoding='utf-8') as f:
    questionarios = json.load(f)

size = len(questionarios)
quant_muito_abaixo = 0
quant_abaixo = 0
quant_nivel = 0
quant_acima = 0
acertos_abaixo = 0
acertos_nivel = 0
acertos_acima = 0
for id, questionario in questionarios.items():
    if not questionario["questao_do_nivel_mais_baixo"]:
        quant_muito_abaixo += 1
    else:
        if not questionario["questao_do_mesmo_nivel"]:
            quant_abaixo += 1
        else:
            if not questionario["questao_do_nivel_mais_alto"]:
                quant_nivel += 1
            else:
                quant_acima += 1

    if questionario["questao_do_nivel_mais_baixo"]:
        acertos_abaixo += 1
    if questionario["questao_do_mesmo_nivel"]:
        acertos_nivel += 1
    if questionario["questao_do_nivel_mais_alto"]:
        acertos_acima += 1


print('Quantidade muito abaixo: %d' % (quant_muito_abaixo))
print('      Quantidade abaixo: %d' % (quant_abaixo))
print('    Quantidade no nível: %d' % (quant_nivel))
print('       Quantidade acima: %d' % (quant_acima))
print('  Porcentagem de acertos questão abaixo: %f' % ((acertos_abaixo / size) * 100))
print('Porcentagem de acertos questão no nível: %f' % ((acertos_nivel / size) * 100))
print('   Porcentagem de acertos questão acima: %f' % ((acertos_acima / size) * 100))

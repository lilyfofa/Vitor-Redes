from sympy import *


def RetPol(a, tensoes, i):  # Função que converte um número complexo em coordenadas retangulares para coordenadas polares
    return f"{tensoes[i]} = {sqrt(re(a) ** 2 + im(a) ** 2):.2f} <{N(atan2(im(a), re(a)) * 180 / pi):.2f}° [V]"


def AnaliseNodal(dados, parametros):
    cargas = dados
    n = int(parametros[0])
    referencia = int(parametros[1])
    no_nominal = int(parametros[2])
    tensao_nominal = sympify(parametros[3].replace("j", "I*"))
    admitancias = zeros(n, n)  # Matriz de admitâncias
    correntes = zeros(n, 1)  # Matriz de correntes
    tensoes = zeros(n, 1)  # Matriz de tensões nodais
    for i in range(0, n):  # Acrescentando as variáveis para as tensões nodais
        tensoes[i] = symbols(f"V{i}")
    for i in range(0, len(cargas)):
        carga = sympify(cargas[i][0].replace("j", "I*"))  # Input de impedância da carga
        no1 = int(cargas[i][1])
        no2 = int(cargas[i][2])
        admitancias[no1, no2] -= 1 / carga  # Admitancia do nó IJ adicionada ao item XY da matriz
        admitancias[no2, no1] -= 1 / carga  # Admitancia do nó JI adicionada ao item XY da matriz
        admitancias[no1, no1] += 1 / carga  # Admitancia do nó II adicionada ao item XY da matriz
        admitancias[no2, no2] += 1 / carga  # Admitancia do nó JJ adicionada ao item XY da matriz
    for i in range(0, n):  # Na linha nó nominal, esse for vai zerar todos os valores e colocar 1 na coluna equivalente
        if i == no_nominal:
            admitancias[no_nominal, i] = 1
        else:
            admitancias[no_nominal, i] = 0
    if parametros[4] != 'nao':
        correntes[parametros[5]] = -1 * sympify(parametros[6].replace("j", "I*"))  # Corrente entra negativa na matriz
    correntes[no_nominal] = tensao_nominal  # Colocar o valor da tensão nominal na matriz das correntes, na linha da tensão nominal
    correntes.row_del(referencia)  # Deletando a linha do nó de referência na matriz das correntes
    tensoes.row_del(referencia)  # Deletando a linha do nó de referência na matriz das tensões
    admitancias.row_del(referencia)  # Deletando a linha do nó de referência na matriz das admitâncias
    admitancias.col_del(referencia)  # Deletando a linha do nó de referência na matriz das admitâncias
    resposta = admitancias.solve(correntes)  # Resolvendo o sistema linear pelo Sympy
    resultado = []
    for i in range(0, len(resposta)):
        resultado.append(RetPol(resposta[i], tensoes, i))
    return resultado


from sympy import *


def RetPol(a):  # Função que converte um número complexo em coordenadas retangulares para coordenadas polares
    return f"{sqrt(re(a) ** 2 + im(a) ** 2):.2f} <{N(atan2(im(a), re(a)) * 180 / pi):.2f}° [V]"


print("Vitor Redes")  # Nome do programa
print("-=" * 15)

n = int(input("Determine o número de nós: "))  # Número de nós

admitancias = zeros(n, n)  # Matriz de admitâncias
correntes = zeros(n, 1)  # Matriz de correntes
tensoes = zeros(n, 1)  # Matriz de tensões nodais

for i in range(0, n):  # Acrescentando as variáveis para as tensões nodais
    tensoes[i] = symbols(f"V{i}")

contador = 1  # Contador de cargas

print("-=" * 15)
print("Digite 999999 para parar de inserir cargas.")

while True:
    print("-=" * 15)
    print(f"Carga {contador}")
    carga = sympify(input("Digite a impedância da carga: ").replace("j", "I*"))  # Input de impedância da carga
    if carga == 999999:  # If para verificar o fim do processo de inserção de dados
        break
    no1 = int(input("Determine o primeiro nó: "))  # Determinação do nó de início
    no2 = int(input("Determine o segundo nó: "))  # Determinação do nó final
    admitancias[no1, no2] -= 1 / carga  # Admitancia do nó IJ adicionada ao item XY da matriz
    admitancias[no2, no1] -= 1 / carga  # Admitancia do nó JI adicionada ao item XY da matriz
    admitancias[no1, no1] += 1 / carga  # Admitancia do nó II adicionada ao item XY da matriz
    admitancias[no2, no2] += 1 / carga  # Admitancia do nó JJ adicionada ao item XY da matriz
    contador += 1

print("-=" * 15)

referencia = int(input("Determine o nó de referência: "))  # Nó de referência
no_nominal = int(input("Determine o nó de tensão conhecida: "))  # Nó nominal
tensao_nominal = sympify(input("Determine a tensão nominal: ").replace("j", "I*"))  # Valor da tensão no nó nominal

print("-=" * 15)

resposta = input("Existe alguma injeção de corrente ou potência? [S/N] ")

if resposta.upper() == 'S':  # Em resposta positiva, determinar valor da corrente/potência
    no_injecao = int(input("Em qual nó? "))
    valor_injecao = sympify(input("Determine o valor da injeção [A/VA]: ").replace("j", "I*"))
    correntes[no_injecao] = -1 * valor_injecao  # Corrente/potência entra negativa na matriz

for i in range(0, n):  # Na linha nó nominal, esse for vai zerar todos os valores e colocar 1 na coluna equivalente
    if i == no_nominal:
        admitancias[no_nominal, i] = 1
    else:
        admitancias[no_nominal, i] = 0

correntes[
    no_nominal] = tensao_nominal  # Colocar o valor da tensão nominal na matriz das correntes, na linha da tensão nominal
correntes.row_del(referencia)  # Deletando a linha do nó de referência na matriz das correntes
tensoes.row_del(referencia)  # Deletando a linha do nó de referência na matriz das tensões
admitancias.row_del(referencia)  # Deletando a linha do nó de referência na matriz das admitâncias
admitancias.col_del(referencia)  # Deletando a linha do nó de referência na matriz das admitâncias

print("-=" * 15)
print("Reposta: ")

resposta = admitancias.solve(correntes)  # Resolvendo o sistema linear pelo Sympy

for i in range(0, len(resposta)):  # Mostrando as repostas
    print(f"{tensoes[i]} = {RetPol(resposta[i])}".replace("*I", "j"))

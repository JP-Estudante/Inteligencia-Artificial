import random

def gerar_estado_inicial():
    "Gera um estado inicial aleatório: uma rainha por coluna, em linha aleatória"
    return [random.randint(0, 7) for _ in range(8)]

def custo(estado):
    "Calcula o custo de um estado (número de pares de rainhas que se atacam)"
    conflitos = 0
    for i in range(len(estado)): # Percorre cada rainha
        for j in range(i + 1, len(estado)): # Compara as rainhas seguintes
            if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(i - j): # Se estiverem na mesma linha, ou diagonal
                conflitos += 1
    return conflitos

def gerar_vizinho(estado):
    "Gera um vizinho alterando a linha de uma rainha (coluna aleatória)"
    novo_estado = estado[:] # Criando cópia para não afetar a original
    col = random.randint(0, 7) # Escolher coluna aleatória
    nova_linha = random.randint(0, 7) # Escolher linha aleatória
    
    while nova_linha == novo_estado[col]: # `novo_estado[col]` linha atual da rainha nessa coluna
        nova_linha = random.randint(0, 7)  # Gera outra linha
    novo_estado[col] = nova_linha # Atribui a nova posição da rainha gerada
    
    return novo_estado # Modificado

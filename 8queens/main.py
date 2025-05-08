import math
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
    
    while nova_linha == novo_estado[col]:  # `novo_estado[col]` linha atual da rainha nessa coluna
        nova_linha = random.randint(0, 7)  # Gera outra linha
    novo_estado[col] = nova_linha # Atribui a nova posição da rainha gerada
    
    return novo_estado # Modificado

def temperatura_inicial():
    "Temperatura inicial"
    return 100

def temperatura_final():
    "Temperatura Final"
    return 0.1

def reduzir(temperatura):
    "Reduz a temperatura (fator de resfriamento)"
    return temperatura * 0.95 # Reduz 5% cada vez

def tempera_simulada():
    estado_atual = gerar_estado_inicial()
    temperatura = temperatura_inicial()
    
    while temperatura > temperatura_final() or custo(estado_atual) == 0:
        vizinho = gerar_vizinho(estado_atual)
        custo_atual = custo(estado_atual)
        custo_vizinho = custo(vizinho)
        delta_e = custo_vizinho - custo_atual
        
        if delta_e < 0: # Melhor solução, aceita
            estado_atual = vizinho
        else: # Pior solução, aceita com probabilidade
            probabilidade = math.exp(-delta_e / temperatura)
            r = random.random()
            if r < probabilidade:
                estado_atual = vizinho
        
        temperatura = reduzir(temperatura)
        
        if custo(estado_atual) == 0:
            break
        
    return estado_atual


if __name__ == "__main__":
    solucao = tempera_simulada()
    print("Solução: ", solucao)
    print("Conflitos: ", custo(solucao))
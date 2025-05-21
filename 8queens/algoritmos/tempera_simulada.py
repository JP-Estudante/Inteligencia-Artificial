import math
import random
from auxiliar.alg_utils import gerar_estado_inicial, custo, gerar_vizinho
from auxiliar.metricas import qualidade

def temperatura_inicial():
    "Temperatura inicial"
    return 200

def temperatura_final():
    "Temperatura Final"
    return 0.1

def reduzir(temperatura): 
    "Reduz a temperatura (fator de resfriamento)"
    return temperatura * 0.999 # Reduz % cada vez

def tempera_simulada():
    estado_atual = gerar_estado_inicial()
    temperatura = temperatura_inicial()
    iteracoes = 0
    melhor_qualidade = qualidade(estado_atual)

    while temperatura > temperatura_final():
        iteracoes += 1
        
        vizinho = gerar_vizinho(estado_atual)
        custo_atual = custo(estado_atual)
        custo_vizinho = custo(vizinho)
        delta_e = custo_vizinho - custo_atual
        
        if delta_e < 0: # Melhor solução, aceita
            estado_atual = vizinho
        else: # Pior solução, aceita com probabilidade
            probabilidade = math.exp(-delta_e / temperatura)
            if random.random() < probabilidade:
                estado_atual = vizinho
        
        temperatura = reduzir(temperatura)
        
        if custo(estado_atual) != 0: # A melhor qualidade antes de resolver o problema
            melhor_qualidade = max(melhor_qualidade, qualidade(estado_atual)) 

        
        if custo(estado_atual) == 0:
            break
        
    return estado_atual, iteracoes, melhor_qualidade

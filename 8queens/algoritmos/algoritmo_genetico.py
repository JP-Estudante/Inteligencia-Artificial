import random
from auxiliar.alg_utils import gerar_estado_inicial, custo
from auxiliar.metricas import qualidade

TAMANHO_POPULACAO = 100
TORNEIO_K = 3
TAXA_MUTACAO = 0.1
MAX_GERACOES = 1000
MAX_CONFLITOS = 28

def fitness(estado):
    return MAX_CONFLITOS - custo(estado)

def selecao_torneio(populacao):
    candidatos = random.sample(populacao, TORNEIO_K)
    return max(candidatos, key=lambda c: fitness(c))

def crossover(pai1, pai2):
    ponto_corte = random.randint(1, 7)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2

def mutacao(cromossomo):
    if random.random() < TAXA_MUTACAO:
        i, j = random.sample(range(8), 2)
        cromossomo[i], cromossomo[j] = cromossomo[j], cromossomo[i]
    return cromossomo

def algoritmo_genetico():
    populacao = [gerar_estado_inicial() for _ in range(TAMANHO_POPULACAO)]
    melhor_qualidade = 0

    for geracao in range(MAX_GERACOES):
        nova_populacao = []

        for _ in range(TAMANHO_POPULACAO // 2):
            pai1 = selecao_torneio(populacao)
            pai2 = selecao_torneio(populacao)

            filho1, filho2 = crossover(pai1, pai2)
            filho1 = mutacao(filho1)
            filho2 = mutacao(filho2)

            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao

        for individuo in populacao:
            if custo(individuo) == 0:
                return individuo, geracao + 1, MAX_CONFLITOS
            melhor_qualidade = max(melhor_qualidade, qualidade(individuo))

    melhor = max(populacao, key=fitness)
    return melhor, MAX_GERACOES, melhor_qualidade

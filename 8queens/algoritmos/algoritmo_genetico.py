import random
from auxiliar.alg_utils import gerar_estado_inicial, custo
from auxiliar.metricas import qualidade

# Valores padrão (caso o usuário apenas pressione Enter)
TAMANHO_POPULACAO = 100
TORNEIO_K = 3
TAXA_MUTACAO = 0.1
MAX_GERACOES = 1000
USAR_CORRECAO = True

# Solicita parâmetros ao usuário
def configurar_parametros():
    global TAMANHO_POPULACAO, TORNEIO_K, TAXA_MUTACAO, MAX_GERACOES, USAR_CORRECAO

    try:
        TAMANHO_POPULACAO = int(input(f"TAMANHO_POPULACAO = ({TAMANHO_POPULACAO}) ") or TAMANHO_POPULACAO)
        TORNEIO_K = int(input(f"TORNEIO_K = ({TORNEIO_K}) ") or TORNEIO_K)
        TAXA_MUTACAO = float(input(f"TAXA_MUTACAO = ({TAXA_MUTACAO}) ") or TAXA_MUTACAO)
        MAX_GERACOES = int(input(f"MAX_GERACOES = ({MAX_GERACOES}) ") or MAX_GERACOES)

        usar = input("Usar correção de repetições no crossover? (s/n) [padrão: s]: ").strip().lower()
        USAR_CORRECAO = (usar != 'n')

    except ValueError:
        print("Entrada inválida. Usando valores padrão.")

# Avaliação do indivíduo (quanto maior a qualidade, melhor)
def fitness(estado):
    return qualidade(estado)

# Seleção por torneio entre K indivíduos aleatórios
def selecao_torneio(populacao):
    candidatos = random.sample(populacao, TORNEIO_K)
    return max(candidatos, key=fitness)

# Crossover com ou sem correção
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, 7)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]

    if USAR_CORRECAO:
        filho1 = corrigir_repeticoes(filho1)
        filho2 = corrigir_repeticoes(filho2)

    return filho1, filho2

def corrigir_repeticoes(filho):
    todos_valores = set(range(8))
    usados = set()
    faltando = []

    for i in range(8):
        if filho[i] not in usados:
            usados.add(filho[i])
        else:
            filho[i] = None  # marca duplicado

    faltando = list(todos_valores - usados)

    for i in range(8):
        if filho[i] is None:
            filho[i] = faltando.pop(0)

    return filho

# Mutação por troca de posições aleatórias
def mutacao(cromossomo):
    if random.random() < TAXA_MUTACAO:
        i, j = random.sample(range(8), 2)
        cromossomo[i], cromossomo[j] = cromossomo[j], cromossomo[i]
    return cromossomo

# Algoritmo Genético principal
def algoritmo_genetico():
    populacao = [gerar_estado_inicial() for _ in range(TAMANHO_POPULACAO)]
    melhor_qualidade_antes_solucao = 0

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
            q = qualidade(individuo)

            if custo(individuo) == 0:
                return individuo, geracao + 1, melhor_qualidade_antes_solucao

            if q > melhor_qualidade_antes_solucao:
                melhor_qualidade_antes_solucao = q

    melhor = max(populacao, key=fitness)
    return melhor, MAX_GERACOES, melhor_qualidade_antes_solucao
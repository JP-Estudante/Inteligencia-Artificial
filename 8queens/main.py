import time
from algoritmos.tempera_simulada import tempera_simulada
from algoritmos.subida_da_encosta import subida_da_encosta_com_reinicio
from auxiliar.alg_utils import custo
from auxiliar.metricas import medir_tempo_execucao

# Lista de algoritmos com nome e função
algoritmos = [
    ("Tempera Simulada", tempera_simulada),
    ("Subida da Encosta", subida_da_encosta_com_reinicio),
    # Futuramente: ("Alg. Genético", algoritmo_genetico),
]

# Resultados de múltiplas execuções
historico_sucesso = {nome: 0 for nome, _ in algoritmos}

def executar_algoritmos():
    resultados = []

    for nome, func in algoritmos:
        @medir_tempo_execucao
        def executar():
            return func()

        (solucao, iteracoes, melhor_qualidade), tempo = executar()
        valida = custo(solucao) == 0
        resultados.append({
            "nome": nome,
            "solucao": solucao,
            "tempo": tempo,
            "iteracoes": iteracoes,
            "qualidade": melhor_qualidade,
            "valida": valida
        })
        if valida:
            historico_sucesso[nome] += 1

    return resultados

def imprimir_resultados(resultados):
    colunas = len(resultados)
    largura = 20
    separador_topo = "╔" + "╦".join(["═" * largura] * colunas) + "╗"
    separador_meio = "╟" + "╫".join(["─" * largura] * colunas) + "╢"
    separador_fundo = "╚" + "╩".join(["═" * largura] * colunas) + "╝"

    header = "║ " + " ║ ".join(f"{r['nome']:<{largura - 2}}" for r in resultados) + " ║"
    iteracoes = "║ " + " ║ ".join(f"Iterações: {r['iteracoes']:<{largura - 13}}" for r in resultados) + " ║"
    qualidade = "║ " + " ║ ".join(f"Qualidade: {r['qualidade']:<{largura - 13}}" for r in resultados) + " ║"
    tempo = "║ " + " ║ ".join(f"Tempo: {r['tempo']:.4f}s".ljust(largura - 2) for r in resultados) + " ║"
    status = "║ " + " ║ ".join(f"Status: {'✓' if r['valida'] else '✗'}".ljust(largura - 2) for r in resultados) + " ║"

    print(separador_topo)
    print(header)
    print(separador_meio)
    print(iteracoes)
    print(qualidade)
    print(tempo)
    print(status)
    print(separador_fundo)

# Executar 10 vezes
for i in range(10):
    print(f"\nExecução {i + 1}/10")
    resultados = executar_algoritmos()
    imprimir_resultados(resultados)
    time.sleep(1.5)

# Imprimir resumo de sucessos
print("\nResumo de Sucessos:")
for nome in historico_sucesso:
    sucesso = historico_sucesso[nome]
    print(f"- {nome}: {sucesso}/10 ✓")

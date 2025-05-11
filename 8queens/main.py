from algoritmos.tempera_simulada import tempera_simulada
from auxiliar.alg_utils import custo
from auxiliar.metricas import medir_tempo_execucao

@medir_tempo_execucao
def executar_algoritmo():
    return tempera_simulada()

sucessos = 0

for _ in range(10):
    (solucao, iteracoes, melhor_qualidade), tempo = executar_algoritmo()
    if custo(solucao) == 0:
        sucessos += 1
        print("Solução encontrada:", solucao)
        print(f"→ Tempo de execução: {tempo:.4f} segundos")
        print(f"→ Iterações até encontrar solução: {iteracoes}")
        print(f"→ Qualidade da melhor solução antes do final: {melhor_qualidade}")
    else:
        print("Nenhuma solução válida.")

print(f"Soluções válidas: {sucessos}/10")

import time
import os

def medir_tempo_execucao(func):
    "Decora a função e retorna resultado + tempo"
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        tempo = fim - inicio
        return resultado, tempo
    return wrapper

def qualidade(estado):
    "Retorna número de pares de rainhas que NÃO se atacam"
    total_rainhas = len(estado)
    conflitos = 0
    for i in range(total_rainhas):
        for j in range(i + 1, total_rainhas):
            if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(i - j):
                conflitos += 1
    max_conflitos = total_rainhas * (total_rainhas - 1) // 2
    return max_conflitos - conflitos

def calcular_media_tempos(lista_tempos):
    return sum(lista_tempos) / len(lista_tempos) if lista_tempos else 0

def formatar_resultado_unitario(i, reinicios, iteracoes, qualidade, tempo, valida, vezes):
    resultado = [
        f"\nExecução {i + 1}/{vezes}\n",
        f"Reinícios: {reinicios if reinicios is not None else '-':<15}",
        f"Iterações: {iteracoes:<15}",
        f"Qualidade: {qualidade:<15}",
        f"Tempo: {tempo:.4f}s".ljust(20),
        f"Status: {'✓' if valida else '✗'}".ljust(20),
        "─────────────────"
    ]
    return "\n".join(resultado)

def salvar_resultado_em_arquivo(linhas, caminho="resultado_execucao.txt"):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for linha in linhas:
            arquivo.write(linha + "\n")

    try:
        os.startfile(caminho)
    except AttributeError:
        print(f"Resultado salvo em {caminho}.")

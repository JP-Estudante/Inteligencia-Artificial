import time

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

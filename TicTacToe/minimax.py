import random

def inicializar_tabuleiro():
    return [[' ' for _ in range(3)] for _ in range(3)]

def verificar_vencedor(tabuleiro):
    for linha in tabuleiro:
        if linha[0] == linha[1] == linha[2] != ' ':
            return linha[0]
    for col in range(3):
        if tabuleiro[0][col] == tabuleiro[1][col] == tabuleiro[2][col] != ' ':
            return tabuleiro[0][col]
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != ' ':
        return tabuleiro[0][0]
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != ' ':
        return tabuleiro[0][2]
    return None

def verificar_empate(tabuleiro):
    for linha in tabuleiro:
        if ' ' in linha:
            return False
    return verificar_vencedor(tabuleiro) is None

def movimentos_possiveis(tabuleiro):
    return [(i, j) for i in range(3) for j in range(3) if tabuleiro[i][j] == ' ']

def minimax(tabuleiro, profundidade, alfa, beta, maximizando):
    vencedor = verificar_vencedor(tabuleiro)
    if vencedor == 'X':
        return 1
    elif vencedor == 'O':
        return -1
    elif verificar_empate(tabuleiro):
        return 0

    if maximizando:
        max_avaliacao = float('-inf')
        for i, j in movimentos_possiveis(tabuleiro):
            tabuleiro[i][j] = 'X'
            avaliacao = minimax(tabuleiro, profundidade + 1, alfa, beta, False)
            tabuleiro[i][j] = ' '
            max_avaliacao = max(max_avaliacao, avaliacao)
            alfa = max(alfa, avaliacao)
            if beta <= alfa:
                break
        return max_avaliacao
    else:
        min_avaliacao = float('inf')
        for i, j in movimentos_possiveis(tabuleiro):
            tabuleiro[i][j] = 'O'
            avaliacao = minimax(tabuleiro, profundidade + 1, alfa, beta, True)
            tabuleiro[i][j] = ' '
            min_avaliacao = min(min_avaliacao, avaliacao)
            beta = min(beta, avaliacao)
            if beta <= alfa:
                break
        return min_avaliacao

def melhor_jogada(tabuleiro):
    # Se for a primeira jogada                  
    if all(celula == ' ' for linha in tabuleiro for celula in linha):
        return random.choice([(i, j) for i in range(3) for j in range(3)])
    
    melhor_valor = float('-inf')
    melhor_movimento = None
    for i, j in movimentos_possiveis(tabuleiro):
        tabuleiro[i][j] = 'X'
        valor = minimax(tabuleiro, 0, float('-inf'), float('inf'), False)
        tabuleiro[i][j] = ' '
        if valor > melhor_valor:
            melhor_valor = valor
            melhor_movimento = (i, j)
    return melhor_movimento

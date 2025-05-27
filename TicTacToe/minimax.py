import random

def inicializar_tabuleiro():
    return [[' ' for _ in range(3)] for _ in range(3)]

# {[' '], [' '], [' '],
#  [' '], [' '], [' '],
#  [' '], [' '], [' ']}

def verificar_vencedor(tabuleiro):
    for linha in tabuleiro:
        if linha[0] == linha[1] == linha[2] != ' ': # Verifica na horizontal
            return linha[0]
    for col in range(3):
        if tabuleiro[0][col] == tabuleiro[1][col] == tabuleiro[2][col] != ' ': # Verifica na vertical
            return tabuleiro[0][col]
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != ' ': # Verifica na diagonal
        return tabuleiro[0][0]
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != ' ': # Verifica na diagonal
        return tabuleiro[0][2]
    return None

def verificar_empate(tabuleiro):
    for linha in tabuleiro:
        if ' ' in linha:
            return False # Não tem como ser empate, se não estiver tudo preenchido
    return verificar_vencedor(tabuleiro) is None # Se `verificar_vencedor` retornar None, empate == true

def movimentos_possiveis(tabuleiro):
    return [(i, j) for i in range(3) for j in range(3) if tabuleiro[i][j] == ' '] # Retorna `i` e `j` aonde for == ' '

def minimax(tabuleiro, profundidade, alfa, beta, maximizando):
    vencedor = verificar_vencedor(tabuleiro)
    if vencedor == 'X':
        return 1
    elif vencedor == 'O':
        return -1
    elif verificar_empate(tabuleiro):
        return 0

    if maximizando:
        max_avaliacao = float('-inf') # Inicializa de modo que qualquer coisa é melhor
        for i, j in movimentos_possiveis(tabuleiro):
            tabuleiro[i][j] = 'X' # Simulação de uma jogada
            avaliacao = minimax(tabuleiro, profundidade + 1, alfa, beta, False) # Recursiva para a próxima jogada
            tabuleiro[i][j] = ' ' # Limpa para simular uma próxima
            max_avaliacao = max(max_avaliacao, avaliacao) # O melhor valor que o MAX encontrou nessa chamada (Local)
            alfa = max(alfa, avaliacao) # O melhor valor que o MAX encontrou em todas as jogadas (Global)
            if beta <= alfa: # Se for `True` vai ocorrer a poda
                break
        return max_avaliacao
    else:
        min_avaliacao = float('inf')
        for i, j in movimentos_possiveis(tabuleiro):
            tabuleiro[i][j] = 'O' # Simula uma jogada
            avaliacao = minimax(tabuleiro, profundidade + 1, alfa, beta, True)
            tabuleiro[i][j] = ' ' # Limpa 
            min_avaliacao = min(min_avaliacao, avaliacao) # Melhor valor local do MIN
            beta = min(beta, avaliacao) # Melhor valor global do MIN
            if beta <= alfa: # Poda
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

def estimar_chances(tabuleiro):
    vitorias = empates = derrotas = 0
    for i, j in movimentos_possiveis(tabuleiro):
        tabuleiro[i][j] = 'X'
        resultado = minimax(tabuleiro, 0, float('-inf'), float('inf'), False)
        tabuleiro[i][j] = ' '
        if resultado == 1:
            vitorias += 1
        elif resultado == 0:
            empates += 1
        elif resultado == -1:
            derrotas += 1

    total = vitorias + empates + derrotas
    if total == 0:
        return 0, 0, 0
    return (
        round((vitorias / total) * 100),
        round((empates / total) * 100),
        round((derrotas / total) * 100)
    )

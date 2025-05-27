import tkinter as tk
from minimax import inicializar_tabuleiro, verificar_vencedor, verificar_empate, melhor_jogada, estimar_chances

CEL_SIZE = 100 # Tamanho do tabuleiro
LINE_WIDTH = 4 # Espessura da linha

placar = {'IA': 0, 'Humano': 0}  # Acumulativo

def desenhar_grade(canvas):
    for i in range(1, 3):
        canvas.create_line(0, i*CEL_SIZE, 3*CEL_SIZE, i*CEL_SIZE, width=LINE_WIDTH)
        canvas.create_line(i*CEL_SIZE, 0, i*CEL_SIZE, 3*CEL_SIZE, width=LINE_WIDTH)

def desenhar_XO(canvas, tabuleiro):
    canvas.delete('marcas')
    canvas.delete('vitoria')
    for i in range(3):
        for j in range(3):
            x = j * CEL_SIZE
            y = i * CEL_SIZE
            if tabuleiro[i][j] == 'X':
                canvas.create_line(x+20, y+20, x+CEL_SIZE-20, y+CEL_SIZE-20, width=LINE_WIDTH, tag='marcas')
                canvas.create_line(x+20, y+CEL_SIZE-20, x+CEL_SIZE-20, y+20, width=LINE_WIDTH, tag='marcas')
            elif tabuleiro[i][j] == 'O':
                canvas.create_oval(x+20, y+20, x+CEL_SIZE-20, y+CEL_SIZE-20, width=LINE_WIDTH, tag='marcas')

def encontrar_linha_vencedora(tabuleiro):
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] != ' ':
            return ('linha', i)
    for j in range(3):
        if tabuleiro[0][j] == tabuleiro[1][j] == tabuleiro[2][j] != ' ':
            return ('coluna', j)
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != ' ':
        return ('diagonal', 'principal')
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != ' ':
        return ('diagonal', 'secundaria')
    return None

def desenhar_linha_vencedora(canvas, tipo):
    if tipo[0] == 'linha':
        y = tipo[1] * CEL_SIZE + CEL_SIZE // 2
        canvas.create_line(20, y, CEL_SIZE * 3 - 20, y, fill='red', width=4, tag='vitoria')
    elif tipo[0] == 'coluna':
        x = tipo[1] * CEL_SIZE + CEL_SIZE // 2
        canvas.create_line(x, 20, x, CEL_SIZE * 3 - 20, fill='red', width=4, tag='vitoria')
    elif tipo == ('diagonal', 'principal'):
        canvas.create_line(20, 20, CEL_SIZE * 3 - 20, CEL_SIZE * 3 - 20, fill='red', width=4, tag='vitoria')
    elif tipo == ('diagonal', 'secundaria'):
        canvas.create_line(CEL_SIZE * 3 - 20, 20, 20, CEL_SIZE * 3 - 20, fill='red', width=4, tag='vitoria')

def jogar_gui():
    tabuleiro = inicializar_tabuleiro()
    vez_ia = True  # Começa com a IA

    def atualizar():
        desenhar_XO(canvas, tabuleiro)
        
        # Estimar e mostrar chances
        v, e, d = estimar_chances(tabuleiro)
        label_chances.config(text=f"Vitoria: {v}%  |  Empate: {e}%  |  Derrota: {d}%")
        
        vencedor = verificar_vencedor(tabuleiro)
        if vencedor:
            if vencedor == 'X':
                placar['IA'] += 1
                status.config(text="Vencedor: IA (X)")
            else:
                placar['Humano'] += 1
                status.config(text="Vencedor: Humano (O)")
            tipo = encontrar_linha_vencedora(tabuleiro)
            if tipo:
                desenhar_linha_vencedora(canvas, tipo)
            canvas.unbind("<Button-1>")
            atualizar_placar()
        elif verificar_empate(tabuleiro):
            status.config(text="Empate!")
            canvas.unbind("<Button-1>")
        else:
            proxima = 'O' if vez_ia else 'X'
            status.config(text=f"Jogada de {proxima}")

    def jogada_ia():
        nonlocal vez_ia # Função pai
        i, j = melhor_jogada(tabuleiro)
        if i is not None: # Se ocorrer um erro em melhor
            tabuleiro[i][j] = 'X'
        atualizar()
        vez_ia = False

    def clique(event):
        nonlocal vez_ia
        if vez_ia:
            return
        row = event.y // CEL_SIZE
        col = event.x // CEL_SIZE
        if tabuleiro[row][col] != ' ':
            return

        tabuleiro[row][col] = 'O'
        atualizar()

        if not verificar_vencedor(tabuleiro) and not verificar_empate(tabuleiro):
            vez_ia = True
            canvas.after(300, jogada_ia)

    def reiniciar():
        nonlocal tabuleiro, vez_ia
        tabuleiro = inicializar_tabuleiro()
        vez_ia = True
        canvas.delete('all')
        desenhar_grade(canvas)
        desenhar_XO(canvas, tabuleiro)
        canvas.bind("<Button-1>", clique)
        status.config(text="Jogada de X (IA)")
        label_chances.config(text="")  # Zera a porcentagem
        canvas.after(300, jogada_ia)

    def atualizar_placar():
        label_placar.config(text=f"Placar - IA (X): {placar['IA']}  |  Humano (O): {placar['Humano']}")

    # Interface
    root = tk.Tk()
    root.title("Jogo da Velha - IA Minimax")
    root.resizable(False, False)
    
    label_placar = tk.Label(root, text="", font=('Arial', 14))
    label_placar.pack(pady=5)

    canvas = tk.Canvas(root, width=CEL_SIZE*3, height=CEL_SIZE*3)
    canvas.pack()
    desenhar_grade(canvas)

    status = tk.Label(root, text="Jogada de X (IA)", font=('Arial', 14))
    status.pack(pady=5)

    label_chances = tk.Label(root, text="", font=('Arial', 12))
    label_chances.pack(pady=5)

    botao_reiniciar = tk.Button(root, text="Reiniciar Partida", font=('Arial', 12), command=reiniciar)
    botao_reiniciar.pack(pady=5)

    canvas.bind("<Button-1>", clique)
    desenhar_XO(canvas, tabuleiro)
    atualizar_placar()

    root.after(300, jogada_ia)  # IA começa
    root.mainloop()

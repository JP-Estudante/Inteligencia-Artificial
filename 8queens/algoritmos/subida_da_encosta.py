from auxiliar.alg_utils import gerar_estado_inicial, custo
from auxiliar.metricas import qualidade

def gerar_todos_vizinhos(estado):
    "Gera todos os 56 vizinhos possíveis de um estado"
    vizinhos = []
    for col in range(8):
        linha_atual = estado[col] # Linha atual da rainha nessa coluna.
        for nova_linha in range(8): 
            if nova_linha != linha_atual: # Se for diferente da linha atual.
                novo_estado = estado[:] # Para não afetar o original.
                novo_estado[col] = nova_linha # Atribui nova posição para a rainha.
                vizinhos.append(novo_estado)
    return vizinhos

def subida_da_encosta_com_reinicio():
    melhor_qualidade = 0
    iteracoes = 0
    reinicios = 0

    while True:
        estado_atual = gerar_estado_inicial()      
        
        while True:
            iteracoes += 1
            custo_atual = custo(estado_atual)
            
            if custo_atual != 0:
                qualidade_atual = qualidade(estado_atual) # Atribui a qualidade atual a uma variável.
                melhor_qualidade = max(melhor_qualidade, qualidade_atual) # Veriifica se a qualidade atual é maior que a melhor qualidade.

            vizinhos = gerar_todos_vizinhos(estado_atual) 
            melhor_vizinho = min(vizinhos, key=custo) # Escolhe o vizinho de menor custo, chamando a função custo.
            custo_melhor = custo(melhor_vizinho) # Atribui o menor custo atual a uma variável.

            if custo_melhor < custo_atual:
                estado_atual = melhor_vizinho # Avança para o vizinho de menor custo, atualizando o estado atual.
            else:
                reinicios += 1
                break  # ótimo local → reinício aleatório.

        if custo(estado_atual) == 0: # Se o custo é zero, significa "solução encontrada".
            return estado_atual, iteracoes, melhor_qualidade, reinicios

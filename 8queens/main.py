from algoritmos.tempera_simulada import tempera_simulada
from algoritmos.subida_da_encosta import subida_da_encosta_com_reinicio
from algoritmos.algoritmo_genetico import algoritmo_genetico, configurar_parametros
from auxiliar.alg_utils import custo
from auxiliar.metricas import (
    medir_tempo_execucao,
    calcular_media_tempos,
    calcular_media_iteracoes,
    formatar_resultado_unitario,
    salvar_resultado_em_arquivo
)

# Dicionário de algoritmos com nome e função
algoritmos = {
    "Tempera Simulada": tempera_simulada,
    "Subida da Encosta": subida_da_encosta_com_reinicio,
    "Alg. Genético": algoritmo_genetico
}

def selecionar_algoritmo():
    print("Escolha o algoritmo para executar:")
    for i, nome in enumerate(algoritmos, start=1):
        print(f"{i}. {nome}")

    while True:
        try:
            escolha = int(input("Digite o número correspondente ao algoritmo: "))
            if 1 <= escolha <= len(algoritmos):
                if escolha == 3:
                    configurar_parametros()
                nome_algoritmo = list(algoritmos.keys())[escolha - 1]
                return nome_algoritmo, algoritmos[nome_algoritmo]
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def definir_num_execucoes():
    while True:
        try:
            vezes = int(input("Quantas execuções deseja realizar? "))
            if vezes > 0:
                return vezes
            else:
                print("Digite um número maior que 0.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def executar_varias_vezes(nome, func, vezes=10):
    sucesso = 0
    tempos_execucao = []
    iteracoes_execucao = []
    saida_resultados = []

    for i in range(vezes):
        @medir_tempo_execucao
        def executar():
            return func()

        resultado_bruto, tempo = executar()
        tempos_execucao.append(tempo)

        if nome == "Subida da Encosta":
            solucao, iteracoes, melhor_qualidade, reinicios = resultado_bruto
        else:
            solucao, iteracoes, melhor_qualidade = resultado_bruto
            reinicios = None
            
        iteracoes_execucao.append(iteracoes)
        valida = custo(solucao) == 0
        if valida:
            sucesso += 1

        resultado_formatado = formatar_resultado_unitario(
            i, reinicios, iteracoes, melhor_qualidade, tempo, valida, vezes
        )

        print(resultado_formatado)
        saida_resultados.append(resultado_formatado)

    media_tempo = calcular_media_tempos(tempos_execucao)
    media_iteracoes = calcular_media_iteracoes(iteracoes_execucao)
    
    resumo = [
        "\nResumo de Sucessos:",
        f"- {nome}: {sucesso}/{vezes} ✓",
        f"- Tempo médio: {media_tempo:.4f} segundos"
        f"\n- Iterações médias: {media_iteracoes:.2f}",
    ]

    print("\n".join(resumo))
    saida_resultados.extend(resumo)
    salvar_resultado_em_arquivo(saida_resultados)

if __name__ == "__main__":
    vezes = definir_num_execucoes()
    nome, func = selecionar_algoritmo()
    executar_varias_vezes(nome, func, vezes)
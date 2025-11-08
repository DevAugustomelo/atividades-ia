import statistics
from time import time
from a_genetico_tsp_atv_06 import criar_populacao_inicial, nova_geracao, GERACOES, NUMERO_EXECUCOES

POPULACAO_TAMANHO = 50  

# Função para executar o algoritmo com um número específico de indivíduos
def experimento_com_populacao(populacao_tamanho):
    global POPULACAO_TAMANHO  # Alterar o tamanho da população globalmente
    POPULACAO_TAMANHO = populacao_tamanho  # Atualiza o tamanho da população
    
    melhores_resultados = []
    melhores_distancias_por_geracao = []  # Lista para armazenar as melhores distâncias por geração
    
    # Inicia o experimento
    start_time = time()  # Marca o tempo de início
    
    for execucao in range(1, NUMERO_EXECUCOES + 1):
        populacao = criar_populacao_inicial()
        melhores_distancias_execucao = []
        
        for geracao in range(GERACOES):
            populacao = nova_geracao(populacao)
            melhor = populacao[0]
            melhores_distancias_execucao.append(melhor["fitness"])  # Armazena a melhor distância dessa geração
        
        # Registra o melhor resultado final
        populacao.sort(key=lambda ind: ind["fitness"])
        melhor = populacao[0]
        melhores_resultados.append(melhor["fitness"])
        melhores_distancias_por_geracao.append(melhores_distancias_execucao)  # Armazena o progresso
    
    tempo_execucao = time() - start_time  # Tempo total de execução
    
    # Calcula as métricas finais
    media = statistics.mean(melhores_resultados)
    desvio = statistics.stdev(melhores_resultados)
    
    return {
        "populacao_tamanho": populacao_tamanho,
        "tempo_execucao": tempo_execucao,
        "media_distancia": media,
        "desvio_distancia": desvio,
        "melhores_distancias_por_geracao": melhores_distancias_por_geracao
    }


# Função para exibir os resultados do experimento
def exibir_resultados(resultados):
    for resultado in resultados:
        print(f"\n=== Resultados para {resultado['populacao_tamanho']} indivíduos ===")
        print(f"Tempo de execução: {resultado['tempo_execucao']:.2f} segundos")
        print(f"Média das melhores distâncias: {resultado['media_distancia']:.2f} milhas")
        print(f"Desvio padrão: {resultado['desvio_distancia']:.2f} milhas")
        
        # Análise da velocidade de convergência
        distancias_por_geracao = resultado['melhores_distancias_por_geracao']
        melhor_geracao = [min(distancias) for distancias in distancias_por_geracao]  # Melhor em cada geração
        print("Melhor distância final por geração (velocidade de convergência):")
        for i, dist in enumerate(melhor_geracao):
            print(f"  Geração {i + 1}: {dist:.2f} milhas")
            
# Função principal do experimento
def realizar_experimento():
    # Tamanhos de população a serem testados
    tamanhos_populacao = [20, 50, 100]
    
    resultados = []
    
    # Executa os experimentos para cada tamanho de população
    for tamanho in tamanhos_populacao:
        resultado = experimento_com_populacao(tamanho)
        resultados.append(resultado)
    
    # Exibe os resultados finais do experimento
    exibir_resultados(resultados)


# Executa o experimento
realizar_experimento()

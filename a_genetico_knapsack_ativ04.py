import random




# ==============================================================================
# PROBLEMA DA MOCHILA (KNAPSACK PROBLEM)
# ==============================================================================

PESOS = [44, 46, 90, 72, 91, 40, 75, 35, 8, 54, 78, 40, 77, 15, 61, 17, 75, 29, 75, 63]
GANHOS = [92, 4, 43, 83, 84, 68, 92, 82, 6, 44, 32, 18, 56, 83, 25, 96, 70, 48, 14, 58]
CAPACIDADE_MAXIMA = 878

# O número de itens é a dimensão.
NUMERO_ITENS = len(PESOS)

# ==============================================================================
# PARÂMETROS DO ALGORITMO GENÉTICO
# ==============================================================================

TAMANHO_POPULACAO = 50       # Quantidade de soluções na população.
NUMERO_GERSACOES = 500       # Quantidade de ciclos de evolução.
TAMANHO_TORNEIO = 3          # Quantidade de indivíduos que competem na seleção.
TAXA_CROSSOVER = 0.8         # Probabilidade de ocorrer crossover entre os pais.
TAXA_MUTACAO = 0.02          # Probabilidade de um gene (bit) ser alterado.
QTD_ELITISMO = 2             # Quantidade dos melhores indivíduos que passam direto.
NUMERO_EXECUCOES = 30       # Quantidade de vezes que o AG será rodado para ter estatísticas.

# ==============================================================================
# FUNÇÕES BÁSICAS
# ==============================================================================

def calcular_fitness(individuo):
    """
    Calcula o ganho total e o peso total de um indivíduo (solução).
    Se o peso exceder a capacidade, o ganho (fitness) é 0.
    Retorna uma tupla: (ganho_total, peso_total)
    """
    peso_total = 0
    ganho_total = 0
    
    for i in range(NUMERO_ITENS):
        # Se o item foi escolhido (valor 1 no indivíduo)
        if individuo[i] == 1:
            peso_total += PESOS[i]
            ganho_total += GANHOS[i]

    if peso_total > CAPACIDADE_MAXIMA:
        return 0, peso_total 
        
    return ganho_total, peso_total


def gerar_individuo_aleatorio():
    """
    Cria uma solução inicial aleatória (lista binária).
    """
    individuo = []
    for _ in range(NUMERO_ITENS):
        individuo.append(random.randint(0, 1))
    return individuo


def gerar_populacao_inicial():
    """
    Cria a primeira população, um conjunto de soluções aleatórias.
    """
    populacao = []
    for _ in range(TAMANHO_POPULACAO):
        populacao.append(gerar_individuo_aleatorio())
    return populacao


def selecao_torneio(populacao, avaliacoes_fitness):
    """
    Seleciona o melhor indivíduo entre 'TAMANHO_TORNEIO' candidatos aleatórios.
    """
    # Combina indivíduos e suas avaliações
    populacao_com_fitness = list(zip(populacao, avaliacoes_fitness))
    
    # Escolhe candidatos aleatórios
    candidatos = random.sample(populacao_com_fitness, TAMANHO_TORNEIO)
    
    # Encontra o vencedor (maior ganho/fitness)
    # x[1][0] acessa o ganho_total
    vencedor = max(candidatos, key=lambda x: x[1][0])
    
    # Retorna APENAS o indivíduo
    return vencedor[0] 


def crossover_um_ponto(pai1, pai2):
    """
    Combina pais trocando genes a partir de um ponto de corte aleatório.
    """
    # Verifica a taxa de crossover
    if random.random() > TAXA_CROSSOVER:
        # Se não ocorrer, retorna cópias idênticas dos pais
        return pai1[:], pai2[:]
    
    # Escolhe o ponto de corte (entre o primeiro e o penúltimo gene)
    ponto_corte = random.randint(1, NUMERO_ITENS - 1)
    
    # Geração dos filhos
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    
    return filho1, filho2


def crossover_dois_pontos(pai1, pai2):
    """
    Combina pais trocando a seção entre dois pontos de corte aleatórios.
    """
    if random.random() > TAXA_CROSSOVER:
        return pai1[:], pai2[:]
        
    # Escolhe os pontos de corte garantindo que ponto1 < ponto2
    ponto1 = random.randint(1, NUMERO_ITENS - 2)
    ponto2 = random.randint(ponto1 + 1, NUMERO_ITENS - 1)
    
    # Filho 1: (Início do pai 1) + (Meio do pai 2) + (Fim do pai 1)
    filho1 = pai1[:ponto1] + pai2[ponto1:ponto2] + pai1[ponto2:]
    
    # Filho 2: (Início do pai 2) + (Meio do pai 1) + (Fim do pai 2)
    filho2 = pai2[:ponto1] + pai1[ponto1:ponto2] + pai2[ponto2:]
    
    return filho1, filho2


def crossover_uniforme(pai1, pai2):
    """
    Combina pais, decidindo aleatoriamente qual gene de qual pai será herdado.
    """
    if random.random() > TAXA_CROSSOVER:
        return pai1[:], pai2[:]
        
    filho1, filho2 = [], []
    for i in range(NUMERO_ITENS):
        # 50% de chance de trocar os genes dos pais para os filhos
        if random.random() < 0.5:
            filho1.append(pai1[i])
            filho2.append(pai2[i])
        else:
            filho1.append(pai2[i])
            filho2.append(pai1[i])
            
    return filho1, filho2


def mutacao_bit_flip(individuo):
    """
    Inverte (flipa) cada gene (bit) com uma pequena probabilidade (TAXA_MUTACAO).
    """
    for i in range(NUMERO_ITENS):
        if random.random() < TAXA_MUTACAO:
            # 1 - valor inverte o bit (0 vira 1, 1 vira 0)
            individuo[i] = 1 - individuo[i] 


# ==============================================================================
# FLUXO DE EVOLUÇÃO E EXECUÇÃO
# ==============================================================================

def evoluir_populacao(populacao_atual, funcao_crossover):
    """
    Aplica Elitismo, Seleção, Crossover e Mutação para criar a próxima geração.
    """
    # 1. Avalia a população
    avaliacoes_fitness = [calcular_fitness(ind) for ind in populacao_atual]
    
    # 2. Prepara para o Elitismo: Ordena por ganho (fitness)
    populacao_ordenada_com_fitness = list(zip(populacao_atual, avaliacoes_fitness))
    # Ordena pelo ganho (primeiro elemento do tuple de fitness), do maior para o menor
    populacao_ordenada_com_fitness.sort(key=lambda x: x[1][0], reverse=True)

    # 3. Aplica Elitismo: Os melhores vão direto para a próxima geração
    individuos_ordenados = [ind for ind, fit in populacao_ordenada_com_fitness]
    nova_populacao = individuos_ordenados[:QTD_ELITISMO]
    
    # 4. Cria novos indivíduos até atingir o TAMANHO_POPULACAO
    while len(nova_populacao) < TAMANHO_POPULACAO:
        # Seleção
        pai1 = selecao_torneio(populacao_atual, avaliacoes_fitness)
        pai2 = selecao_torneio(populacao_atual, avaliacoes_fitness)
        
        # Crossover
        filho1, filho2 = funcao_crossover(pai1, pai2)
        
        # Mutação (altera os filhos)
        mutacao_bit_flip(filho1)
        mutacao_bit_flip(filho2)
        
        # Adiciona filhos à nova população
        nova_populacao.append(filho1)
        if len(nova_populacao) < TAMANHO_POPULACAO:
            nova_populacao.append(filho2)
            
    return nova_populacao


def executar_ag_knapsack(funcao_crossover):
    """
    Executa o Algoritmo Genético por um número fixo de gerações.
    """
    populacao = gerar_populacao_inicial()
    melhor_individuo_geral = None
    melhor_fitness_geral = (0, 0) # (ganho, peso)

    for _ in range(NUMERO_GERSACOES):
        # Gera a próxima população
        populacao = evoluir_populacao(populacao, funcao_crossover)
        
        # Avalia a nova população para encontrar o melhor
        avaliacoes_fitness = [calcular_fitness(ind) for ind in populacao]
        
        # Encontra a melhor fitness (maior ganho) da geração
        melhor_fitness_geracao = max(avaliacoes_fitness, key=lambda x: x[0])
        
        # Atualiza o melhor global
        if melhor_fitness_geracao[0] > melhor_fitness_geral[0]:
            melhor_fitness_geral = melhor_fitness_geracao
            # Encontra o indivíduo correspondente ao melhor fitness
            indice_melhor = avaliacoes_fitness.index(melhor_fitness_geral)
            melhor_individuo_geral = populacao[indice_melhor]
            
    return melhor_fitness_geral, melhor_individuo_geral


def calcular_media_desvio(resultados):
    """
    Calcula a média e o desvio padrão de uma lista de resultados.
    """
    if not resultados:
        return 0, 0
    
    # Cálculo da Média
    soma = sum(resultados)
    media = soma / len(resultados)
    
    # Cálculo do Desvio Padrão
    soma_quadrados = sum([(x - media) ** 2 for x in resultados])
    variancia = soma_quadrados / len(resultados)
    desvio_padrao = variancia ** 0.5
    
    return media, desvio_padrao


def executar_instancia(funcao_crossover, nome_instancia):
    """
    Executa o AG 30 vezes e coleta as estatísticas de desempenho.
    """
    resultados_ganho = []
    print(f"Executando {nome_instancia}...")
    
    for exec_num in range(1, NUMERO_EXECUCOES + 1):
        melhor_f, melhor_ind = executar_ag_knapsack(funcao_crossover)
        resultados_ganho.append(melhor_f[0]) # Salva apenas o ganho (fitness)
        
        print(
            f"Execução {exec_num}: Melhor ganho = {melhor_f[0]}, "
            f"Peso = {melhor_f[1]}"
        )
        
    # Calcula e imprime as estatísticas
    media, desvio = calcular_media_desvio(resultados_ganho)
    
    print(f"\n--- {nome_instancia} - {NUMERO_EXECUCOES} Melhores fitness ---")
    print(resultados_ganho)
    print(f"Média fitness final: {media:.2f}")
    print(f"Desvio padrão fitness final: {desvio:.2f}\n")
    
    return resultados_ganho, media, desvio


def main():
    """
    Função principal que compara os diferentes tipos de crossover.
    """
    print("Iniciando comparação de Algoritmos Genéticos para o Problema da Mochila.")
    
    # 1. Crossover de Um Ponto
    resultados_um_ponto = executar_instancia(
        crossover_um_ponto, "AG Crossover Um Ponto"
    )
    
    # 2. Crossover de Dois Pontos
    resultados_dois_pontos = executar_instancia(
        crossover_dois_pontos, "AG Crossover Dois Pontos"
    )
    
    # 3. Crossover Uniforme
    resultados_uniforme = executar_instancia(
        crossover_uniforme, "AG Crossover Uniforme"
    )
    
    print("--- FIM DA EXECUÇÃO ---")


if __name__ == "__main__":
    main()
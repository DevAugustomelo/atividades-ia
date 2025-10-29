import random
import statistics
from tsp_problem_atv_05 import rota_valida, USA13



# ==============================================================================
# PROBLEMA DO CAIXEIRO VIAJANTE - TSP (TRAVELING SALESMAN PROBLEM)
# ==============================================================================


def distancia_total(rota, matriz_distancias):
    distancia_total = 0

    # Soma a distância entre as cidades percorridas na rota
    for i in range(len(rota) - 1):
        cidade_atual = rota[i]
        proxima_cidade = rota[i + 1]
        distancia_total += matriz_distancias[cidade_atual][proxima_cidade]
    return distancia_total

CIDADES = [
    "New York", "Los Angeles", "Chicago", "Minneapolis", "Denver", "Dallas",
    "Seattle", "Boston", "San Francisco", "St. Louis", "Houston", "Phoenix", "Salt Lake City"
]
# --------------------------------------------------------
# PARÂMETROS DO ALGORITMO GENÉTICO
# --------------------------------------------------------
NUM_CIDADES = len(USA13)
POPULACAO_TAMANHO = 50
GERACOES = 400
TAMANHO_TORNEIO = 3
TAXA_CROSSOVER = 0.9
TAXA_MUTACAO = 0.05
ELITISMO = 5
NUMERO_EXECUCOES = 30 

def gerar_rota_inicial():
    """Gera uma rota aleatória começando e terminando em 0 (Nova York)."""
    while True:
        # cria uma lista de cidades exceto a cidade inicial/final (0)
        cidades = list(range(1, NUM_CIDADES))
        # embaralha a lista de cidades sem repetições
        random.shuffle(cidades)
        # completa a rota inicial adicionando a cidade inicial/final (0)
        rota_inicial = [0] + cidades + [0]
        #obs: a forma que a rota inicial é gerada neste trecho já garante q ela é válida
        if rota_valida(rota_inicial, NUM_CIDADES):
            return rota_inicial


def fitness(rota):
    """O fitness é a distância total (quanto menor, melhor)."""
    return distancia_total(rota, USA13)


def selecao_torneio(populacao):
    """Seleciona um indivíduo usando torneio."""
    competidores = random.sample(populacao, TAMANHO_TORNEIO)
    competidores.sort(key=lambda ind: ind["fitness"])
    return competidores[0]  # melhor (menor distância)


def crossover_ox(pai1, pai2):
    """Order Crossover (OX)."""
    tamanho = len(pai1) - 2  # exclui a cidade inicial e final
    p1, p2 = random.sample(range(1, tamanho + 1), 2)
    inicio, fim = min(p1, p2), max(p1, p2)

    filho = [None] * (tamanho + 2)
    filho[0] = filho[-1] = 0

    # Copia o segmento do pai1
    filho[inicio:fim] = pai1[inicio:fim]

    # Preenche o restante mantendo a ordem do pai2
    pos = fim
    for cidade in pai2[1:-1]:
        if cidade not in filho:
            if pos == tamanho + 1:
                pos = 1
            filho[pos] = cidade
            pos += 1

    return filho


def mutacao_swap(rota):
    """Realiza mutação trocando duas cidades."""
    nova_rota = rota[:]
    if random.random() < TAXA_MUTACAO:
        i, j = random.sample(range(1, len(rota) - 1), 2)
        nova_rota[i], nova_rota[j] = nova_rota[j], nova_rota[i]
    return nova_rota


def criar_populacao_inicial():
    """Cria a população inicial."""
    populacao = []
    for _ in range(POPULACAO_TAMANHO):
        rota = gerar_rota_inicial()
        populacao.append({"rota": rota, "fitness": fitness(rota)})
    return populacao


def nova_geracao(populacao):
    """Cria uma nova geração com elitismo, crossover e mutação."""
    populacao.sort(key=lambda ind: ind["fitness"])
    nova_pop = populacao[:ELITISMO]  # mantém os melhores

    while len(nova_pop) < POPULACAO_TAMANHO:
        pai1 = selecao_torneio(populacao)
        pai2 = selecao_torneio(populacao)

        if random.random() < TAXA_CROSSOVER:
            filho_rota = crossover_ox(pai1["rota"], pai2["rota"])
        else:
            filho_rota = pai1["rota"][:]

        filho_rota = mutacao_swap(filho_rota)
        nova_pop.append({"rota": filho_rota, "fitness": fitness(filho_rota)})

    return nova_pop


# --------------------------------------------------------
# EXECUÇÃO PRINCIPAL (30 REPETIÇÕES)
# --------------------------------------------------------
melhores_resultados = []

for execucao in range(1, NUMERO_EXECUCOES + 1):
    populacao = criar_populacao_inicial()

    for _ in range(GERACOES):
        populacao = nova_geracao(populacao)

    populacao.sort(key=lambda ind: ind["fitness"])
    melhor = populacao[0]
    melhores_resultados.append(melhor["fitness"])
    rota_nomes = " -> ".join(CIDADES[i] for i in melhor["rota"])

    print(f"Execução {execucao:02d}:")
    print(f"  Melhor rota: {melhor['rota']}")
    print(f"  Cidades: {rota_nomes}")
    print(f"  Menor distância: {melhor['fitness']} milhas")
    print("-" * 60)

media = statistics.mean(melhores_resultados)
desvio = statistics.stdev(melhores_resultados)

print("\n=== RESULTADOS FINAIS ===")
print(f"Média das melhores distâncias: {media:.2f} milhas")
print(f"Desvio padrão: {desvio:.2f} milhas")


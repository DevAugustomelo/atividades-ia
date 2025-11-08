import random
import statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.patheffects as pe
import seaborn as sns
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


def main():
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

    # =============================================================
    # GRÁFICO DE CONVERGÊNCIA (MELHOR FITNESS POR EXECUÇÃO)
    # =============================================================
    # sns.set_theme(style="whitegrid", context="notebook", palette="viridis")

    # plt.rcParams.update({
    #     "figure.figsize": (12, 7),
    #     "axes.titlesize": 18,
    #     "axes.labelsize": 14,
    #     "xtick.labelsize": 12,
    #     "ytick.labelsize": 12,
    #     "legend.fontsize": 12,
    #     "lines.linewidth": 2.5,
    #     "axes.edgecolor": "#444444",
    #     "axes.linewidth": 1.2
    # })


    # execucoes = np.arange(1, len(melhores_resultados) + 1)
    # fit =  np.array(melhores_resultados)

    # fig, ax = plt.subplots()

    # ax.plot(
    #     execucoes,
    #     fit,
    #     color=sns.color_palette("crest")[4],
    #     linewidth=2.5,
    #     label="Melhor fitness por execução",
    #     path_effects=[pe.SimpleLineShadow(alpha=0.4), pe.Normal()]
    # )

    # # Marcadores com cor distinta
    # ax.scatter(
    #     execucoes,
    #     fit,
    #     color=sns.color_palette("flare", 10)[6],
    #     s=70,
    #     zorder=3,
    #     label="Execuções individuais"
    # )

    # ax.set_title("Convergência do Algoritmo Genético\nMelhor Fitness por Execução", pad=20)
    # ax.set_xlabel("Execução")
    # ax.set_ylabel("Melhor distância (milhas)")

    # ax.legend(frameon=True, loc="best", fancybox=True)
    # ax.grid(True, linestyle="--", alpha=0.5)

    # for spine in ["top", "right"]:
    #     ax.spines[spine].set_visible(False)



    # ax.text(
    #     0.02, -0.12,
    #     f"População: {POPULACAO_TAMANHO} | Gerações: {GERACOES} | Execuções: {NUMERO_EXECUCOES}",
    #     transform=ax.transAxes,
    #     fontsize=10,
    #     color="#555555"
    # )

    # fig.tight_layout()
    # plt.show()



    # =============================================================
    # CONFIGURAÇÃO DE ESTILO
    # =============================================================
    sns.set_theme(style="whitegrid", context="notebook", palette="crest")

    plt.rcParams.update({
        "figure.figsize": (10, 9),
        "axes.titlesize": 18,
        "axes.titleweight": 'bold',
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "axes.edgecolor": "#444",
        "axes.linewidth": 1.2
    })

    # =============================================================
    # DADOS
    # =============================================================
    execucoes = np.arange(1, len(melhores_resultados) + 1)
    fit= np.array(melhores_resultados)

    # =============================================================
    # SUBPLOTS: 2 GRÁFICOS (CONVERGÊNCIA + BOXPLOT)
    # =============================================================
    # fig, (ax1, ax2) = plt.subplots(2, 1, sharex=False, height_ratios=[3, 1.2], figsize=(10, 10))
    # fig.subplots_adjust(hspace=0.45)

    fig = plt.figure(constrained_layout=False, figsize=(10, 9))
    gs = gridspec.GridSpec(
        2, 1,             # 2 linhas, 1 coluna
        height_ratios=[3, 1.2],  # proporção entre os gráficos
        hspace=0.5        # espaço vertical entre eles
    )
    # Cria os eixos com base no grid
    ax1 = fig.add_subplot(gs[0, 0])  # gráfico de convergência
    ax2 = fig.add_subplot(gs[1, 0])  # gráfico boxplot


    # -------------------------------------------------------------
    # 1️⃣ GRÁFICO DE CONVERGÊNCIA
    # -------------------------------------------------------------
    ax1.plot(
        execucoes,
        fit,
        color=sns.color_palette("crest")[4],
        linewidth=2.5,
        label="Melhor fitness por execução",
        path_effects=[pe.SimpleLineShadow(alpha=0.4), pe.Normal()]
    )

    ax1.scatter(
        execucoes,
        fit,
        color=sns.color_palette("flare", 10)[5],
        s=70,
        zorder=3,
        label="Execuções individuais"
    )

    # Tendência linear
    z = np.polyfit(execucoes, fit, 1)
    trend = np.poly1d(z)
    ax1.plot(
        execucoes,
        trend(execucoes),
        color="#E76F51",
        linestyle="--",
        linewidth=1.8,
        label="Tendência linear"
    )

    ax1.set_title("Convergência do Algoritmo Genético", fontweight='bold', pad=15)
    ax1.set_ylabel("Melhor distância (milhas)")
    ax1.set_xlabel("Execução")
    ax1.legend(frameon=True, loc="best", fancybox=True)
    ax1.grid(True, linestyle="--", alpha=0.5)

    for spine in ["top", "right"]:
        ax1.spines[spine].set_visible(False)


    ax1.text(
        0.02, -0.12,
        f"População: {POPULACAO_TAMANHO} | Gerações: {GERACOES} | Execuções: {NUMERO_EXECUCOES}",
        transform=ax1.transAxes,
        fontsize=10,
        color="#555555"
    )
    # -------------------------------------------------------------
    # 2️⃣ BOXPLOT DA DISTRIBUIÇÃO FINAL
    # -------------------------------------------------------------
    sns.boxplot(
        y=fit,
        width=0.3,
        color=sns.color_palette("crest")[4],
        boxprops={"alpha": 0.8, "linewidth": 1.2},
        medianprops={"color": "#E76F51", "linewidth": 2},
        whiskerprops={"linewidth": 1.2},
        capprops={"linewidth": 1.2},
        flierprops={"marker": "o", "color": "#243FD8", "alpha": 0.8, "markersize": 7},
        ax=ax2
    )


    sns.stripplot(
        y=fit,
        color=sns.color_palette("flare", 10)[5],
        alpha=0.7,
        jitter=0.18,     # espalhamento horizontal
        size=6,
        zorder=3,
        ax=ax2
    )


    ax2.set_title("Distribuição dos Melhores Fitness", pad=10)
    ax2.set_ylabel("Distância (milhas)")
    ax2.set_xticks([])

    # Estatísticas
    media = np.mean(fit)
    mediana = np.median(fit)
    desvio = np.std(fit)

    ax2.text(
        0.05, 0.95,
        f"Média: {media:.2f}\nMediana: {mediana:.2f}\nDesvio: {desvio:.2f}",
        transform=ax2.transAxes,
        fontsize=10,
        color="#333333",
        verticalalignment="top",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="#AAAAAA")
    )

    for spine in ["top", "right"]:
        ax2.spines[spine].set_visible(False)

    # =============================================================
    # LAYOUT FINAL
    # =============================================================
    fig.suptitle("Análise de Desempenho do Algoritmo Genético (TSP)", fontsize=20, y=2.02)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
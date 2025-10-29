# TSP https://developers.google.com/optimization/routing/tsp#python

# 0. New York - 1. Los Angeles - 2. Chicago - 3. Minneapolis - 4. Denver - 5. Dallas - 6. Seattle -
# 7. Boston - 8. San Francisco - 9. St. Louis - 10. Houston - 11. Phoenix - 12. Salt Lake City
# New York is the start and end location. Distance is measured in miles.


USA13 = [
    [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
    [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
]


def distancia_total(rota, matriz_distancias):
    distancia_total = 0

    # Soma a distância entre as cidades percorridas na rota
    for i in range(len(rota) - 1):
        cidade_atual = rota[i]
        proxima_cidade = rota[i + 1]
        distancia_total += matriz_distancias[cidade_atual][proxima_cidade]
        print(
            f"distancia parcial: {matriz_distancias[cidade_atual][proxima_cidade]} milhas"
        )
        print(f"Até agora: {distancia_total} milhas")

    return distancia_total


def rota_valida(rota, num_cidades):
    """
    Uma rota é válida se:
      - Começa e termina na mesma cidade.
      - Todas as outras cidades são visitadas exatamente uma vez.
      - Não há cidades fora do intervalo permitido (0 até num_cidades - 1).
    """
    # Verifica se a rota não está vazia
    if not rota:
        print("Rota vazia.")
        return False

    # Deve começar e terminar na mesma cidade
    if rota[0] != rota[-1]:
        print("Rota não começa e termina na mesma cidade.")
        return False

    # Remove a última cidade (pois é igual à primeira)
    cidades_visitadas = rota[:-1]

    # Cria um conjunto de itens únicos a partir de uma lista e compara se há duplicatas (todas devem ser únicas)
    if len(cidades_visitadas) != len(set(cidades_visitadas)):
        print("Rota contém cidades duplicadas.")
        return False

    # Verifica se todas as cidades estão dentro do intervalo permitido
    for cidade in cidades_visitadas:
        if cidade < 0 or cidade >= num_cidades:
            print(f"Cidade {cidade} está fora do intervalo permitido.")
            return False

    return True


if __name__ == "__main__":
    # Exemplo de uso
    rota_exemplo = [0, 1, 2, 3, 0]
    num_cidades = len(USA13)

    if rota_valida(rota_exemplo, num_cidades):
        distancia = distancia_total(rota_exemplo, USA13)
        print(f"A distância total da rota {rota_exemplo} é: {distancia} milhas.")
    else:
        print("A rota fornecida não é válida.")

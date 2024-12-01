#############
#  IMPORTS  #
#############
import pandas as pd
import pickle
from Class.player import Player
from Class.genetic import AlgoritmoGenetico
import matplotlib.pyplot as plt

csv_path = "data/player_ratings_teste.csv"

#######################
#  Pre-Processamento  #
#######################


def pre_processamento_inicial():
    """
      Pre-processamento a partir do CSV.

      Retorna:
      list: Lista com todos as linhas do csv
    """

    df = pd.read_csv(csv_path)

    player_list = []

    for index, row in df.iterrows():

        player = Player(int(row["account_id"]), int(
            row["total_matches"]), round(row["trueskill_mu"], 2), round(row["trueskill_sigma"], 2))
        player_list.append(player)

    with open('data/lista_players.pkl', 'wb') as f:
        pickle.dump(player_list, f)

    return player_list


def pre_processamento_realizada():
    """
      Pre-processamento lendo o arquivo pkl já processado.
      Retorna:
      list: Lista com todos as linhas do csv
    """

    with open('data/lista_players.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":

    ####################
    # Hyper Parametros #
    ####################

    # player_list = pre_processamento_inicial()
    player_list = pre_processamento_realizada()

    print(f'Quantidade de registros {len(player_list)}')

    tamanho_populacao = 2000
    numero_de_geracoes = 100
    taxa_de_mutacao = 0.1

    ag = AlgoritmoGenetico(tamanho_populacao=tamanho_populacao)
    ag.resolver(taxa_mutacao=taxa_de_mutacao, numero_geracoes=numero_de_geracoes,
                lista_jogadores=player_list)

    plt.plot(ag.lista_de_solucoes)
    plt.title("Lista de SoluçÕes Partida Dota 2")
    plt.savefig("resultados_algoritmo_genético")

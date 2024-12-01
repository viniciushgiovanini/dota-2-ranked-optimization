#############
#  IMPORTS  #
#############
import pandas as pd
import pickle
from Class.player import Player
from Class.individuo import Individuo

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

    player_list = pre_processamento_inicial()
    # player_list = pre_processamento_realizada()

    print(f'Quantidade de registros {len(player_list)}')

    individuo1 = Individuo(jogadores=player_list)
    individuo1.avaliacao()

    individuo2 = Individuo(jogadores=player_list)
    individuo2.avaliacao()

    # print(f"Cromossomo individuo 1: {individuo1.cromossomos}")

    # print(f"Cromossomo individuo 2: {individuo2.cromossomos}")

    # crossover = individuo1.crossover(individuo2)
    # print(f"Cromossomo crossover: {crossover[0].cromossomos}")

    # individuo1.mutacao(taxa_mutacao=0.25)

    str("")

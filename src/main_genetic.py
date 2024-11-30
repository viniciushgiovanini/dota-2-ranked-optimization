#############
#  IMPORTS  #
#############
import pandas as pd
import pickle
from Class.player import Player
from Class.individuo import Individuo

csv_path = "data/player_ratings.csv"

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

    # player_list = pre_processamento_inicial()
    player_list = pre_processamento_realizada()

    print(f'Quantidade de registros {len(player_list)}')

    player_list[-1].visualizarJogador()

    total_wins = []
    total_matches = []
    trueskill_mu = []
    trueskill_sigma = []

    for each in player_list:
        total_wins.append(each.getTotalWins())
        total_matches.append(each.getTotalWins())
        trueskill_mu.append(each.getTrueskillmu())
        trueskill_sigma.append(each.getTrueskillsigma())

    individuos1 = Individuo(total_wins=total_wins, total_matches=total_matches,
                            skill_mu=trueskill_mu, skill_sigma=trueskill_sigma)

    print(f"Quantidade de Cromossomos: {len(individuos1.cromossomos)}")

    cont = 0
    for each in individuos1.cromossomos:
        if each == 1:
            cont = cont + 1

    print(f"Quantidade de jogadores que vão {cont}")

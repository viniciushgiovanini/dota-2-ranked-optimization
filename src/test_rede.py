import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import random
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns


def predict_data(model, csv_path):
    '''
    Método que realiza a previsão do TrueSkill_MU

    Param:
      - model(obj): recebe o modelo treinado
      - csv_path(str): Recebe o path do csv de teste

    Return:
      - resp_dataframe (dataframe): Csv contendo 2 colunas, TrueSkillMU original e predito para plot
      - X_test (dataframe): Csv de teste, com agora a coluna TrueSkillMU sendo a predita
    '''

    model = load_model(model)

    test = pd.read_csv(csv_path)

    print(f"Quantidade de dados no test: {len(test)}")

    X_test = test.drop("trueskill_mu", axis=1)
    Y_test = test[['trueskill_mu']]

    scaler = StandardScaler()
    X_test_scaled = scaler.fit_transform(X_test)

    resp_dataframe = pd.DataFrame()

    previsoes = model.predict(X_test_scaled).flatten()

    resp_dataframe['trueskill_mu_predict'] = previsoes
    resp_dataframe["trueskill_mu_correct"] = Y_test
    X_test["trueskill_mu_predict"] = previsoes

    # df_compare = X_test
    # df_compare["trueskill_mu"] = Y_test
    # df_compare["trueskill_mu_predict"] = previsoes
    # df_compare.to_csv("data/csv_comparacao.csv")

    return resp_dataframe, X_test


def generate_best_matches(df_matches, group_size=10, qtd_partidas=10):
    '''
    Metodo para gerar as combinações aleatorias de jogadores

    Param:
      - df_mathes(df): Csv de teste, contendo a coluna de TrueSkill_Mu predita
      - group_size(int): Quantidade de players por partida
      - qtd_partidas(int): Quantidade de partidas

    Return:
      - list_partida(list): Retorna uma lista contendo uma ou mais partidas 10x10 jogadores
    '''

    best_group = None
    best_score = -np.inf
    list_partida = []

    random.seed(42)
    sampled_groups = [random.sample(list(df_matches.index), group_size)
                      for _ in range(qtd_partidas)]

    for i, group in enumerate(sampled_groups):
        group_data = df_matches.loc[group]
        group_mu = group_data["trueskill_mu_predict"].mean()
        group_sigma = group_data["trueskill_sigma"].mean()
        score = round(group_mu - 0.5 * group_sigma, 2)

        match_dict = {}

        match_dict = {
            "id_partida": i,
            "score": score,
            "mu_mean": group_mu,
            "sigma_mean": group_sigma,
            "group": group
        }

        list_partida.append(match_dict.copy())

    list_partida = sorted(list_partida, key=lambda x: x["score"], reverse=True)

    return list_partida


def plot_graph(df_graph):
    '''
    Método para plot do scatterplot

    Param:
      - df_graph(df): Csv com apenas colunas TrueSkill_Mu Predita e Original

    '''

    plt.figure(figsize=(8, 8))
    sns.scatterplot(
        x='trueskill_mu_correct',
        y='trueskill_mu_predict',
        data=df_graph,
        color='blue',
        label='Previsões'
    )

    plt.plot(
        [df_graph['trueskill_mu_correct'].min(
        ), df_graph['trueskill_mu_correct'].max()],
        [df_graph['trueskill_mu_correct'].min(
        ), df_graph['trueskill_mu_correct'].max()],
        color='red',
        linestyle='--',
        label='Linha x = y'
    )

    plt.title('Comparação entre Previsões e Valores Reais')
    plt.xlabel('TrueSkill Mu (Real)')
    plt.ylabel('TrueSkill Mu (Previsto)')
    plt.legend()
    plt.grid()
    plt.savefig("graph/scatterplot_previsoes.png")


def visualizar_jogadores_por_partida(dict_partida, df_matches):
    '''
    Método para visualizar os dados de cada jogador de uma partida

    Param:
      - dict_partida(Dicionario): Um dicionario contendo um registro de uma partida
      - df_matches(df): Csv de teste contendo coluna de Mu prevista pela rede

    '''

    players_selecionados_indices = dict_partida["group"]

    id_partida = dict_partida["id_partida"]

    print(f"----- Partida {id_partida} -----\n")

    for i, each in enumerate(players_selecionados_indices):
        registro_jogador = df_matches.iloc[each]
        wins = registro_jogador["total_wins"]
        acc_id = registro_jogador["account_id"]
        total_matches = registro_jogador["total_matches"]
        mu = registro_jogador["trueskill_mu_predict"]
        sigma = registro_jogador["trueskill_sigma"]

        print(f"\n\nJogador {i} ---> Id: {acc_id} | Total de Vitórias: {wins} | Total de Partidas: {total_matches} | TrueSkill_MU: {mu} | TrueSkill_Sigma: {sigma}")


def visualizar_partidas(lista_de_partidas, df_matches):
    '''
    Método para visualizar as partidas selecionadas

    Param:
      - lista_de_partidas(List): Uma lista contendo as partidas selecionadas randomicamente
      - df_matches(df): Csv de teste contendo coluna de Mu prevista pela rede

    '''

    high_matches = []
    mid_matches = []
    low_matches = []

    for each in lista_de_partidas:

        if each["score"] <= 24.5:
            low_matches.append(each)
        elif each["score"] > 24.5 and each["score"] <= 26:
            mid_matches.append(each)
        elif each["score"] > 26:
            high_matches.append(each)

    print("----- Partidas Rankeds Altas -----\n")
    for each in high_matches:
        identificador = each["id_partida"]
        score = each["score"]
        print(f"ID Partida: {identificador}\nScore: {score}\n\n")

    print("----- Partidas Rankeds Medias -----\n")
    for each in mid_matches:
        identificador = each["id_partida"]
        score = each["score"]
        print(f"ID Partida: {identificador}\nScore: {score}\n\n")

    print("----- Partidas Rankeds Baixas -----\n")
    for each in low_matches:
        identificador = each["id_partida"]
        score = each["score"]
        print(f"ID Partida: {identificador}\nScore: {score}\n\n")

    id_melhor_partida = lista_de_partidas[0]["id_partida"]
    score_melhor_partida = lista_de_partidas[0]["score"]

    print(
        f'Partida balanceada com nível mais alto: ID Partida: {id_melhor_partida}\nScore: {score_melhor_partida}')

    visualizar_jogadores_por_partida(lista_de_partidas[0], df_matches)


if __name__ == "__main__":

    model_path = "models/shurupitas.h5"
    csv_path = "data/player_teste.csv"

    df_graph, df_test = predict_data(model=model_path, csv_path=csv_path)

    # plot_graph(df_graph=df_graph)
    lista_partidas = generate_best_matches(
        df_matches=df_test, qtd_partidas=200)
    visualizar_partidas(
        lista_de_partidas=lista_partidas, df_matches=df_test)

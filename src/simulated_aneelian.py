import pandas as pd
import numpy as np
import random

np.random.seed(42)
df = pd.read_csv("data/player_teste.csv")


def calcular_score(jogadores):
    media_mu = jogadores["trueskill_mu"].mean()
    media_sigma = jogadores["trueskill_sigma"].mean()
    return media_mu - 0.5 * media_sigma


def simulated_annealing(df, team_size=10, initial_temperature=100, cooling_rate=0.95):
    current_team = df.sample(team_size)
    current_score = calcular_score(current_team)

    best_team = current_team
    best_score = current_score

    temperature = initial_temperature

    while temperature > 0.1:

        print(f"Valor atual da temperatura: {temperature}")

        new_team = current_team.copy()
        new_player = df.sample(1)
        replace_idx = random.randint(0, team_size - 1)
        new_team.iloc[replace_idx] = new_player.iloc[0]
        new_score = calcular_score(new_team)

        delta_score = new_score - current_score

        if delta_score > 0 or np.exp(delta_score / temperature) > random.random():
            current_team = new_team
            current_score = new_score

        if current_score > best_score:
            best_team = current_team
            best_score = current_score

        temperature *= cooling_rate

    return best_team, best_score


melhor_time, melhor_score = simulated_annealing(
    df, team_size=10, initial_temperature=1000)

print("Melhor score:", melhor_score)
print("Melhor time:")
print(melhor_time)

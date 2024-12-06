import pandas as pd
from itertools import combinations
import time

def calculate_score(mu, sigma):
    return mu - 0.5 * sigma

def branch_and_bound(players, target_size=10):
    players['score'] = calculate_score(players['trueskill_mu'], players['trueskill_sigma'])
    players = players.sort_values(by='score', ascending=False).reset_index(drop=True)

    best_combination = None
    best_score_diff = float('inf')

    def explore_branch(selected, remaining):
        nonlocal best_combination, best_score_diff

        if len(selected) == target_size:
            current_score = sum(players.loc[selected, 'score'])
            score_diff = abs(current_score - sum(players.loc[remaining, 'score']))
            if score_diff < best_score_diff:
                best_score_diff = score_diff
                best_combination = selected[:]
            return

        for i in range(len(remaining)):
            next_selected = selected + [remaining[i]]
            next_remaining = remaining[i+1:]
            
            if abs(sum(players.loc[next_selected, 'score']) - sum(players.loc[next_remaining, 'score'])) < best_score_diff:
                explore_branch(next_selected, next_remaining)

    explore_branch([], list(range(len(players))))
    return players.loc[best_combination]

file_path = "data/player_teste.csv"
players = pd.read_csv(file_path)

start_time = time.time()
best_team = branch_and_bound(players)
end_time = time.time()

tempo_execucao = end_time - start_time
tempo_execucao_minutos = tempo_execucao / 60
print(f"Tempo de execução: {tempo_execucao_minutos:.6f} minutos")

print(best_team)

import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import random
from itertools import combinations

model = load_model("models/shurupitas.h5")

test = pd.read_csv("data/player_teste.csv")

X_test = test[['total_wins', 'total_matches',
               'trueskill_mu', 'trueskill_sigma']]


scaler = StandardScaler()
X_test_scaled = scaler.fit_transform(X_test)

# O impact score é a media do player entre trueskill mu e sigma penalizado
test['impact_score'] = model.predict(X_test_scaled).flatten()

# Criar combinações de 10 jogadores
group_size = 10
# indices = list(test.index)
# groups = list(combinations(indices, group_size))

# Avaliar os grupos
best_group = None
best_score = -np.inf


random.seed(42)
sampled_groups = [random.sample(list(test.index), group_size)
                  for _ in range(20)]

for group in sampled_groups:
    group_data = test.loc[group]
    group_mu = group_data["trueskill_mu"].mean()
    group_sigma = group_data["trueskill_sigma"].mean()
    score = round(group_mu - 0.5 * group_sigma, 2)
    if score > best_score:
        best_score = score
        best_group = group

# Exibir o melhor grupo
print("Melhor grupo (índices):", best_group)
print("Melhor score:", best_score)

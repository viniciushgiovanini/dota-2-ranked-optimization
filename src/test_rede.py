import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

model = load_model("models/shurupitas.h5")

data = pd.read_csv("data/player_ratings.csv")
data = data[data["total_matches"] >= 10]
real_values = data["truskill_mu"].values

test = data.iloc[40000:]
test = test[['total_wins', 'total_matches', 'trueskill_mu', 'trueskill_sigma']].drop(columns=["trueskill_mu"])

scaler = StandardScaler()
validation_data = scaler.fit_transform(test)

predictions = model.predict(test)

plt.title('Comparação entre Valores Reais e Previstos')
plt.xlabel('Índice')
plt.ylabel('Trueskill Mu')
plt.legend()
plt.grid(True)
plt.savefig('teste_rede.png')
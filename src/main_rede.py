import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt
from tensorflow.keras.metrics import MeanAbsoluteError
from tensorflow.keras.losses import MeanSquaredError

################################################################
# A REDE TEM QUE CLASSIFICAR O TRUESKILL_MU e NAO O impact_SCORE
################################################################


data = pd.read_csv("data/player_treinamento.csv")

data["impact_score"] = data["trueskill_mu"] - 0.5 * data["trueskill_sigma"]

X = data[['total_wins', 'total_matches', 'trueskill_mu', 'trueskill_sigma']]
y = data["impact_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


model = Sequential([
    Dense(64, input_dim=X_train.shape[1], activation='relu'),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss=MeanSquaredError(),
              metrics=[MeanAbsoluteError()])


history = model.fit(X_train, y_train, validation_split=0.2,
                    epochs=5, batch_size=16, verbose=1)


model.save("models/shurupitas.h5")


loss, mae = model.evaluate(X_test, y_test)
print(f"Mean Absolute Error: {mae}")

plt.figure(figsize=(10, 5))
plt.plot(history.history['mean_absolute_error'], label='Mae Treinamento')
plt.plot(history.history['val_mean_absolute_error'], label='Mae Validação')
plt.title('Perda (Mae) durante o Treinamento e Validação')
plt.xlabel('Épocas')
plt.ylabel('Mae')
plt.legend()
plt.grid(True)
plt.savefig('graph/grafico_mae.png')

plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Loss Treinamento')
plt.plot(history.history['val_loss'], label='Loss Validação')
plt.title('Loss durante o Treinamento e Validação')
plt.xlabel('Épocas')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.savefig('graph/grafico_loss.png')

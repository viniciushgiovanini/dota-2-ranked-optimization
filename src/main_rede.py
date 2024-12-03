import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanAbsoluteError

data = pd.read_csv("data/player_ratings.csv")
data = data[data["total_matches"] >= 10]


validation = data.iloc[40000:]

data = data.iloc[:40000]

def define_mmr_category(mu):
    if mu < 25:
        return 0  
    elif 25 <= mu < 30:
        return 1  
    else:
        return 2  


X = data[['total_wins', 'total_matches', 'trueskill_mu', 'trueskill_sigma']].drop(columns=["trueskill_mu"])
y = data['trueskill_mu']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = Sequential([
    Dense(1024, input_dim=X_train.shape[1], activation='relu'),
    Dense(512, activation='relu'),
    Dense(256, activation='relu'),
    # Dropout(0.3),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    # Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(4, activation='relu'),
    Dense(1)
])

model.compile(optimizer=Adam(learning_rate=0.002),
              loss=MeanSquaredError(),
              metrics=[MeanAbsoluteError()])

model.summary()


history = model.fit(X_train, y_train, validation_split=0.2, epochs=200, batch_size=16, verbose=1)

model.save("shurupitas.h5")

loss, mae= model.evaluate(X_test, y_test)
print(f"Mae no teste: {mae * 100:.2f}%")

plt.figure(figsize=(10, 5))
plt.plot(history.history['mae'], label='Mae Treinamento')
plt.plot(history.history['val_mae'], label='Mae Validação')
plt.title('Perda (Mae) durante o Treinamento e Validação')
plt.xlabel('Épocas')
plt.ylabel('Mae')
plt.legend()
plt.grid(True)
plt.savefig('grafico_mae.png') 

plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Loss Treinamento')
plt.plot(history.history['val_loss'], label='Loss Validação')
plt.title('Loss durante o Treinamento e Validação')
plt.xlabel('Épocas')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.savefig('grafico_loss.png')
import pandas as pd


df = pd.read_csv("../../data/player_ratings.csv")
df = df[df["total_matches"] > 5]

meio = int(len(df)/2)

print(f"Quantidade registros csv original {len(df)}\nMeio é {meio}")

csv_treinamento = df.iloc[:meio]
csv_test = df.iloc[meio:]

print(f"Quantidade registro csv treinamento: {len(csv_treinamento)}")
print(f"Quantidade registro csv test: {len(csv_test)}")

csv_treinamento.to_csv("../../data/player_treinamento.csv")
csv_treinamento.to_csv("../../data/player_teste.csv")

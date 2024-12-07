import pandas as pd
import gdown
import shutil


id = "163sVkZHux_lEwvzFaxryftfnFuVKh0Aq"
gdown.download(id=id, output="player_ratings.csv")
shutil.move("player_ratings.csv", "data/")

df = pd.read_csv("data/player_ratings.csv")
df = df[df["total_matches"] > 5]

meio = int(len(df)/2)

print(f"Quantidade registros csv original {len(df)}\nMeio é {meio}")

csv = df.iloc[:meio]

print(f"Quantidade registro csv reduzido: {len(csv)}")

csv.to_csv("data/player_teste.csv")

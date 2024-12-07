# Balanceamento de Partidas de Dota 2

## Alunos

- João Pedro Lobato
- Vinícius Henrique Giovanini

## Conjunto de dados

O conjunto de dados pode ser encontrado [clicando aqui](https://www.kaggle.com/datasets/devinanzelmo/dota-2-matches?select=player_ratings.csv), **mas o código já realiza o download e o preprocessamento automatico**, foi utilizado somente o CSV de habilidade de jogadores denominado player_ratings.csv.

## Como rodar os algoritmos de otimização

- Baixe as depêndencias do projeto com pip

```
pip install -r requirements.txt
```

- Baixe o dataset e rode o preprocessamento, o dataset original é o **player_ratings.csv**, mas ele foi dividido ao meio.

```
python ./src/preprocessing.py
```

- Para rodar o algoritmo Genético, o arquivo principal chama **main_genetic.py**, e as classes estão da pasta Class.

```
python ./src/main_genetic.py
```

- Para rodar o algoritmo B&B, o arquivo principal chama **main_bnb.py**.

```
python ./src/main_bnb.py
```

- Para rodar o algoritmo Simulated Annealing, o arquivo principal chama **simulated_aneelian.py**

```
python ./src/simulated_aneelian.py
```

## Resultados

- Os resultados podem ser encontrados no diretório abaixo em arquivos texto.

```
resultados/*
```

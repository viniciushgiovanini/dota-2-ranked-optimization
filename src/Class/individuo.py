from random import random


class Individuo():
    def __init__(self, total_wins, total_matches, skill_mu, skill_sigma, geracao=0):
        self.total_wins = total_wins,
        self.total_matches = total_matches
        self.skill_mu = skill_mu
        self.skiil_sigma = skill_sigma
        self.nota_avaliacao = 0
        self.geracao = geracao
        self.cromossomos = []

        for i in range(len(total_wins)):
            if random() < 0.5:
                self.cromossomos.append(0)
            else:
                self.cromossomos.append(1)

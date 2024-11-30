class Player:
    def __init__(self, acc_id, total_wins, trueskill_mu, trueskill_sigma):
        self.acc_id = acc_id
        self.total_wins = total_wins
        self.trueskill_mu = trueskill_mu
        self.trueskill_sigma = trueskill_sigma

    def getAccId(self):
        return self.acc_id

    def getTotalWins(self):
        return self.total_wins

    def getTrueskillmu(self):
        return self.trueskill_mu

    def getTrueskillsigma(self):
        return self.trueskill_sigma

    def visualizarJogador(self):
        print(f"ID: {self.acc_id}\nWins: {self.total_wins}\nTS - MU: {self.trueskill_mu}\nTS - Sigma: {self.trueskill_sigma}")

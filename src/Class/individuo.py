import random


class Individuo():
    def __init__(self, jogadores, geracao=0):
        self.jogadores = jogadores
        self.nota_avaliacao = 0
        self.geracao = geracao

        # Geração do Array de Cromossomos
        self.cromossomos = [1] * 10 + [0] * (len(jogadores)-10)
        random.shuffle(self.cromossomos)

    def crossover(self, outro_individuo):
        """
        Realiza o Crossover entre o array cromossomo atual e outro inidivuo, retornando 2 filhos

        Retorna:
        list: Retorna a lista de 2 inidividuos filhos 
        """
        corte = round(random.random() * len(self.cromossomos))

        filho1 = outro_individuo.cromossomos[0:corte] + \
            self.cromossomos[corte::]

        filho2 = self.cromossomos[0:corte] + \
            outro_individuo.cromossomos[corte::]

        filhos = [Individuo(self.jogadores, self.geracao + 1),
                  Individuo(self.jogadores, self.geracao + 1)]

        filhos[0].cromossomos = filho1
        filhos[1].cromossomos = filho2

        return filhos

    def mutacao(self, taxa_mutacao):
        """
        Realiza a mutação do gene do vetor do cromossomo e garante que
        exatamente 10 elementos do cromossomo sejam 1.

        Args:
            taxa_mutacao (float): Taxa de probabilidade para ocorrer mutação.

        Retorna:
            obj: retorna o próprio objeto.
        """

        for i in range(len(self.cromossomos)):
            if random.random() < taxa_mutacao:
                if self.cromossomos[i] == 1:
                    self.cromossomos[i] = 0
                else:
                    self.cromossomos[i] = 1

        selecionados = [i for i, gene in enumerate(
            self.cromossomos) if gene == 1]
        nao_selecionados = [i for i, gene in enumerate(
            self.cromossomos) if gene == 0]

        while len(selecionados) > 10:

            elemento_aleatorio = random.choice(selecionados)
            self.cromossomos[elemento_aleatorio] = 0
            selecionados.remove(elemento_aleatorio)

        while len(selecionados) < 10:

            elemento_aleatorio = random.choice(nao_selecionados)
            self.cromossomos[elemento_aleatorio] = 1
            selecionados.append(elemento_aleatorio)

        return self

    def avaliacao(self):
        """
        Calcula o fitness com a skill dos players

        Retorna:
        int: Media entre 2 times
        """

        jogadores_selecionados = []

        for i in range(len(self.cromossomos)):
            if self.cromossomos[i] == 1:
                jogadores_selecionados.append(self.jogadores[i])
            if len(jogadores_selecionados) == 10:
                break

        media_mu, media_sigma = self.calcularMediaSkill(jogadores_selecionados)

        self.nota_avaliacao = round(media_mu - 0.5 * media_sigma, 2)

    def calcularMediaSkill(self, jogadores_selecionados):
        """
        Calcular Media TrueSkill entre 2 times

        Entrada:
          list - jogadores_selecionados

        Retorna:
        int: Media entre 2 times de TrueSkill MU
        int: Media entre 2 time de TrueSkill Sigma
        """

        media_mu = 0
        media_sigma = 0

        for jogador in jogadores_selecionados:
            media_mu += jogador.getTrueskillmu()
            media_sigma += jogador.getTrueskillsigma()

        return abs(media_mu/10), abs(media_sigma/10)

    def visualizarGenesSelecionados(self, players_list):
        """
        Printa os 10 players selecionados para a partida randomicamente

        Entrada:
          list - player_list: lista de Players
        """
        for i, gene in enumerate(self.cromossomos):

            if gene == 1:
                player_selecionado = players_list[i]
                player_selecionado.visualizarJogador()
                print("------X-----\n\n")

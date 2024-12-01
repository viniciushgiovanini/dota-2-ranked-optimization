import random
from Class.individuo import Individuo


class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao) -> None:
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0

    def inicializa_populacao(self, jogadores):
        '''
        Inicializa a populacao com uma lista de Individuos
        Seta a melhor solucao sendo a primeira solucao (Inicialmente)

        Param:
          list: lista de Players

        '''

        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(jogadores=jogadores))

        self.melhor_solucao = self.populacao[0]

    def ordena_populacao(self):
        '''
         Ordena a lista populacao que é uma lista de individuos pela maior nota
        '''

        self.populacao = sorted(
            self.populacao, key=lambda populacao: populacao.nota_avaliacao, reverse=True)

    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        return round(soma, 2)

    def seleciona_pai(self, soma_avaliacao):
        '''
        Método da roleta viciada para selecionar o elemento PAI

        Param:
          - soma_avaliacao(int): soma da avaliacao das notas da populacao

        Return:
          - int: indice do elemento selecionado na roleta viciada
        '''

        pai = -1
        valor_sorteado = random.random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai

    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print(f"Geração: {melhor.geracao}")
        print(
            f"Nota da Partida de Dota 2: {melhor.nota_avaliacao}")
        print(f"Cromossomos: {melhor.cromossomos}")

        print("\n-----X-----\n")

    def resolver(self, taxa_mutacao, numero_geracoes, lista_jogadores):

        self.inicializa_populacao(jogadores=lista_jogadores)

        for individuo in self.populacao:
            individuo.avaliacao()

        self.ordena_populacao()

        self.visualiza_geracao()

        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []

            for individuos_gerados in range(0, self.tamanho_populacao, 2):

                pai1 = self.seleciona_pai(soma_avaliacao=soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao=soma_avaliacao)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            self.populacao = list(nova_populacao)

            for individuo in self.populacao:
                individuo.avaliacao()

            self.ordena_populacao()

            self.visualiza_geracao()

            melhor = self.populacao[0]
            self.melhor_individuo(melhor)

        print("#########################################\n#             MELHOR SOLUCAO            #\n#########################################\n")
        print(
            f"Melhor Solucao --> \nGeracao: {self.melhor_solucao.geracao}\nNota da Partida: {self.melhor_solucao.nota_avaliacao}\n")
        self.melhor_solucao.visualizarGenesSelecionados(
            players_list=lista_jogadores)

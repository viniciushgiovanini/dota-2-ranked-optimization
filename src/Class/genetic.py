import random
import pickle
from Class.individuo import Individuo


class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao) -> None:
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_de_solucoes = []
        self.todas_solucoes_por_geracao = []

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

    def visualizar_lista_melhores_resultados(self):

        self.todas_solucoes_por_geracao.sort(
            key=lambda x: x.nota_avaliacao, reverse=True)

        low_matches = []
        mid_matches = []
        high_matches = []

        for solucao in self.todas_solucoes_por_geracao:

            if solucao.nota_avaliacao <= 24.5:
                low_matches.append(solucao)
            elif solucao.nota_avaliacao > 24.5 and solucao.nota_avaliacao <= 26:
                mid_matches.append(solucao)
            elif solucao.nota_avaliacao > 26:
                high_matches.append(solucao)

        print("###################\n#Partida Altas#\n###################\n")

        for each in high_matches:
            print(
                f"Partidas Altas --> Geracao: {each.geracao} Nota da Partida: {each.nota_avaliacao}\n")

        print("###################\n#Partida Medias#\n###################\n")

        for each in mid_matches:
            print(
                f"Partidas Medias --> Geracao: {each.geracao} Nota da Partida: {each.nota_avaliacao}\n")

        print("###################\n#Partida Baixas#\n###################\n")
        for each in low_matches:
            print(
                f"Partidas Baixas --> Geracao: {each.geracao} Nota da Partida: {each.nota_avaliacao}\n")

    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print(f"Geração: {melhor.geracao}")
        print(
            f"Nota da Partida de Dota 2: {melhor.nota_avaliacao}")
        # print(f"Cromossomos: {melhor.cromossomos}")

        print("\n-----X-----\n")

    def resolver(self, taxa_mutacao, numero_geracoes, lista_jogadores):

        self.inicializa_populacao(jogadores=lista_jogadores)

        for individuo in self.populacao:
            individuo.avaliacao()

        self.ordena_populacao()

        self.melhor_solucao = self.populacao[0]
        self.lista_de_solucoes.append(self.melhor_solucao.nota_avaliacao)

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

            self.todas_solucoes_por_geracao.append(melhor)

            self.lista_de_solucoes.append(melhor.nota_avaliacao)
            self.melhor_individuo(melhor)

        print("#########################################\n#             MELHOR SOLUCAO            #\n#########################################\n")
        print(
            f"Melhor Solucao --> \nGeracao: {self.melhor_solucao.geracao}\nNota da Partida: {self.melhor_solucao.nota_avaliacao}\n")
        self.melhor_solucao.visualizarGenesSelecionados(
            players_list=lista_jogadores)

        self.visualizar_lista_melhores_resultados()

""" Módulo para os algoritmos de ordenação """


from abc import ABC, abstractmethod
from typing import List


class Algorithm(ABC):
    """ Base de um algoritmo """

    def __init__(self):
        self.__array: List[int] = []

    @property
    def array(self):
        """ O estado atual do array """
        return self.__array

    @array.setter
    def array(self, array: List[int]):
        """ Define um novo array para realizar o sort """
        self.__array = array

    @abstractmethod
    def is_done(self):
        """ Se a ordenação já foi concluída """

    @abstractmethod
    def sort_new(self, array: List[int]):
        """ Define um novo array para realizar o sort """

    @abstractmethod
    def one_step(self):
        """ Ordernar apenas um passo """


class Quicksort(Algorithm):
    """ Implementação do algoritmo de quicksort utilizando um stack """

    def __init__(self):
        super().__init__()
        self.__stack: List[int] = []
        self.__high = -1
        self.__low = -1
        self.__top = -1

    def is_done(self):
        return self.__top <= 0

    def sort_new(self, array: List[int]):
        self.array = array
        self.__high = len(self.array) - 1
        self.__low = 0
        self.__stack = [0] * len(self.array)
        self.__top = 0
        self.__stack[self.__top] = self.__low
        self.__top += 1
        self.__stack[self.__top] = self.__high

    def __switch_elements(self, i: int, j: int):
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def __partition(self):
        high_value = self.array[self.__high]

        i = self.__low - 1
        for j in range(self.__low, self.__high):
            if self.array[j] <= high_value:
                i += 1
                self.__switch_elements(i, j)
        i += 1
        self.__switch_elements(i, self.__high)
        return i

    def __aux(self):
        self.__high = self.__stack[self.__top]
        self.__top -= 1
        self.__low = self.__stack[self.__top]
        self.__top -= 1

        # Realiza o particionamento, recebendo o pivot
        pivot = self.__partition()

        # Se houverem elementos à esquerda do pivot, adicionamos ao stack
        if pivot - 1 > self.__low:
            self.__top += 1
            self.__stack[self.__top] = self.__low
            self.__top += 1
            self.__stack[self.__top] = pivot - 1

        # Se houverem elementos à direita do pivot, adicionamos ao stack
        if pivot + 1 < self.__high:
            self.__top += 1
            self.__stack[self.__top] = pivot + 1
            self.__top += 1
            self.__stack[self.__top] = self.__high

    def one_step(self):
        if self.__top >= 0:
            self.__aux()


class BubbleSort(Algorithm):
    """
    Implementação do algoritmo de bubblesort:
    O algoritmo percorre o array diversas vezes,
    e a cada passagem fazer flutuar para o topo o
    maior elemento da sequencia.
    """

    def __init__(self):
        super().__init__()
        self.__is_done = False
        self.__total_higher = 0
        self.__next_position = 0
        self.__less = 1

    def is_done(self):
        return self.__is_done

    def sort_new(self, array: list):
        self.array = array
        self.__is_done = False
        self.__total_higher = 0
        self.__next_position = 0
        self.__less = 1

    def one_step(self):
        for i in range(self.__next_position, len(self.array) - 1):
            if self.array[i] > self.array[i + 1]:
                # Faz a troca de posicao.
                self.array[i], self.array[i +
                                          1] = self.array[i+1], self.array[i]
                # Reset da variavel auxiliar.
                self.__total_higher = 0
                # Posicao de partida do proximo looping e averiguacao de posicao.
                self.__next_position = i + 1

                # Caso o valor atinja sua posicao correta no array ordenado:
                if self.__next_position == len(self.array) - self.__less:
                    # A variavel auxiliar de partida sofre reset.
                    self.__next_position = 0
                    # E a posicao correta do proximo termo e uma
                    # anterior a do ultimo termo ordenado.
                    self.__less += 1
                break
            # Variavel auxiliar conta quantas vezes isso ocorre.
            self.__total_higher += 1

            # Caso seja igual ao comprimento da lista, o array esta ordenado:
            if self.__total_higher == len(self.array)-1:
                self.__is_done = True


class SelectionSort(Algorithm):
    """
    Implementação do algoritmo de Selectionsort:
    A ordenacao e feita de forma que o algoritmo
    procura o menor valor do array e o posiciona
    na primeira posicao, trocando-o de lugar com
    o valor que ocupava tal posicao, entao a
    busca pelo segundo menor comeca e ao fim
    posiciona o segundo menor valor na segunda
    posicao e assim por diante.
    """

    def __init__(self):
        super().__init__()
        self.__is_done = False
        self.__actual_less = -1
        self.__initial = 0
        self.__higher = 0
        self.__higher_true_position = 0

    def is_done(self):
        return self.__is_done

    def sort_new(self, array: list):
        self.array = array
        self.__is_done = False
        self.__actual_less = self.array[0]
        self.__initial = 0
        self.__higher = 0
        self.__higher_true_position = 0

    def one_step(self):
        """ ordenacao de apenas um passo """

        # Busca pelo menor valor partindo da posicao self.__initial:
        for i in range(self.__initial, len(self.array)):
            # Caso o menor valor encontrado no array ate o momento seja maior que algum proximo:
            if self.__actual_less > self.array[i]:
                # A variavel auxiliar armazena o maior valor.
                self.__higher = self.array[self.__initial]
                # A variavel auxiliar armazena a posicao real do maior valor.
                self.__higher_true_position = i
                # A variavel auxiliar armazena o menor valor.
                self.__actual_less = self.array[i]

        # E feita a troca de posicoes entre o menor e maior valores encontrados:
        self.array[self.__initial], self.array[self.__higher_true_position] = self.__actual_less, self.__higher

        # Como o menor valor ja esta em sua posicao, a proxima busca parte de uma casa adiante:
        self.__initial += 1

        # Caso self.__initial seja igual ao comprimento da lista, o array ja esta ordenado:
        if self.__initial == len(self.array):
            self.__is_done = True

        if self.__is_done is False:
            # A variavel auxiliar responsavel por armazenar o menor valor
            # encontrado ate o momento recebe o valor da
            # primeira posicao da proxima busca:
            self.__actual_less = self.array[self.__initial]

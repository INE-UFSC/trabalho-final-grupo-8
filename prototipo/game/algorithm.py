""" Módulo para os algoritmos de ordenação """


from abc import ABC, abstractmethod


class Algorithm(ABC):
    """ Base de um algoritmo """

    def __init__(self):
        self.__array: list[int] = []

    @property
    def array(self):
        """ O estado atual do array """
        return self.__array

    @array.setter
    def array(self, array: list):
        """ Define um novo array para realizar o sort """
        self.__array = array

    @abstractmethod
    def is_done(self):
        """ Se a ordenação já foi concluída """

    @abstractmethod
    def sort_new(self, array: list):
        """ Define um novo array para realizar o sort """

    @abstractmethod
    def one_step(self):
        """ Ordernar apenas um passo """


class Quicksort(Algorithm):
    """ Implementação do algoritmo de quicksort utilizando um stack """

    def __init__(self):
        super().__init__()
        self.__stack: list[int] = []
        self.__high = -1
        self.__low = -1
        self.__top = -1

    def is_done(self):
        return self.__top <= 0

    def sort_new(self, array: list):
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


class Bubblesort(Algorithm):
    """ Implementação do algoritmo de bubblesort """

    def __init__(self):
        super().__init__()
        self.__is_done = False
        self.__total_higher = 0
        self.__actual = 0
        self.__next_position = 0
        self.__less = 1

    def is_done(self):
        return self.__is_done

    def sort_new(self, array: list):
        self.__array = array
        self.__is_done = False
        self.__total_higher = 0
        self.__actual = 0
        self.__next_position = 0
        self.__less = 1

    def one_step(self):
        ''' ordenacao de apenas um passo '''

        for i in range(self.__next_position, len(self.__array) - 1):
            if self.__array[i] > self.__array[i + 1]:
                self.__array[i], self.__array[i+1] = self.__array[i+1], self.__array[i]     # Faz a troca de posicao.
                self.__total_higher = 0                 # Reset da variavel auxiliar.
                self.__next_position = i + 1            # posicao de partida do proximo looping.

                # Caso o valor atinja sua posicao correta no array ordenado:
                if self.__next_position == len(self.__array) - self.__less:
                    self.__next_position = 0    # A variavel auxiliar de partida sofre reset.
                    self.__less += 1   # E a posicao correta do proximo termo e uma anterior a do ultimo termo ordenado.
                break

            else:                           # Caso o proximo valor nao seja menor que o atual.
                self.__total_higher += 1    # Variavel auxiliar conta quantas vezes isso ocorre.

                # Caso seja igual ao comprimento da lista, o array esta ordenado:
                if self.__total_higher == len(self.__array)-1:
                    self.__is_done = True


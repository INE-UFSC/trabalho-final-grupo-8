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

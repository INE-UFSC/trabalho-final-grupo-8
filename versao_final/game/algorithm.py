""" Módulo para os algoritmos de ordenação """


from abc import ABC, abstractmethod
from typing import Generator, Iterator, List
from game.array import Array
from game.command import Command, SwapCommand
from game.utils import is_sorted


class Algorithm(ABC):
    """ Base de um algoritmo """

    @abstractmethod
    def one_step(self) -> Iterator[Command]:
        """ Ordenar apenas um passo, por meio de um iterador """

    @abstractmethod
    def is_done(self) -> bool:
        """ Se o algoritmo já terminou a ordenação """


class BubbleSort(Algorithm):
    """
    Implementação do algoritmo de bubblesort:

    O algoritmo percorre o array diversas vezes,
    e a cada passagem fazer flutuar para o topo
    o maior elemento da sequência.
    """

    def __init__(self, array: Array):
        self.__array = array
        self.__done = False

    def is_done(self) -> bool:
        return self.__done

    def one_step(self) -> Iterator[Command]:
        array = self.__array.numbers
        less = 1

        while not self.__done:
            for i in range(len(array) - less):
                if array[i] > array[i + 1]:
                    yield SwapCommand(self.__array, i, i + 1)
            self.__done = is_sorted(array)
            less += 1


class RecursiveQuicksort(Algorithm):
    """ Implementação recursiva do algoritmo de quicksort """

    def __init__(self, array: Array):
        self.__array = array
        self.__done = False

    def is_done(self) -> bool:
        return self.__done

    def __partition(self, array: List[int], start: int, end: int) -> Generator[Command, None, int]:
        pivot_index = start
        pivot = array[pivot_index]

        while start < end:
            while start < len(array) and array[start] <= pivot:
                start += 1
            while array[end] > pivot:
                end -= 1
            if start < end:
                yield SwapCommand(self.__array, start, end)
        yield SwapCommand(self.__array, end, pivot_index)
        return end

    def __sort(self, array: List[int], low: int, high: int) -> Iterator[Command]:
        if low < high:
            pivot = yield from self.__partition(array, low, high)
            yield from self.__sort(array, low, pivot - 1)
            yield from self.__sort(array, pivot + 1, high)

    def one_step(self) -> Iterator[Command]:
        array = self.__array.numbers
        yield from self.__sort(array, 0, len(array) - 1)
        self.__done = True


class IterativeQuicksort(Algorithm):
    """ Implementação iterativa do quicksort, usando um stack """

    def __init__(self, array: Array):
        self.__array = array
        self.__done = False

    def is_done(self) -> bool:
        return self.__done

    def one_step(self) -> Iterator[Command]:
        array = self.__array.numbers

        stack: List[int] = []
        stack.append(0)
        stack.append(len(array) - 1)

        while stack:
            high = stack.pop()
            low = stack.pop()

            pivot = low - 1
            high_value = array[high]
            for j in range(low, high):
                if array[j] <= high_value:
                    pivot += 1
                    if pivot != j:
                        yield SwapCommand(self.__array, pivot, j)
            pivot += 1
            if pivot != high:
                yield SwapCommand(self.__array, pivot, high)

            if pivot - 1 > low:
                stack.append(low)
                stack.append(pivot - 1)

            if pivot + 1 < high:
                stack.append(pivot + 1)
                stack.append(high)
        self.__done = True


# class SelectionSort(Algorithm):
#     """
#     Implementação do algoritmo de Selectionsort:
#     A ordenacao e feita de forma que o algoritmo
#     procura o menor valor do array e o posiciona
#     na primeira posicao, trocando-o de lugar com
#     o valor que ocupava tal posicao, entao a
#     busca pelo segundo menor comeca e ao fim
#     posiciona o segundo menor valor na segunda
#     posicao e assim por diante.
#     """

#     def __init__(self):
#         super().__init__()
#         self.__is_done = False
#         self.__actual_less = -1
#         self.__initial = 0
#         self.__higher = 0
#         self.__higher_true_position = 0

#     def is_done(self):
#         return self.__is_done

#     def sort_new(self, array: list):
#         self.array = array
#         self.__is_done = False
#         self.__actual_less = self.array[0]
#         self.__initial = 0
#         self.__higher = 0
#         self.__higher_true_position = 0

#     def one_step(self):
#         """ ordenacao de apenas um passo """

#         # Busca pelo menor valor partindo da posicao self.__initial:
#         for i in range(self.__initial, len(self.array)):
#             # Caso o menor valor encontrado no array ate o momento seja maior que algum proximo:
#             if self.__actual_less > self.array[i]:
#                 # A variavel auxiliar armazena o maior valor.
#                 self.__higher = self.array[self.__initial]
#                 # A variavel auxiliar armazena a posicao real do maior valor.
#                 self.__higher_true_position = i
#                 # A variavel auxiliar armazena o menor valor.
#                 self.__actual_less = self.array[i]

#         # E feita a troca de posicoes entre o menor e maior valores encontrados:
#         self.array[self.__initial], self.array[self.__higher_true_position] = self.__actual_less, self.__higher

#         # Como o menor valor ja esta em sua posicao, a proxima busca parte de uma casa adiante:
#         self.__initial += 1

#         # Caso self.__initial seja igual ao comprimento da lista, o array ja esta ordenado:
#         if self.__initial == len(self.array):
#             self.__is_done = True

#         if self.__is_done is False:
#             # A variavel auxiliar responsavel por armazenar o menor valor
#             # encontrado ate o momento recebe o valor da
#             # primeira posicao da proxima busca:
#             self.__actual_less = self.array[self.__initial]

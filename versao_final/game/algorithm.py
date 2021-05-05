""" Módulo para os algoritmos de ordenação """


from abc import ABC, abstractmethod
from typing import Callable, Generator, Iterator, List, Tuple
from game.array import Array
from game.command import Command, SetCommand, SwapCommand
from game.utils import is_sorted


class Algorithm(ABC):
    """ Base de um algoritmo """

    @abstractmethod
    def one_step(self) -> Iterator[Command]:
        """ Ordenar apenas um passo, por meio de um iterador """

    @abstractmethod
    def is_done(self) -> bool:
        """ Se o algoritmo já terminou a ordenação """

    @abstractmethod
    def description(self) -> str:
        """ Retorna a descrição do algoritmo de ordenação"""


class BubbleSort(Algorithm):
    """ Implementação do algoritmo de bubblesort: """

    def __init__(self, array: Array):
        self.__array = array
        self.__done = False

    def is_done(self) -> bool:
        return self.__done

    def description(self) -> str:
        return ("O algoritmo percorre o array diversas vezes, "
                "e a cada passagem fazer flutuar para o topo o "
                "maior elemento da sequência.")

    def one_step(self) -> Iterator[Command]:
        array = self.__array.numbers
        less = 1

        while not self.__done:
            for i in range(len(array) - less):
                if array[i] > array[i + 1]:
                    yield SwapCommand(self.__array, i, i + 1)
            self.__done = is_sorted(array)
            less += 1


# Partitioner é uma função que:
#   - Recebe uma lista e dois inteiro
#   - Retorna um generator
Partitioner = Callable[
    [List[int], int, int],
    Generator[Tuple[int, int], None, int]
]


class RecursiveQuicksort(Algorithm):
    """ Implementação recursiva do algoritmo de quicksort """

    def __init__(self, partitioner: Partitioner, array: Array):
        self.__partitioner = partitioner
        self.__array = array
        self.__done = False

    def is_done(self) -> bool:
        return self.__done

    def description(self) -> str:
        return ("bla")

    def __sort(self, array: List[int], low: int, high: int) -> Iterator[Command]:
        if low < high:
            try:
                partitions = self.__partitioner(array, low, high)
                while True:
                    i, j = next(partitions)
                    yield SwapCommand(self.__array, i, j)
            except StopIteration as generator_done:
                pivot = generator_done.value
            yield from self.__sort(array, low, pivot - 1)
            yield from self.__sort(array, pivot + 1, high)

    def one_step(self) -> Iterator[Command]:
        array = self.__array.numbers
        yield from self.__sort(array, 0, len(array) - 1)
        self.__done = True


class IterativeQuicksort(Algorithm):
    """ Implementação iterativa do quicksort, usando um stack """

    def __init__(self, partitioner: Partitioner, array: Array):
        self.__partitioner = partitioner
        self.__array = array
        self.__done = False

    def is_done(self) -> bool:
        return self.__done

    def description(self) -> str:
        return ("bla")

    def one_step(self) -> Iterator[Command]:
        array = self.__array.numbers

        stack: List[int] = []
        stack.append(0)
        stack.append(len(array) - 1)

        while stack:
            high = stack.pop()
            low = stack.pop()

            try:
                partitions = self.__partitioner(array, low, high)
                while True:
                    i, j = next(partitions)
                    yield SwapCommand(self.__array, i, j)
            except StopIteration as generator_done:
                pivot = generator_done.value

            if pivot - 1 > low:
                stack.append(low)
                stack.append(pivot - 1)

            if pivot + 1 < high:
                stack.append(pivot + 1)
                stack.append(high)
        self.__done = True


class InsertionSort(Algorithm):
    """ Implementação do algoritmo de InsertionSort """

    def __init__(
        self,
        array: Array
    ):
        self.__array = array
        self.__done = False

    def is_done(self) -> bool:
        return self.__done

    def description(self) -> str:
        return ("bla")

    def one_step(self) -> Iterator[Command]:
        """
        Verificará se os elementos anteriores são
        maiores ou menores que o atual para ordenar
        """
        array = self.__array.numbers
        for i in range(1, len(array)):
            key = array[i]
            j = i - 1
            while j >= 0 and key < array[j]:
                SetCommand(self.__array, j + 1, array[j]).execute()
                j -= 1
            yield SetCommand(self.__array, j + 1, key)
        self.__done = True


class SelectionSort(Algorithm):
    """Implementação do algoritmo de Selectionsort:"""

    def __init__(self, array: Array):
        self.__array = array
        self.__done = False

    def is_done(self):
        return self.__done

    def description(self) -> str:
        return ("A ordenação é feita de forma que o algoritmo procura"
                " o menor valor do array e o posiciona na primeira posição, "
                "trocando-o de lugar com o valor que ocupava tal posicao,"
                "o processo termina quando todos os valores estiverem ordenados.")

    def one_step(self):
        array = self.__array.numbers
        for i in range(len(array)):
            minimum_index = i
            for j in range(i + 1, len(array)):
                if array[minimum_index] > array[j]:
                    minimum_index = j
            yield SwapCommand(self.__array, minimum_index, i)
        self.__done = True


def lomuto_partitioner(
    array: List[int],
    low: int,
    high: int
) -> Generator[Tuple[int, int], None, int]:
    """ Método de partição de Nico Lomuto, com apenas um for loop """
    pivot = low - 1
    high_value = array[high]
    for j in range(low, high):
        if array[j] <= high_value:
            pivot += 1
            if pivot != j:
                yield (pivot, j)
    pivot += 1
    if pivot != high:
        yield (pivot, high)
    return pivot


def hoare_partitioner(
    array: List[int],
    low: int,
    high: int
) -> Generator[Tuple[int, int], None, int]:
    """ Método de partição de Tony Hoare, com while loops """
    pivot_index = low
    pivot = array[pivot_index]
    while low < high:
        while low < len(array) and array[low] <= pivot:
            low += 1
        while array[high] > pivot:
            high -= 1
        if low < high:
            yield (low, high)
    yield (high, pivot_index)
    return high

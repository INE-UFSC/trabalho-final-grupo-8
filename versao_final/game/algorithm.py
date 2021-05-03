""" Módulo para os algoritmos de ordenação """


from abc import ABC, abstractmethod
from typing import Generator, Iterator, List
from game.array import Array
from game.command import Command, SetCommand, SwapCommand, SwapCommandFactory
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

    def __init__(self, swap_factory: SwapCommandFactory, array: Array):
        self.__swap_factory = swap_factory
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
                    yield self.__swap_factory.create(i, i + 1)
            self.__done = is_sorted(array)
            less += 1


class PartitionScheme(ABC):
    """ Método de partição para o algoritmo de quicksort """

    @abstractmethod
    def partition(self, array: List[int], low: int, high: int) -> Generator[Command, None, int]:
        """
        Realiza a partição, utilizando yield nas trocas
        de posição e retornando o valor do pivor quando
        finalizado
        """


class LomutoPartitionScheme(PartitionScheme):
    """ Método de partição de Nico Lomuto """

    def __init__(self, swap_factory: SwapCommandFactory):
        self.__swap_factory = swap_factory

    def partition(self, array: List[int], low: int, high: int) -> Generator[Command, None, int]:
        """ Utiliza apenas um for loop ao realizar o particionamento """
        pivot = low - 1
        high_value = array[high]
        for j in range(low, high):
            if array[j] <= high_value:
                pivot += 1
                if pivot != j:
                    yield self.__swap_factory.create(pivot, j)
        pivot += 1
        if pivot != high:
            yield self.__swap_factory.create(pivot, high)
        return pivot


class HoarePartitionScheme(PartitionScheme):
    """ Método de partição de Tony Hoare """

    def __init__(self, swap_factory: SwapCommandFactory):
        self.__swap_factory = swap_factory

    def partition(self, array: List[int], low: int, high: int) -> Generator[Command, None, int]:
        """ Utiliza while loops durante o particionamento """
        pivot_index = low
        pivot = array[pivot_index]

        while low < high:
            while low < len(array) and array[low] <= pivot:
                low += 1
            while array[high] > pivot:
                high -= 1
            if low < high:
                yield self.__swap_factory.create(low, high)
        yield self.__swap_factory.create(high, pivot_index)
        return high


class RecursiveQuicksort(Algorithm):
    """ Implementação recursiva do algoritmo de quicksort """

    def __init__(self, partitioner: PartitionScheme, array: Array):
        self.__partitioner = partitioner
        self.__array = array
        self.__done = False

    def is_done(self) -> bool:
        return self.__done

    def __sort(self, array: List[int], low: int, high: int) -> Iterator[Command]:
        if low < high:
            pivot = yield from self.__partitioner.partition(array, low, high)
            yield from self.__sort(array, low, pivot - 1)
            yield from self.__sort(array, pivot + 1, high)

    def one_step(self) -> Iterator[Command]:
        array = self.__array.numbers
        yield from self.__sort(array, 0, len(array) - 1)
        self.__done = True


class IterativeQuicksort(Algorithm):
    """ Implementação iterativa do quicksort, usando um stack """

    def __init__(self, partitioner: PartitionScheme, array: Array):
        self.__partitioner = partitioner
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

            pivot = yield from self.__partitioner.partition(array, low, high)

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

    def __init__(self, array: Array):
        self.__array = array
        self.__done = False

    def is_done(self):
        return self.__done

    def one_step(self):
        array = self.__array.numbers
        for i in range(len(array)):
            minimum_index = i
            for j in range(i + 1, len(array)):
                if array[minimum_index] > array[j]:
                    minimum_index = j
            yield SwapCommand(self.__array, minimum_index, i)
        self.__done = True

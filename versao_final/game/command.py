""" Módulo para as operações realizadas nos array """


from abc import ABC, abstractmethod
from game.array import Array


class Command(ABC):
    """ Uma operação a ser executada """

    @abstractmethod
    def execute(self) -> None:
        """ Executa a operação """


class SwapCommand(Command):
    """ Troca duas posições do array """

    def __init__(self, array: Array, origin: int, destination: int):
        self.__array = array
        self.__origin = origin
        self.__destination = destination

    def execute(self):
        for array in [self.__array.numbers, self.__array.boxes]:
            (array[self.__origin],
             array[self.__destination]) = (array[self.__destination],
                                           array[self.__origin])

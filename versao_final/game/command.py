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


class CommandFactory(ABC):
    """ Classe criadora de comandos """

    @abstractmethod
    def create(self, origin: int, destination: int) -> Command:
        """
        Cria um novo comando

        Por enquanto todos deverão receber a posição
        inicial e a posição final, no entanto caso
        seja necessário isso poderá ser alterado.
        """


class SwapCommandFactory(CommandFactory):
    """ Classe criadora de comandos de troca de posições """

    def __init__(self, array: Array):
        self.__array = array

    def create(self, origin: int, destination: int):
        return SwapCommand(self.__array, origin, destination)

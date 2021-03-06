""" Módulo para as operações realizadas nos array """


from abc import ABC, abstractmethod

from game.array.array import Array


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

    def __change_colors(self) -> None:
        for box in self.__array.boxes:
            box.draw()
        self.__array.boxes[self.__origin].draw((255, 255, 0))
        self.__array.boxes[self.__destination].draw((255, 255, 0))

    def execute(self) -> None:
        self.__change_colors()
        for array in [self.__array.numbers, self.__array.boxes]:
            (array[self.__origin],
             array[self.__destination]) = (array[self.__destination],
                                           array[self.__origin])


class RemoveCommand(Command):
    """ Remove uma posição do array """

    def __init__(self, array: Array, index: int):
        self.__array = array
        self.__index = index

    def execute(self):
        for array in [self.__array.numbers, self.__array.boxes]:
            array.pop(self.__index)


class SetCommand(Command):
    """ Define uma posição no array """

    def __init__(self, array: Array, index: int, value: int):
        self.__array = array
        self.__index = index
        self.__value = value

    def __change_colors(self) -> None:
        self.__array.boxes[self.__index].draw((0, 255, 0))

    def execute(self):
        self.__array.numbers[self.__index] = self.__value
        self.__array.boxes[self.__index] = self.__array.box_factory.create(
            self.__value
        )
        self.__change_colors()

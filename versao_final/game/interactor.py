""" Classes que interagem com o array """


from abc import ABC, abstractmethod
from game.array import Array


class Interactor(ABC):
    """ Interage com um array ao ser atualizado """

    @abstractmethod
    def set_array(self, array: Array) -> None:
        """ Associa um novo array ao interactor """

    @abstractmethod
    def update(self) -> None:
        """ Modifica o array """

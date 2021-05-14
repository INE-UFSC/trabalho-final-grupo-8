""" Módulo para as entidades que jogarão o jogo """


from typing import Optional

from game.array.array import Array
from game.entity.data import Data
from game.entity.interactor import Interactor
from game.exceptions import AttributesNotSetException


class Entity:
    """ Uma entidade que possui interação com o array, dados e um array """

    def __init__(self, array: Array, interactor: Interactor, data: Data):
        self.__array = array
        self.__interactor = interactor
        self.__data = data
        self.__interactor.set_array(array)

    @property
    def array(self) -> Array:
        """ O array dessa entidade """
        return self.__array

    @property
    def interactor(self) -> Interactor:
        """ O modo de interação dessa entidade """
        return self.__interactor

    @property
    def data(self) -> Data:
        """ Os dados dessa entidade """
        return self.__data


class EntityBuilder:
    """ Responsável pela criação de entidades do jogo """

    def __init__(self):
        self.__array: Optional[Array] = None
        self.__data: Optional[Data] = None
        self.__interactor: Optional[Interactor] = None
        self.__result: Optional[Entity] = None

    def reset(self) -> None:
        """ Remove a entidade do builder """
        self.__result = None

    def set_array(self, array: Array) -> None:
        """ Define o array da entidade """
        if not isinstance(array, Array):
            raise TypeError
        self.__array = array

    def set_data(self, data: Data) -> None:
        """ Define os dados da entidades """
        if not isinstance(data, Data):
            raise TypeError
        self.__data = data

    def set_interactor(self, interactor: Interactor) -> None:
        """ Define o modo de interação da entidade """
        if not isinstance(interactor, Interactor):
            raise TypeError
        self.__interactor = interactor

    def get_result(self) -> Entity:
        """ Retorna a entidade criada """
        if self.__result is None:
            if (
                self.__array is not None and
                self.__interactor is not None and
                self.__data is not None
            ):
                self.__result = Entity(
                    self.__array,
                    self.__interactor,
                    self.__data,
                )
            else:
                raise AttributesNotSetException
        return self.__result

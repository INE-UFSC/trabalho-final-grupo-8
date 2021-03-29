""" Módulo para os algoritmos de ordenação """


from abc import ABC, abstractmethod


class Algorithm(ABC):
    """ Base de um algoritmo """

    def __init__(self, array: list):
        self.__original_array = array
        self.__current_array = array
        self.__done = False

    @property
    def original_array(self):
        """ O estado original do array """
        return self.__original_array

    @property
    def current_array(self):
        """ O estado atual do array """
        return self.__current_array

    @property
    def done(self):
        """ Se a ordenação já foi concluída """
        return self.__done

    @abstractmethod
    def one_step(self):
        """ Ordernar apenas um passo """

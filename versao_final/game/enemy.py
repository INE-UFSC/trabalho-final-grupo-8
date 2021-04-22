""" Módulo para gerar o inimigo """


from typing import List
from game.algorithm import Algorithm
from game.numbers import NumberArray


class Enemy:
    """ Classe responsável pela ordenação do array conforme um período de tempo especificado """

    def __init__(
        self,
        algorithm: Algorithm,
        number_array: NumberArray,
        step_time: float
    ):
        self.__time = -1.0
        self.__step_time = step_time
        self.__algorithm = algorithm
        self.__number_array = number_array

    def __update_timer(self, increment: float):
        """ Atualiza o timer, iniciando caso não tenha iniciado """
        if self.__time == -1:
            self.__time = 0
        else:
            self.__time += increment

    def __should_sort(self):
        """ Se o timer já está superior ao período que o inimigo deve esperar """
        return self.__time >= self.__step_time

    def set_array(self, array: List[int]):
        """ Define um novo array para realizar a ordenação """
        self.__algorithm.sort_new(array)
        self.__number_array.array = array

    def update(self, delta_time: float):
        """ Atualiza o timer e checa se o array deve ser organizado """
        if self.__algorithm.is_done():
            return
        self.__update_timer(delta_time)
        if self.__should_sort():
            self.__time = 0
            self.__algorithm.one_step()
            self.__number_array.array = self.__algorithm.array.copy()

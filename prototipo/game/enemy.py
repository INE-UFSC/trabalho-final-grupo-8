""" Módulo para gerar o inimigo """


from game.algorithm import Algorithm
from game.number_array import NumberArray


def get_array_differences(original: list, new: list):
    """
    Retorna os índices das diferenças entre duas listas.

    Não utlizado na implementação atual.
    """
    differences: list[tuple[int, int]] = []
    for index, _ in enumerate(original):
        if original[index] != new[index]:
            search_start = 0
            new_index = -1
            while True:
                new_index = new.index(original[index], search_start)
                if original[new_index] != new[new_index]:
                    break
                search_start = new_index + 1
            if (new_index, index) not in differences:
                differences.append((index, new_index))
    return differences


class Enemy:
    """ Classe responsável pela ordenação do array conforme um período de tempo especificado """

    def __init__(self, algorithm: Algorithm, number_array: NumberArray, step_time: float):
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

    def set_array(self, array: list):
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

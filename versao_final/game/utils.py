""" Módulo com funcionalidade utilitárias """


import sys
import pygame as pg


def end():
    """ Finaliza o pygame e encerra o processo """
    pg.quit()
    sys.exit()


class Timer:
    """ Um timer que é atualizado todos os frames """

    def __init__(
        self,
        time: float,
        auto_start: bool = True,
        one_shot: bool = False
    ):
        self.__time = time
        self.__time_left = time
        self.__paused = not auto_start
        self.__one_shot = one_shot
        self.__timeout = False

    @property
    def paused(self):
        """ O estado atual do timer """
        return self.__paused

    @property
    def time_left(self):
        """ Quanto tempo falta para o timer finalizar """
        return self.__time_left

    @property
    def timeout(self):
        """ Se o clock já finalizou a contagem """
        return self.__timeout

    def start(self):
        """ Reinicia o timer """
        self.__time_left = self.__time
        self.__paused = False

    def update(self, delta_time: float):
        """ Atualiza o timer conforme o delta time """
        if not self.__paused:
            self.__timeout = False
            self.__time_left -= delta_time
            if self.__time_left <= 0:
                self.__timeout = True
                if self.__one_shot:
                    self.__paused = True
                else:
                    self.start()

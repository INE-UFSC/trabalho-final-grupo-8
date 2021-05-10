""" Módulo com funcionalidade utilitárias """


import sys
from typing import Dict, List
import pygame as pg


def end():
    """ Finaliza o pygame e encerra o processo """
    pg.quit()
    sys.exit()


def is_sorted(array: List[float]):
    """ Percorre o array checando se o mesmo está organizado """
    if len(array) in [0 or 1]:
        return True
    for i in range(1, len(array)):
        if array[i - 1] > array[i]:
            return False
    return True


class Singleton(type):
    """ Metaclasse referente a um singleton """

    __instances: Dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(
                Singleton, cls
            ).__call__(*args, **kwargs)
        return cls.__instances[cls]


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
        TimerList().add_timer(self)

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


class TimerList(metaclass=Singleton):
    """ Responsável por atualizar todos os timers """

    def __init__(self):
        self.__timers: List[Timer] = []

    def add_timer(self, timer: Timer) -> None:
        if not isinstance(timer, Timer):
            raise TypeError
        self.__timers.append(timer)

    def update(self, delta_time: float) -> None:
        """ Atualiza todos os timers """
        for timer in self.__timers:
            timer.update(delta_time)

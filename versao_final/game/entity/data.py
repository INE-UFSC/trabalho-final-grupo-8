""" Módulo para os dados de uma entidade """


import pygame as pg

from game.constants import SCORE_CHANGED


class Data:
    """ Representa os dados de um jogador """

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError
        if len(name) == 0:
            raise ValueError
        self.__name = name
        self.__score = 0

    @property
    def name(self) -> str:
        """ O nome """
        return self.__name

    @property
    def score(self) -> int:
        """ A pontuação """
        return self.__score

    @score.setter
    def score(self, score: int) -> None:
        """ Define uma nova pontuação """
        self.__score = score
        event = pg.event.Event(
            SCORE_CHANGED,
            value=self.__score,
            name=self.__name
        )
        pg.event.post(event)

""" Módulo relacionado à partida """


import pygame as pg
from game.array import Array
from game.interactor import Interactor


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


class GameEntity:
    """ Uma entidade que possui interação com o array, dados e um array """

    def __init__(self, array: Array, interactor: Interactor, data: Data):
        self.__array = array
        self.__interactor = interactor
        self.__data = data

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


class Match:
    """ Uma partida do jogo """

    def __init__(
        self,
        player: GameEntity,
        enemy: GameEntity
    ):
        self.__player = player
        self.__enemy = enemy

    def update(self):
        """ Atualiza a partida """
        self.__player.interactor.update()
        self.__enemy.interactor.update()

    def draw(self, surface: pg.Surface):
        """ Desenha os arrays """
        self.__player.array.draw(surface)
        self.__enemy.array.draw(surface)

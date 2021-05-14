""" Módulo para o gerenciamento do estado do jogo """


from typing import Optional

import pygame as pg

from game.game.match import Match, MatchFactory


class GameState():
    """ Representa o estado do jogo """

    def __init__(self, match_factory: MatchFactory):
        self.__match_factory = match_factory
        self.__match: Optional[Match] = None

    @property
    def match(self) -> Optional[Match]:
        """ A partida atual do jogo """
        return self.__match

    @match.setter
    def match(self, match: Match) -> None:
        """ Define uma nova partida """
        if not isinstance(match, Match):
            raise TypeError
        self.__match = match

    @property
    def match_factory(self) -> MatchFactory:
        """ Retorna a fábrica de partidas """
        return self.__match_factory

    def draw(self, surface: pg.Surface):
        """ Desenha o jogo """
        if self.__match is not None:
            self.__match.update()
            self.__match.draw(surface)

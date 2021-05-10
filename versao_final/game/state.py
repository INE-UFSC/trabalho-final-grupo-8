""" Módulo para o gerenciamento do estado do jogo """


from typing import Optional
from game.utils import Singleton
from game.match import Match


class GameState(metaclass=Singleton):
    """ Representa o estado do jogo """

    def __init__(self):
        self.__match: Optional[Match] = None

    @property
    def match(self) -> Optional[Match]:
        """ A partida atual do jogo """
        return self.__match

    @match.setter
    def match(self, match: Match) -> None:
        """ Define uma nova partida """
        self.__match = match

""" Módulo relacionado à partida """


from typing import List, Optional
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

        event_id = pg.event.custom_type()
        print(event_id)
        pg.event.Event(
            event_id,
            value=self.__score,
            name=self.__name
        )


class GameEntity:
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


class Match:
    """ Uma partida do jogo """

    def __init__(
        self,
        player: GameEntity,
        enemy: GameEntity,
        array: List[int]
    ):
        self.__player = player
        self.__enemy = enemy
        self.__set_array(array)

    @property
    def player(self) -> GameEntity:
        """ O jogador """
        return self.__player

    @property
    def enemy(self) -> GameEntity:
        """ O adversário """
        return self.__enemy

    def __set_array(self, array: List[int]) -> None:
        self.__player.array.numbers = array
        self.__enemy.array.numbers = array

    def update(self):
        """ Atualiza a partida """
        self.__player.interactor.update()
        self.__enemy.interactor.update()

    def draw(self, surface: pg.Surface):
        """ Desenha os arrays """
        self.__player.array.draw(surface)
        self.__enemy.array.draw(surface)


class AttributesNotSetException(Exception):
    """ Lançada em builder quando os atributos não foram totalemente definidos """

    def __init__(self):
        super().__init__("Atributos não definidos no Builder")


class GameEntityBuilder:
    """ Responsável pela criação de entidades do jogo """

    def __init__(self):
        self.__array: Optional[Array] = None
        self.__data: Optional[Data] = None
        self.__interactor: Optional[Interactor] = None
        self.__result: Optional[GameEntity] = None

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

    def get_result(self) -> GameEntity:
        """ Retorna a entidade criada """
        if self.__result is None:
            if (
                self.__array is not None and
                self.__interactor is not None and
                self.__data is not None
            ):
                self.__result = GameEntity(
                    self.__array,
                    self.__interactor,
                    self.__data,
                )
            else:
                raise AttributesNotSetException
        return self.__result


class MatchFactory:
    """
    Responsável pela criação de partidas levando em conta os
    criadores de entidades para o jogador e o adversário
    """

    def __init__(self):
        self.__player = GameEntityBuilder()
        self.__enemy = GameEntityBuilder()

    @property
    def player(self) -> GameEntityBuilder:
        """ O criador do jogador """
        return self.__player

    @property
    def enemy(self) -> GameEntityBuilder:
        """ O criador do adversário """
        return self.__enemy

    def create(self, array: List[int]):
        """ Cria a partida """
        return Match(
            self.__player.get_result(),
            self.__enemy.get_result(),
            array
        )

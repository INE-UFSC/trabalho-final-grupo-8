""" Módulo para as classes referentes ao estado do jogo """


import pygame as pg
from game.array import Array
from game.enemy import Enemy
from game.player import Player
from game.sound import SoundManager
from game.engine import DisplayManager, InputManager


class Data:
    """ Representa os dados de um jogador """

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError
        if len(name) == 0:
            raise ValueError
        self.__name = name
        self.__score = 0
        self.__subscribers: list = []

    @property
    def name(self) -> str:
        """ O nome do jogador """
        return self.__name

    @property
    def score(self) -> int:
        """ A pontuação do jogador """
        return self.__score

    @score.setter
    def score(self, score: int) -> None:
        """ Define uma nova pontuação ao jogador """
        self.__score = score

    def subscribe(self, observer):
        """ Adiciona um subscriber a estes dados """
        self.__subscribers.append(observer)


class GameState:
    """ O estado da partida """

    def __init__(self, player_data: Data, enemy_data: Data):
        if not isinstance(player_data, Data) or not isinstance(enemy_data, Data):
            raise TypeError
        self.__enemy_data: Data = enemy_data
        self.__player_data: Data = player_data

    @property
    def player_data(self) -> Data:
        """ Os dados do jogador """
        return self.__player_data

    @property
    def enemy_data(self) -> Data:
        """ Os dados do inimigo """
        return self.__enemy_data

    def update(self) -> None:
        """ Atualiza o estado do jogo """
        self.__enemy_data.score = 10
        self.__player_data.score = 200


class Game:
    """ A classe responsável pelo gerenciamento do jogo """

    def __init__(
        self,
        display: DisplayManager,
        inputs: InputManager,
        sound: SoundManager
    ):
        self.__display = display
        self.__inputs = inputs
        self.__sound = sound


class Match:
    """ Responsável pelo gerenciamento de uma partida """

    def __init__(
        self,
        player: Player,
        player_array: Array,
        enemy: Enemy,
        enemy_array: Array
    ):
        self.__entities = [player, enemy]
        self.__arrays = [player_array, enemy_array]

    def update(self):
        """ Atualiza a partida """
        for entity in self.__entities:
            entity.update()

    def draw(self, surface: pg.Surface):
        """ Desenha a partida """
        for array in self.__arrays:
            array.draw(surface)

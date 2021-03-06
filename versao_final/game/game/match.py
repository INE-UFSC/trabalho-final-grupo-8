""" Módulo relacionado à partida """


from typing import Optional

import pygame as pg

from game.entity.entity import Entity, EntityBuilder
from game.exceptions import AttributesNotSetException
from game.game.mode import GameMode


class Match:
    """ Uma partida do jogo """

    def __init__(
        self,
        game_mode: GameMode,
        player: Entity,
        enemy: Entity
    ):
        self.__game_mode = game_mode
        self.__player = player
        self.__enemy = enemy
        self.__game_mode.set_entities(player, enemy)

    @property
    def game_mode(self) -> GameMode:
        """ O modo de jogo """
        return self.__game_mode

    @property
    def player(self) -> Entity:
        """ O jogador """
        return self.__player

    @property
    def enemy(self) -> Entity:
        """ O adversário """
        return self.__enemy

    def update(self):
        """ Atualiza a partida """
        self.__game_mode.update()

    def draw(self, surface: pg.Surface):
        """ Desenha os arrays """
        self.__player.array.draw(surface)
        self.__enemy.array.draw(surface)


class MatchFactory:
    """
    Responsável pela criação de partidas levando em conta os
    criadores de entidades para o jogador e o adversário
    """

    def __init__(self):
        self.__player = EntityBuilder()
        self.__enemy = EntityBuilder()
        self.__game_mode: Optional[GameMode] = None

    def set_game_mode(self, game_mode: GameMode) -> None:
        """ Define o modo de jogo a ser criado """
        if not isinstance(game_mode, GameMode):
            raise TypeError
        self.__game_mode = game_mode

    @property
    def player(self) -> EntityBuilder:
        """ O criador do jogador """
        return self.__player

    @property
    def enemy(self) -> EntityBuilder:
        """ O criador do adversário """
        return self.__enemy

    def create(self):
        """ Cria a partida """
        if self.__game_mode is None:
            raise AttributesNotSetException
        return Match(
            self.__game_mode,
            self.__player.get_result(),
            self.__enemy.get_result()
        )

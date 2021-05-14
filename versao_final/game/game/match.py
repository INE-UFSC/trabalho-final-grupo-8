""" Módulo relacionado à partida """


import random
from abc import abstractmethod

import pygame as pg

from game.manager.sound import Sound
from game.entity.entity import Entity, EntityBuilder


class Match:
    """ Uma partida do jogo """

    def __init__(
        self,
        player: Entity,
        enemy: Entity
    ):
        self.__player = player
        self.__enemy = enemy
        self.__set_new_array(player)
        self.__set_new_array(enemy)

    @property
    def player(self) -> Entity:
        """ O jogador """
        return self.__player

    @property
    def enemy(self) -> Entity:
        """ O adversário """
        return self.__enemy

    @abstractmethod
    def __set_new_array(self, entity: Entity):
        """ Define um novo array para uma entidade """
        new_array = list(range(10))
        random.shuffle(new_array)
        entity.array.numbers = new_array
        entity.interactor.set_array(entity.array)

    def update(self):
        """ Atualiza a partida """
        for entity in [self.__player, self.__enemy]:
            entity.interactor.update()
            if entity.array.is_sorted():
                Sound().play('FinishedSorting')
                entity.data.score += 10
                self.__set_new_array(entity)

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
        return Match(
            self.__player.get_result(),
            self.__enemy.get_result()
        )

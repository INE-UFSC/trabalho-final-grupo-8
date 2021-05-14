""" Módulo para as classes de comportamento """


import random
from abc import ABC, abstractmethod
from typing import Optional

from game.exceptions import AttributesNotSetException
from game.entity.entity import Entity
from game.utils import Timer


def set_random_array(entity: Entity):
    """ Define um novo array para uma entidade """
    new_array = list(range(10))
    random.shuffle(new_array)
    entity.array.numbers = new_array
    entity.interactor.set_array(entity.array)


class GameMode(ABC):
    """ Como o inimigo se comporta """

    @abstractmethod
    def set_entities(self, player: Entity, enemy: Entity) -> None:
        """ Define as entidade que o game mode deve lidar """

    @abstractmethod
    def update(self) -> None:
        """ Atualiza as entidades e suas pontuações """


class TimedGameMode(GameMode):
    """
    O inimigo é atualizado conforme
    um determinado período de tempo
    """

    def __init__(self) -> None:
        self.__timed_entity: Optional[Entity] = None
        self.__entity: Optional[Entity] = None
        self.__timer: Optional[Timer] = None

    def set_entities(self, player: Entity, enemy: Entity) -> None:
        if not isinstance(player, Entity) or not isinstance(enemy, Entity):
            raise TypeError
        self.__timed_entity = enemy
        self.__timer = Timer(1.0)
        self.__entity = player
        set_random_array(player)
        set_random_array(enemy)

    def update(self) -> None:
        if self.__timed_entity is None or self.__entity is None:
            raise AttributesNotSetException

        # Atualiza a entidade de timer
        if self.__timer is not None and self.__timer.timeout:
            self.__timed_entity.interactor.update()
        if self.__timed_entity.interactor.is_done():
            self.__timed_entity.data.score += 10
            set_random_array(self.__timed_entity)

        # Atualiza o jogador
        self.__entity.interactor.update()
        if self.__entity.interactor.is_done():
            self.__entity.data.score += 10
            set_random_array(self.__entity)


class TurnsGameMode(GameMode):
    """
    Cada jogador tem a sua vez de jogar
    """

    def __init__(self) -> None:
        self.__current_entity: Optional[Entity] = None
        self.__next_entity: Optional[Entity] = None

    def __next_turn(self):
        self.__current_entity, self.__next_entity = self.__next_entity, self.__current_entity

    def set_entities(self, player: Entity, enemy: Entity) -> None:
        if not isinstance(player, Entity) or not isinstance(enemy, Entity):
            raise TypeError
        self.__current_entity = player
        self.__next_entity = enemy
        set_random_array(player)
        set_random_array(enemy)

    def update(self) -> None:
        if self.__current_entity is None or self.__next_entity is None:
            raise AttributesNotSetException

        self.__current_entity.interactor.update()
        if self.__current_entity.interactor.has_moved():
            self.__current_entity.data.score -= 10
        if self.__current_entity.interactor.is_done():
            self.__current_entity.data.score += 100
            set_random_array(self.__current_entity)
        if self.__current_entity.interactor.has_moved():
            self.__next_turn()


def string_to_mode(name: str) -> GameMode:
    """
    Converte uma string para um modo de jogo específico

    Lançará um KeyError caso o modo não exista
    """
    algorithms = {
        "Tempo": TimedGameMode(),
        "Turnos": TurnsGameMode()
    }
    return algorithms[name]

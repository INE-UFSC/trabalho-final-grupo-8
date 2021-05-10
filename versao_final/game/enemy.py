""" Módulo para gerar o inimigo """


from abc import ABC, abstractmethod
from typing import Iterator, Optional
from game.command import Command
from game.array import Array
from game.interactor import Interactor
from game.sound import SoundManager
from game.algorithm import Algorithm
from game.utils import Timer


class Behaviour(ABC):
    """ Como o inimigo se comporta """

    @abstractmethod
    def should_update(self) -> bool:
        """ Retorna se o inimigo deve ser atualizado """


class TimedBehaviour(Behaviour):
    """
    O inimigo é atualizado conforme um
    determinado período de tempo
    """

    def __init__(self, timer: Timer):
        self.__timer = timer

    def should_update(self) -> bool:
        """ Se o timer já está superior ao período que o inimigo deve esperar """
        return self.__timer.timeout


def string_to_behaviour(name: str):
    """ Converte uma string em um comportamento """
    behaviours = {
        "Tempo": TimedBehaviour(Timer(1.0, auto_start=True))
    }
    return behaviours[name]


class EnemyInteractor(Interactor):
    """ Classe responsável pela ordenação do array conforme um período de tempo especificado """

    def __init__(
        self,
        algorithm: Algorithm,
        behaviour: Behaviour,
    ):
        self.__algorithm = algorithm
        self.__behaviour = behaviour
        self.__sort_iterator: Optional[Iterator[Command]] = None

    def set_array(self, array: Array) -> None:
        self.__sort_iterator = self.__algorithm.sort(array)

    def update(self):
        """ Atualiza o timer e checa se o array deve ser organizado """
        if self.__algorithm.is_done():
            return
        if self.__sort_iterator is None:
            return
        if self.__behaviour.should_update():
            try:
                command = next(self.__sort_iterator)
                command.execute()
            except StopIteration:  # Ordenação finalizou...
                SoundManager().play('finished')

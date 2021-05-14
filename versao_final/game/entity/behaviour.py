""" Módulo para as classes de comportamento """


from abc import ABC, abstractmethod
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

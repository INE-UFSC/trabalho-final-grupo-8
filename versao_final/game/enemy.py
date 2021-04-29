""" Módulo para gerar o inimigo """


from abc import ABC, abstractmethod
from game.algorithm import NewAlgorithm
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


class Enemy:
    """ Classe responsável pela ordenação do array conforme um período de tempo especificado """

    def __init__(
        self,
        algorithm: NewAlgorithm,
        behaviour: Behaviour
    ):
        self.__algorithm = algorithm
        self.__behaviour = behaviour
        self.__step_by_step = algorithm.one_step()

    def update(self):
        """ Atualiza o timer e checa se o array deve ser organizado """
        if self.__algorithm.is_done():
            return
        if self.__behaviour.should_update():
            try:
                next(self.__step_by_step).execute()
            except StopIteration:  # Ordenação finalizou...
                pass

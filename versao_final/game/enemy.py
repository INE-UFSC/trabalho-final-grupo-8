""" Módulo para gerar o inimigo """


from abc import ABC, abstractmethod
from typing import Optional
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


class Enemy:
    """ Classe responsável pela ordenação do array conforme um período de tempo especificado """

    def __init__(
        self,
        algorithm: Algorithm,
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


class AttributesNotSetException(Exception):
    """ Os atributos do criador não estão definidos """

    def __init__(self):
        super().__init__("Os atributos do criador não estão definidos.")


class EnemyBuilder:
    """ Responsável pela criação de inimigos """

    def __init__(self):
        self.__enemy: Optional[Enemy] = None
        self.__algorithm: Optional[Algorithm] = None
        self.__behaviour: Optional[Behaviour] = None

    def reset(self) -> None:
        """ Reinicia o estado do criador """
        self.__enemy = None
        self.__algorithm = None
        self.__behaviour = None

    def set_algorithm(self, algorithm: Algorithm) -> None:
        """ Define o algoritmo a ser a utilizado pelo inimigo """
        if isinstance(algorithm, Algorithm):
            self.__algorithm = algorithm

    def set_behaviour(self, behaviour: Behaviour) -> None:
        """ Define o comportamento do inimigo """
        if isinstance(behaviour, Behaviour):
            self.__behaviour = behaviour

    def get_result(self) -> Enemy:
        """ Retorna o inimigo, caso todos os parâmetros estejam estabelecidos """
        if self.__enemy is None:
            if (
                isinstance(self.__algorithm, Algorithm) and
                isinstance(self.__behaviour, Behaviour)
            ):
                self.__enemy = Enemy(self.__algorithm, self.__behaviour)
            else:
                raise AttributesNotSetException()
        return self.__enemy

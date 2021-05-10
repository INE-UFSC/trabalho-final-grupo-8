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
        if self.__behaviour.should_update():
            try:
                next(self.__sort_iterator).execute()
            except StopIteration:  # Ordenação finalizou...
                SoundManager().play('finished')


class AttributesNotSetException(Exception):
    """ Os atributos do criador não estão definidos """

    def __init__(self):
        super().__init__("Os atributos do criador não estão definidos.")


class EnemyInteractorBuilder:
    """ Responsável pela criação de inimigos """

    def __init__(self):
        self.__enemy: Optional[EnemyInteractor] = None
        self.__algorithm: Optional[Algorithm] = None
        self.__behaviour: Optional[Behaviour] = None
        self.__array: Optional[Array] = None

    def reset(self) -> None:
        """ Reinicia o estado do criador """
        self.__enemy = None

    def set_algorithm(self, algorithm: Algorithm) -> None:
        """ Define o algoritmo a ser a utilizado pelo inimigo """
        if isinstance(algorithm, Algorithm):
            self.__algorithm = algorithm

    def set_behaviour(self, behaviour: Behaviour) -> None:
        """ Define o comportamento do inimigo """
        if isinstance(behaviour, Behaviour):
            self.__behaviour = behaviour

    def set_array(self, array: Array) -> None:
        """ Define o array a ser ordenado pelo inimigo """
        if isinstance(array, Array):
            self.__array = array

    def get_result(self) -> EnemyInteractor:
        """ Retorna o inimigo, caso todos os parâmetros estejam estabelecidos """
        if self.__enemy is None:
            if (
                self.__algorithm is not None and
                self.__behaviour is not None and
                self.__array is not None
            ):
                self.__enemy = EnemyInteractor(
                    self.__algorithm, self.__behaviour, self.__array)
            else:
                raise AttributesNotSetException
        return self.__enemy

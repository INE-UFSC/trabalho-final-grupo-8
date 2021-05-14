""" Módulo para o DAO """


from abc import ABC, abstractmethod
from typing import Any, Dict
import json

from game.entity.data import Data


class DAO(ABC):
    """ Classe base para a implementação do DAO """

    def __init__(self, arquivo: str):
        self.__arquivo = arquivo
        self.__cache: Dict[str, Any] = {}

        try:
            self.load()
        except FileNotFoundError:
            self.dump()

    @property
    def cache(self):
        """ Retorna o cache """
        return self.__cache

    def load(self):
        """ Carrega de um arquivo JSON """
        with open(self.__arquivo) as arquivo:
            self.__cache = json.load(arquivo)

    def dump(self):
        """ Salva o cache em um arquivo JSON """
        with open(self.__arquivo, 'w') as arquivo:
            json.dump(self.__cache, arquivo)

    def get_all(self):
        """ Retorna o cache completo """
        return self.__cache

    @abstractmethod
    def add(self, obj: Any):
        """ Adiciona uma key ao dicionário """

    @abstractmethod
    def get(self, key: str):
        """ Recebe um valor conforme a key """

    @abstractmethod
    def remove(self, key: str):
        """ Remove uma key do dicionário """


class ScoreboardDAO(DAO):
    """ DAO para o placar """

    def add(self, obj: Data):
        self.cache[obj.name] = obj.score

    def get(self, key: str):
        return self.cache.get(key)

    def remove(self, key: str):
        del self.cache[key]

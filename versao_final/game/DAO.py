""" Módulo para o DAO """

from abc import ABC, abstractmethod
import json
from typing import Any


class DAO(ABC):
    """ Classe base para a implementação do DAO """

    def __init__(self, arquivo: str):
        self.__arquivo = arquivo
        self.__cache: dict[str, Any] = {}

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
    def add(self, obj):
        """ Adiciona uma key ao dicionário """

    @abstractmethod
    def get(self, key):
        """ Recebe um valor conforme a key """

    @abstractmethod
    def remove(self, key):
        """ Remove uma key do dicionário """
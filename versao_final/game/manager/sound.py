""" Módulo para lidar com áudio """


from typing import Dict, Optional

import pygame as pg

from game.utils import Singleton


class Sound(metaclass=Singleton):
    """ Classe que lida com os sons """

    def __init__(self, path: str = './', files: Optional[Dict[str, str]] = None):
        self.__path = path
        self.__sounds: Dict[str, pg.mixer.Sound] = {}
        pg.mixer.init()
        if files is not None:
            self.__load_dict(files)

    def __load_dict(self, files: Dict[str, str]) -> None:
        for key, path in files.items():
            self.load_sound(key, path)

    def load_sound(self, key: str, file: str) -> None:
        """ Carrega um novo som """
        self.__sounds[key] = pg.mixer.Sound(f"{self.__path}/{file}")

    def play(self, key: str) -> None:
        """ Retorna o objeto de som """
        self.__sounds[key].play()

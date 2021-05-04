""" Módulo para lidar com áudio """

from typing import Dict
import pygame as pg
from game.utils import Singleton


class SoundManager(metaclass=Singleton):
    """ Classe singleton que lida com os sons """

    def __init__(self, path: str = './'):
        self.__path = path
        self.__sounds: Dict[str, pg.mixer.Sound] = {}
        pg.mixer.init()

    def load_sound(self, key: str, file_name: str) -> None:
        """ Carrega um novo som """
        self.__sounds[key] = pg.mixer.Sound(f"{self.__path}/{file_name}")

    def play(self, key: str) -> None:
        """ Retorna o objeto de som """
        self.__sounds[key].play()

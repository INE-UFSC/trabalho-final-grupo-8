""" Genéricos para basear uma interface """

from enum import IntEnum
from abc import ABC, abstractmethod
from typing import Dict, Tuple
import pygame_gui
import pygame as pg
from pygame_gui.core.ui_element import UIElement


class UIState(IntEnum):
    """ Estados possíveis da interface """
    MAIN_MENU = 0
    BIG_O = 1
    SETUP_MENU = 2
    IN_GAME = 3
    VICTORY = 4
    DEFEAT = 5


class UIScene(ABC):
    """ Representa uma tela da interface gráfica """

    def __init__(
        self,
        manager: pygame_gui.UIManager,
        size: Tuple[int, int]
    ):
        self.__elements: Dict[str, UIElement] = {}
        self.__container = pygame_gui.elements.UIPanel(
            pg.Rect(0, 0, *size),
            0,
            manager
        )
        self.disable()
        self.make_elements()

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> UIState:
        """ O que deve ser feito para os eventos """

    @abstractmethod
    def make_elements(self) -> None:
        """ Cria os elementos, não deve ser chamado manualmente """

    @property
    def elements(self) -> Dict[str, pygame_gui.core.UIElement]:
        """ O dicionário de elementos da cena """
        return self.__elements

    @property
    def container(self) -> pygame_gui.elements.UIPanel:
        """ O elemento que contem todos os widgets """
        return self.__container

    def enable(self):
        """ Ativa a interface """
        self.__container.enable()
        self.__container.show()

    def disable(self):
        """ Desativa a interface """
        self.__container.disable()
        self.__container.hide()

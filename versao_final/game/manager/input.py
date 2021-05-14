""" Módulo para o gerenciador de inputs """


from typing import Callable, Dict, Optional, Set

import pygame as pg

from game.constants import MOUSE_DRAG
from game.utils import Singleton, end


class Input(metaclass=Singleton):
    """ Gerencia as teclas pressionadas """

    def __init__(self, mappings: Optional[Dict[int, str]] = None):
        self.__mappings = mappings if mappings is not None else {}
        self.__pressed: Set[str] = set()
        self.__just_pressed: Set[str] = set()
        self.__mouse_pos = (0, 0)
        self.__mouse_frames_pressed = 0
        self.__events: pg.EventList = None

    @property
    def events(self):
        """ Os eventos do frame atual """
        return self.__events

    @property
    def pressed(self):
        """ As teclas pressionadas """
        return self.__pressed

    @property
    def just_pressed(self):
        """ As teclas pressionadas no frame atual """
        return self.__just_pressed

    @property
    def mouse_pos(self):
        """ A posição do mouse """
        return self.__mouse_pos

    def __update_mouse_state(self):
        self.__mouse_pos = pg.mouse.get_pos()
        if self.__mappings.get(pg.MOUSEBUTTONDOWN) in self.__pressed:
            if self.__mouse_frames_pressed == 3:
                action_name = self.__mappings.get(MOUSE_DRAG)
                if action_name is not None:
                    self.__pressed.add(action_name)
                    self.__just_pressed.add(action_name)
            self.__mouse_frames_pressed += 1

    def update(self, custom_functions: list[Callable]):
        """ Atualiza as teclas """
        self.__just_pressed.clear()

        self.__update_mouse_state()

        self.__events = pg.event.get()
        for event in self.__events:
            if event.type == pg.QUIT:
                end()
            elif event.type in (pg.KEYDOWN, pg.KEYUP) and event.key in self.__mappings:
                action_name = self.__mappings[event.key]
                if event.type == pg.KEYDOWN:
                    self.__pressed.add(action_name)
                    self.__just_pressed.add(action_name)
                elif action_name in self.__pressed:
                    self.__pressed.remove(action_name)
            elif (
                event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP) and
                pg.MOUSEBUTTONDOWN in self.__mappings
            ):
                action_name = self.__mappings[pg.MOUSEBUTTONDOWN]
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.__pressed.add(action_name)
                    self.__just_pressed.add(action_name)
                elif event.type == pg.MOUSEBUTTONUP:
                    self.__mouse_frames_pressed = 0
                    self.__pressed.remove(action_name)
                    drag_action_name = self.__mappings.get(MOUSE_DRAG)
                    if drag_action_name in self.__pressed:
                        self.__pressed.remove(drag_action_name)
            for function in custom_functions:
                function(event)

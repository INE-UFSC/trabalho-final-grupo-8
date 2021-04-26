""" Classes de gerenciamento """


import sys
from typing import Any, Callable, Dict, List, Set, Tuple
import pygame as pg


class DisplayManager:
    """ Inicializa a janela """

    def __init__(self, caption: str, resolution: Tuple[int, int], framerate=60):
        pg.init()
        pg.font.init()

        pg.display.set_caption(caption)

        self.__framerate = framerate
        self.__clock = pg.time.Clock()
        self.__window = pg.display.set_mode(
            resolution,
            pg.RESIZABLE | pg.HWSURFACE | pg.DOUBLEBUF | pg.SCALED,
            32
        )
        self.tick()

    @property
    def window(self) -> pg.surface.Surface:
        """ A superfície da janela """
        return self.__window

    def tick(self) -> float:
        """ Atualiza o clock do jogo """
        return self.__clock.tick(self.__framerate) * 0.001

    def draw(self, surface: pg.Surface):
        """ Desenha uma superfície na janela """
        self.__window.fill((0, 0, 0))
        self.__window.blit(surface, (0, 0))
        pg.display.update()


MOUSE_DRAG = pg.event.custom_type()
EVENT_STRINGS = {
    "a": pg.K_a,
    "b": pg.K_b,
    "c": pg.K_c,
    "d": pg.K_d,
    "e": pg.K_e,
    "f": pg.K_f,
    "g": pg.K_g,
    "h": pg.K_h,
    "i": pg.K_i,
    "j": pg.K_j,
    "k": pg.K_k,
    "l": pg.K_l,
    "m": pg.K_m,
    "n": pg.K_n,
    "o": pg.K_o,
    "p": pg.K_p,
    "q": pg.K_q,
    "r": pg.K_r,
    "s": pg.K_s,
    "t": pg.K_t,
    "u": pg.K_u,
    "v": pg.K_v,
    "w": pg.K_w,
    "x": pg.K_x,
    "y": pg.K_y,
    "z": pg.K_z,
    "space": pg.K_SPACE,
    "esc": pg.K_ESCAPE,
    "up": pg.K_UP,
    "down": pg.K_DOWN,
    "left": pg.K_LEFT,
    "right": pg.K_RIGHT,
    "mouse_click": pg.MOUSEBUTTONDOWN,
    "mouse_drag": MOUSE_DRAG
}


class InputManager:
    """ Gerencia as teclas pressionadas """

    def __init__(self, mappings: Dict[str, str]):
        self.__mappings = {EVENT_STRINGS[k]: m for m, k in mappings.items()}
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
            if self.__mouse_frames_pressed == 5:
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
                pg.quit()
                sys.exit()
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

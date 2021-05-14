""" Módulo para o resultado da partida """


import pygame_gui
import pygame as pg

from game.ui.scene import UIScene, UIState
from game.game.state import GameState
from typing import Tuple


class Victory(UIScene):
    def __init__(self, state: GameState, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size)
        self.__state = state
        self.__font = manager.get_theme().get_font_dictionary().find_font(16, "MatchupPro")

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        pygame_gui.elements.UILabel(
            pg.Rect(0, 40, size[0], 48),
            "VITORIA!",
            manager,
            container=self.container,
            object_id="victory"
        )

        self.elements["Score"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 - 80, size[1] - 140, 160, 40),
            "placar de pontos",
            manager,
            container=self.container,
            object_id="green_button"
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["Score"]:
                    return UIState.SCORE
        return UIState.VICTORY


class Defeat(UIScene):
    def __init__(self, state: GameState, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size)
        self.__state = state
        self.__font = manager.get_theme().get_font_dictionary().find_font(16, "MatchupPro")

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        pygame_gui.elements.UILabel(
            pg.Rect(0, 40, size[0], 48),
            "DERROTA!",
            manager,
            container=self.container,
            object_id="lose"
        )

        self.elements["Score"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 - 80, size[1] - 140, 160, 40),
            "placar de pontos",
            manager,
            container=self.container,
            object_id="red_button"
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["Score"]:
                    return UIState.SCORE
        return UIState.DEFEAT


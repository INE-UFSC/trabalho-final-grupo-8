""" Módulo para o resultado da partida """


from typing import Tuple

import pygame_gui
import pygame as pg

from game.ui.scene import UIScene, UIState
from game.game.state import GameState


class Victory(UIScene):
    """ Cena de vitória """

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        pygame_gui.elements.UILabel(
            pg.Rect(0, 40, size[0], 48),
            "VITÓRIA!",
            manager,
            container=self.container,
            object_id="victory"
        )

        self.elements["Score"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 - 80, size[1] - 140, 160, 40),
            "Ver placar de pontos",
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
    """ Cena de derrota """

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
            "Ver placar de pontos",
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

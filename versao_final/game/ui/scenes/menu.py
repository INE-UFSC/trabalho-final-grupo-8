""" Módulo para o menu principal """


import pygame_gui
import pygame as pg

from game.ui.scene import UIScene, UIState
from game.utils import end


class Menu(UIScene):
    """ A tela inicial do jogo """

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        pygame_gui.elements.UILabel(
            pg.Rect(0, 40, size[0], 48),
            "Sort it!",
            manager,
            container=self.container,
            object_id="title"
        )
        self.elements["PlayButton"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 - 80, size[1] - 140, 160, 40),
            "Jogar",
            manager,
            container=self.container,
            object_id="green_button"
        )
        self.elements["ExitButton"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 - 80, size[1] - 80, 160, 40),
            "Sair",
            manager,
            container=self.container,
            object_id="red_button"
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["PlayButton"]:
                    return UIState.SETUP_MENU
                if event.ui_element == self.elements["ExitButton"]:
                    end()
        return UIState.MAIN_MENU

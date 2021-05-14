""" Módulo para a cena da tabela de Big O """


import pygame_gui
import pygame as pg

from game.ui.scene import UIScene, UIState


class BigO(UIScene):
    """ Classe da tabela de big o """

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        pygame_gui.elements.UIImage(
            pg.Rect((0, 0), size),
            pg.image.load('./assets/TabelaBigO.png'),
            manager,
            container=self.container
        )
        self.elements["ExitButton"] = pygame_gui.elements.UIButton(
            pg.Rect(10, size[1] - 50, size[0] - 20, 40),
            "Voltar",
            manager,
            container=self.container,
            object_id="red_button"
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["ExitButton"]:
                    return UIState.SETUP_MENU
        return UIState.BIG_O

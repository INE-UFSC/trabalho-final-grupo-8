""" Módulo para a cena de informações """


import pygame_gui
import pygame as pg

from game.ui.scene import UIScene, UIState


class Info(UIScene):
    """ Dá informações sobre o tempo de execução dos algoritmos """

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        self.elements["Voltar"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 - 80, size[1] - 60, (size[0] // 2) - 25, 40),
            "Voltar",
            manager,
            container=self.container,
            object_id="voltar"
        )

        self.elements["BigOWorst"] = pygame_gui.elements.UITextBox(
            "Despacito",
            pg.Rect(10, 100, size[0]-20, 50),
            manager,
            container=self.container
        )
        self.elements["BigOAvg"] = pygame_gui.elements.UITextBox(
            "Despacito",
            pg.Rect(10, 100, size[0]-20, 130),
            manager,
            container=self.container
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["Voltar"]:
                    return UIState.SETUP_MENU
        return UIState.INFO_MENU

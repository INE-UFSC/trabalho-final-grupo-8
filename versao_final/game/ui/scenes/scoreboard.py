""" Módulo para a implementação do scoreboard """


from typing import Any, Dict, Tuple

import pygame_gui
import pygame as pg

from game.ui.scene import UIScene, UIState
from game.game.state import GameState


def scoreboard_to_string(scoreboard: Dict[str, Any]) -> str:
    """ Processa o placar em uma string de múltiplas linhas """
    string = ""
    for index, (name, score) in enumerate(
        sorted(
            scoreboard.items(), key=lambda i: i[1], reverse=True
        )
    ):
        string += f"{index+1} - {name}: {score}<br>"
    return string


class Scoreboard(UIScene):
    """ Cena do placar """

    def __init__(
        self,
        state: GameState,
        manager: pygame_gui.UIManager,
        size: Tuple[int, int]
    ):
        super().__init__(manager, size)
        self.__state = state

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        pygame_gui.elements.UILabel(
            pg.Rect((size[0]//2) - 50, 0, 100, 16),
            "Pontuação: ",
            manager,
            container=self.container
        )

        self.elements["Scoreboard"] = pygame_gui.elements.UITextBox(
            "",
            pg.Rect(10, 20, size[0] - 20, 200),
            manager,
            container=self.container
        )

        self.elements["Sair"] = pygame_gui.elements.UIButton(
            pg.Rect(10, size[1] - 60, size[0] - 20, 40),
            "Voltar",
            manager,
            container=self.container,
            object_id="red_button"
        )

    def enable(self):
        if self.__state.match is not None:
            self.__state.scoreboard.add(self.__state.match.player.data)
        self.elements["Scoreboard"].html_text = scoreboard_to_string(
            self.__state.scoreboard.get_all()
        )
        self.elements["Scoreboard"].rebuild()
        super().enable()

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["Sair"]:
                    return UIState.MAIN_MENU
        return UIState.SCORE

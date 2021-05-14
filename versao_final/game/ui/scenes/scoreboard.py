
import pygame_gui
import pygame as pg

from game.ui.scene import UIScene, UIState
from game.game.state import GameState
from typing import Tuple


class Scoreboard(UIScene):

    def __init__(self, state: GameState, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size)
        self.__state = state
        self.__font = manager.get_theme().get_font_dictionary().find_font(16, "MatchupPro")

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        pygame_gui.elements.UILabel(
            pg.Rect((size[0]//2) - 50, 0, 100, 16),
            "Pontuação: ",
            manager,
            container=self.container
        )

        self.elements["AlgorithmDescription"] = pygame_gui.elements.UITextBox(
            "kajdkajhsdkajhsdkahsdkajhsdkjahskdjhaksjdhakjshdakjshdkajshdkajshdkashdkajhsdkajhsdkajhsdkjahsdkjahksdjhakjsdhkashdkajshdshdkajshdkajshdkashdkajhsdkajhsdkajhsdkjahsdkjahksdjhakjsdhkashdkajshshdkajshdkajshdkashdkajhsdkajhsdkajhsdkjahsdkjahksdjhakjsdhkashdkajshshdkajshdkajshdkashdkajhsdkajhsdkajhsdkjahsdkjahksdjhakjsdhkashdkajshshdkajshdkajshdkashdkajhsdkajhsdkajhsdkjahsdkjahksdjhakjsdhkashdkajshkajhsdkahsdkajhsdka",
            pg.Rect(10, 20, size[0] - 20, 200),
            manager,
            container=self.container
        )

        self.elements["PlayAgain"] = pygame_gui.elements.UIButton(
            pg.Rect(10, size[1] - 60, (size[0] // 2) - 25, 40),
            "Jogar de novo",
            manager,
            container=self.container,
            object_id="green_button"
        )

        self.elements["Sair"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 + 10, size[1] - 60, (size[0] // 2) - 25, 40),
            "Sair",
            manager,
            container=self.container,
            object_id="red_button"
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["PlayAgain"]:
                    return UIState.SETUP_MENU
                if event.ui_element == self.elements["Sair"]:
                    return end()
        return UIState.SCORE

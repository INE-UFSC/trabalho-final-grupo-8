""" Módulo para os dados da interface durante o jogo """


from typing import Tuple, Union

import pygame_gui
import pygame as pg

from game.constants import DEFEAT, SCORE_CHANGED, TIME_CHANGED, VICTORY
from game.ui.scene import UIScene, UIState
from game.game.state import GameState
from game.utils import seconds_as_string


class InGame(UIScene):
    """ A tela durante o jogo """

    def __init__(self, state: GameState, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size)
        self.__state = state
        self.__font = manager.get_theme().get_font_dictionary().find_font(16, "MatchupPro")

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        self.elements["PlayerName"] = pygame_gui.elements.UILabel(
            pg.Rect(0, size[1]//2 - 32, 16, 16),
            "",
            manager,
            container=self.container,
            object_id="blue_label"
        )
        self.elements['PlayerScore'] = pygame_gui.elements.UILabel(
            pg.Rect(0, size[1]//2, 16, 16),
            "",
            manager,
            container=self.container,
            object_id="blue_label"
        )
        self.elements['EnemyName'] = pygame_gui.elements.UILabel(
            pg.Rect(0, size[1]//2 - 32, 16, 16),
            "",
            manager,
            container=self.container,
            object_id="red_label",
            anchors={
                'left': 'right',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            }
        )
        self.elements['EnemyScore'] = pygame_gui.elements.UILabel(
            pg.Rect(0, size[1]//2, 16, 16),
            "",
            manager,
            container=self.container,
            object_id="red_label",
            anchors={
                'left': 'right',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            }
        )
        self.elements['Timer'] = pygame_gui.elements.UILabel(
            pg.Rect(
                size[0] // 2 - 32,
                size[1] // 2,
                64,
                32
            ),
            "",
            manager,
            container=self.container,
            object_id="yellow_label"
        )

    def __update_label(
        self,
        element: str,
        text: Union[str, int]
    ):
        text = str(text)
        self.elements[element].set_dimensions(self.__font.size(text))
        if element.startswith('Enemy'):
            self.elements[element].set_relative_position((
                -self.__font.size(text)[0],
                self.elements[element].rect.y
            ))
        elif element == 'Timer':
            self.elements[element].set_position((
                self.container.rect.w // 2 - self.__font.size(text)[0] // 2,
                self.container.rect.h // 2
            ))
        self.elements[element].set_text(text)

    def handle_event(self, event: pg.event.Event) -> UIState:
        if self.__state.match is not None:
            if event.type == SCORE_CHANGED:
                player = self.__state.match.player.data
                enemy = self.__state.match.enemy.data
                for entity, label in [(player, "PlayerScore"), (enemy, "EnemyScore")]:
                    if event.name == entity.name:
                        self.__update_label(
                            label,
                            entity.score
                        )
                        break
            if event.type == VICTORY:
                return UIState.VICTORY
            if event.type == DEFEAT:
                return UIState.DEFEAT
            if event.type == TIME_CHANGED:
                self.__update_label("Timer", seconds_as_string(event.value))
        return UIState.IN_GAME

    def enable(self):
        if self.__state.match is not None:
            player = self.__state.match.player.data
            enemy = self.__state.match.enemy.data
            self.__update_label('PlayerName', player.name)
            self.__update_label('PlayerScore', player.score)
            self.__update_label('EnemyName', enemy.name)
            self.__update_label('EnemyScore', enemy.score)
        super().enable()

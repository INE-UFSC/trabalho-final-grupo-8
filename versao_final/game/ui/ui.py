""" Módulo para o gerenciador da user interface """


from typing import Tuple, Dict

import pygame_gui
import pygame as pg

from game.game.state import GameState
from game.ui.scene import UIState, UIScene
from game.ui.scenes.game import InGame
from game.ui.scenes.setup import Setup
from game.ui.scenes.menu import Menu
from game.ui.scenes.big_o import BigO
from game.ui.scenes.results import Victory, Defeat
from game.ui.scenes.scoreboard import Scoreboard


class UI:
    """ Envolve o módulo pygame_gui """

    def __init__(self, game_state: GameState, size: Tuple[int, int]):
        self.__manager = pygame_gui.UIManager(
            size,
            theme_path="./assets/theme.json"
        )
        self.__state: UIState = UIState.MAIN_MENU
        self.__layouts: Dict[UIState, UIScene] = {
            UIState.MAIN_MENU: Menu(self.__manager, size),
            UIState.SETUP_MENU: Setup(game_state, self.__manager, size),
            UIState.IN_GAME: InGame(game_state, self.__manager, size),
            UIState.VICTORY: Victory(game_state, self.__manager, size),
            UIState.DEFEAT: Defeat(game_state, self.__manager, size),
            UIState.SCORE: Scoreboard(game_state, self.__manager, size),
            UIState.BIG_O: BigO(self.__manager, size)
        }
        self.__layouts[self.__state].enable()

    @property
    def state(self):
        """ Retorna o estado atual da interface gráfica """
        return self.__state

    def in_game(self):
        """ Se está no estado de jogo """
        return self.__state == UIState.IN_GAME

    def change_state(self, next_state: UIState):
        """ Troca de estado """
        self.__layouts[self.__state].disable()
        self.__state = next_state
        self.__layouts[self.__state].enable()

    def handle_event(self, event):
        """ Lida com um evento específico """
        next_state = self.__layouts[self.__state].handle_event(event)
        self.__manager.process_events(event)
        if next_state != self.__state:
            self.change_state(next_state)

    def update(self, delta_time: float):
        """ Atualiza conforme o delta time """
        self.__manager.update(delta_time)

    def draw(self, surface: pg.Surface):
        """ Desenha a interface apropriada na superfície """
        self.__manager.draw_ui(surface)

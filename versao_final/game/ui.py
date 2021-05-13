""" Implementação da interface gráfica """


from enum import IntEnum
from abc import ABC, abstractmethod
from typing import Dict, Tuple
import pygame_gui
import pygame as pg
from pygame_gui.core.ui_element import UIElement
from game.algorithm import string_to_algorithm
from game.enemy import EnemyInteractor, string_to_behaviour
from game.match import Data
from game.state import GameState


class UIState(IntEnum):
    """ Estados possíveis da interface """
    MAIN_MENU = 0
    SETUP_MENU = 1
    IN_GAME = 2
    VICTORY = 3
    DEFEAT = 4


class UIScene(ABC):
    """ Representa uma tela da interface gráfica """

    def __init__(
        self,
        manager: pygame_gui.UIManager,
        size: Tuple[int, int]
    ):
        self.__elements: Dict[str, UIElement] = {}
        self.__container = pygame_gui.elements.UIPanel(
            pg.Rect(0, 0, *size),
            0,
            manager
        )
        self.make_elements()
        self.disable()

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> UIState:
        """ O que deve ser feito para os eventos """

    @abstractmethod
    def make_elements(self) -> None:
        """ Cria os elementos, não deve ser chamado manualmente """

    @property
    def container(self) -> pygame_gui.elements.UIPanel:
        """ O elemento que contem todos os widgets """
        return self.__container

    @property
    def elements(self) -> Dict[str, pygame_gui.core.UIElement]:
        """ O dicionário de elementos da cena """
        return self.__elements

    def enable(self):
        """ Ativa a interface """
        self.__container.enable()
        self.__container.show()

    def disable(self):
        """ Desativa a interface """
        self.__container.disable()
        self.__container.hide()


class SetupMenu(UIScene):
    """ A tela de preparação do jogo """

    def __init__(self, state: GameState, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size)
        self.__state = state

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        self.elements["NameBox"] = pygame_gui.elements.UITextEntryLine(
            pg.Rect(10, 10, size[0] - 20, 20),
            manager,
            container=self.container
        )
        self.elements["NameBox"].set_text("John")
        self.elements["ModeSelector"] = pygame_gui.elements.UIDropDownMenu(
            ["Tempo", "Turnos"],
            "Tempo",
            pg.Rect(10, 40, size[0]-20, 20),
            manager,
            container=self.container,
        )
        self.elements["AlgorithmSelector"] = pygame_gui.elements.UIDropDownMenu(
            [
                "Quicksort (Lomuto)",
                "Bubble Sort"
            ],
            "Quicksort (Lomuto)",
            pg.Rect(10, 70, size[0]-20, 20),
            manager,
            container=self.container
        )
        self.elements["AlgorithmDescription"] = pygame_gui.elements.UITextBox(
            "Descrição do algoritmo...",
            pg.Rect(10, 100, size[0]-20, 130),
            manager,
            container=self.container
        )
        self.elements["PlayButton"] = pygame_gui.elements.UIButton(
            pg.Rect(20, size[1] - 60, (size[0] // 2) - 25, 40),
            "Jogar",
            manager,
            container=self.container,
            object_id="green_button"
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.elements["AlgorithmSelector"]:
                    self.elements["AlgorithmDescription"].html_text = event.text
                    self.elements["AlgorithmDescription"].rebuild()
                    self.elements["AlgorithmDescription"].set_active_effect(
                        pygame_gui.TEXT_EFFECT_TYPING_APPEAR
                    )
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["PlayButton"]:
                    name = self.elements["NameBox"].get_text()
                    mode = self.elements["ModeSelector"].current_state.selected_option
                    algorithm = self.elements["AlgorithmSelector"].current_state.selected_option
                    try:
                        self.__state.match_factory.player.set_data(Data(name))
                        self.__state.match_factory.enemy.set_data(
                            Data("Inimigo"))
                        self.__state.match_factory.enemy.set_interactor(
                            EnemyInteractor(
                                string_to_algorithm(algorithm),
                                string_to_behaviour(mode)
                            )
                        )
                        self.__state.match = self.__state.match_factory.create(
                            [15, 0, 10, 8, 2, 1, 5, 7]
                        )
                    except ValueError:
                        print("Erro na construção do jogo...")
                    return UIState.IN_GAME
        return UIState.SETUP_MENU


class InGameMenu(UIScene):
    """ A tela durante o jogo """

    def __init__(self, state: GameState, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size)
        self.__state = state

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
        ),
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
                size[0] // 2 - 20,
                size[1] // 2,
                40,
                16
            ),
            "",
            manager,
            container=self.container,
            object_id="yellow_label"
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            pass
        return UIState.IN_GAME


class UI:
    """ Envolve o módulo pygame_gui """

    def __init__(self, game_state: GameState, size: Tuple[int, int]):
        self.__manager = pygame_gui.UIManager(
            size,
            # theme_path="./assets/theme.json"
        )
        self.__state: UIState = UIState.SETUP_MENU
        self.__layouts: Dict[UIState, UIScene] = {
            UIState.SETUP_MENU: SetupMenu(game_state, self.__manager, size),
            UIState.IN_GAME: InGameMenu(game_state, self.__manager, size)
        }
        self.__layouts[self.__state].enable()

    @ property
    def state(self):
        """ Retorna o estado atual da interface gráfica """
        return self.__state

    def in_game(self):
        """ Se está no estado de jogo """
        return self.__state == UIState.SETUP_MENU

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

""" Módulo de wrapper para a interface """


from enum import IntEnum
from abc import ABC, abstractmethod
from game.state import GameState
from typing import Dict, Tuple
import pygame as pg
import pygame_gui
from game.enemy import EnemyInteractor, string_to_behaviour
from game.algorithm import string_to_algorithm
from game.match import Data
from game.utils import end


class UIState(IntEnum):
    """ Estados possíveis da interface """
    MAIN_MENU = 0
    SETUP_MENU = 1
    IN_GAME = 2
    VICTORY = 3
    DEFEAT = 4


class UIScene(ABC):
    """ Representa uma tela da interface gráfica """

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> UIState:
        """ O que deve ser feito para os eventos """

    @property
    @abstractmethod
    def container(self) -> pygame_gui.elements.UIPanel:
        """ O elemento que contem todos os widgets """

    def enable(self):
        """ Ativa a interface """
        self.container.enable()
        self.container.show()

    def disable(self):
        """ Desativa a interface """
        self.container.disable()
        self.container.hide()


class MainMenu(UIScene):
    """ Representa o menu principal """

    def __init__(self, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        self.__container = pygame_gui.elements.UIPanel(
            pg.Rect(0, 0, *size),
            0,
            manager
        )
        self.disable()

        pygame_gui.elements.UILabel(
            pg.Rect(0, 40, size[0], 48),
            "Sort it!",
            manager,
            container=self.__container,
            object_id="title"
        )
        self.__play_button = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 - 80, size[1] - 140, 160, 40),
            "Jogar",
            manager,
            container=self.__container,
            object_id="green_button"
        )
        self.__exit_button = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 - 80, size[1] - 80, 160, 40),
            "Sair",
            manager,
            container=self.__container,
            object_id="red_button"
        )

    @property
    def container(self) -> pygame_gui.elements.UIPanel:
        return self.__container

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.__play_button:
                    return UIState.SETUP_MENU
                if event.ui_element == self.__exit_button:
                    end()
        return UIState.MAIN_MENU


class SetupMenu(UIScene):
    """ Seleção do modo de jogo """

    def __init__(
        self,
        state: GameState,
        manager: pygame_gui.UIManager,
        size: Tuple[int, int]
    ):
        self.__state = state
        self.__container = pygame_gui.elements.UIPanel(
            pg.Rect(0, 0, *size),
            0,
            manager
        )
        self.disable()

        pygame_gui.elements.UILabel(
            pg.Rect(10, 10, 40, 20),
            "Nome:",
            manager,
            container=self.__container
        )
        self.__name = pygame_gui.elements.UITextEntryLine(
            pg.Rect(50, 10, size[0] - 60, 20),
            manager,
            container=self.__container
        )
        self.__name.set_text("John Doe")

        pygame_gui.elements.UILabel(
            pg.Rect(10, 40, 40, 20),
            "Modo:",
            manager,
            container=self.__container
        )
        self.__mode = pygame_gui.elements.UIDropDownMenu(
            ["Tempo", "Turnos"],
            "Tempo",
            pg.Rect(50, 40, size[0]-60, 20),
            manager,
            container=self.__container,
        )

        pygame_gui.elements.UILabel(
            pg.Rect(10, 70, 70, 20),
            "Algoritmo:",
            manager,
            container=self.__container
        )
        self.__algorithm = pygame_gui.elements.UIDropDownMenu(
            [
                "Quicksort (Lomuto)",
                "Bubble Sort"
            ],
            "Quicksort (Lomuto)",
            pg.Rect(80, 70, size[0]-90, 20),
            manager,
            container=self.__container
        )

        self.__play_button = pygame_gui.elements.UIButton(
            pg.Rect(20, size[1] - 60, (size[0] // 2) - 25, 40),
            "Jogar",
            manager,
            container=self.__container,
            object_id="green_button"
        )
        self.__back_button = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 + 10, size[1] - 60, (size[0] // 2) - 25, 40),
            "Voltar",
            manager,
            container=self.__container,
            object_id="red_button"
        )

    @property
    def container(self) -> pygame_gui.elements.UIPanel:
        return self.__container

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.__play_button:
                    name = self.__name.get_text()
                    mode = self.__mode.current_state.selected_option
                    algorithm = self.__algorithm.current_state.selected_option

                    self.__state.match_factory.player.set_data(Data(name))
                    self.__state.match_factory.enemy.set_data(Data("Inimigo"))
                    self.__state.match_factory.enemy.set_interactor(
                        EnemyInteractor(
                            string_to_algorithm(algorithm),
                            string_to_behaviour(mode)
                        )
                    )
                    self.__state.match = self.__state.match_factory.create(
                        [15, 0, 10, 8, 2, 1, 5, 7]
                    )
                    return UIState.IN_GAME
                if event.ui_element == self.__back_button:
                    return UIState.MAIN_MENU
        return UIState.SETUP_MENU


class InGameMenu(UIScene):
    """ Tela a ser mostrada durante o jogo """

    def __init__(
        self,
        _: GameState,
        manager: pygame_gui.UIManager,
        size: Tuple[int, int]
    ):
        self.__container = pygame_gui.elements.UIPanel(
            pg.Rect(0, 0, *size),
            0,
            manager
        )
        self.disable()

        # font = manager.get_theme().get_font_dictionary().find_font(16, "MatchupPro")

        # pygame_gui.elements.UILabel(
        #     pg.Rect(0, size[1] // 2 - 32, *
        #             font.size(GameState().player_data.name)),
        #     GameState().player_data.name,
        #     manager,
        #     container=self.__container,
        #     object_id="blue_label"
        # )
        # pygame_gui.elements.UILabel(
        #     pg.Rect(0, size[1] // 2 - 16, *
        #             font.size(str(GameState().player_data.score))),
        #     str(GameState().player_data.score),
        #     manager,
        #     container=self.__container,
        #     object_id="blue_label"
        # )

        # pygame_gui.elements.UILabel(
        #     pg.Rect(
        #         size[0] - font.size(GameState().enemy_data.name)[0],
        #         size[1] // 2 - 32,
        #         *font.size(GameState().enemy_data.name)
        #     ),
        #     GameState().enemy_data.name,
        #     manager,
        #     container=self.__container,
        #     object_id="red_label"
        # )
        # pygame_gui.elements.UILabel(
        #     pg.Rect(
        #         size[0] - font.size(str(GameState().enemy_data.score))[0],
        #         size[1] // 2 - 16,
        #         *font.size(str(GameState().enemy_data.score))
        #     ),
        #     str(GameState().enemy_data.score),
        #     manager,
        #     container=self.__container,
        #     object_id="red_label"
        # )

        # pygame_gui.elements.UILabel(
        #     pg.Rect(
        #         size[0] // 2 - 20,
        #         size[1] // 2,
        #         40,
        #         16
        #     ),
        #     "1:53",
        #     manager,
        #     container=self.__container,
        #     object_id="yellow_label"
        # )

    @property
    def container(self) -> pygame_gui.elements.UIPanel:
        return self.__container

    def handle_event(self, event: pg.event.Event):
        return UIState.IN_GAME


class UI:
    """ Envolve o módulo pygame_gui """

    def __init__(self, state: GameState, size: Tuple[int, int]):
        self.__manager = pygame_gui.UIManager(
            size, theme_path="./assets/theme.json"
        )
        self.__state: UIState = UIState.MAIN_MENU
        self.__layouts: Dict[UIState, UIScene] = {
            UIState.MAIN_MENU: MainMenu(self.__manager, size),
            UIState.SETUP_MENU: SetupMenu(state, self.__manager, size),
            UIState.IN_GAME: InGameMenu(state, self.__manager, size)
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

    def update(self, delta_time: float):
        """ Atualiza conforme o delta time """
        self.__manager.update(delta_time)

    def handle_event(self, event):
        """ Lida com um evento específico """
        next_state = self.__layouts[self.__state].handle_event(event)
        self.__manager.process_events(event)
        if next_state != self.__state:
            self.change_state(next_state)

    def draw(self, surface: pg.Surface):
        """ Desenha a interface apropriada na superfície """
        self.__manager.draw_ui(surface)

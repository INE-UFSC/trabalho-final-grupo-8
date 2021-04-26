""" Módulo de wrapper para a interface """


from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Dict, Tuple
import pygame as pg
import pygame_gui
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

    def __init__(
        self,
        manager: pygame_gui.UIManager,
        size: Tuple[int, int],
        object_id: str = "panel"
    ):
        """ Inicializa recebendo o manager e o tamanho da tela """
        self.__container = pygame_gui.elements.UIPanel(
            pg.Rect(0, 0, *size),
            0,
            manager,
            object_id=object_id
        )
        self.disable()

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> UIState:
        """ O que deve ser feito para os eventos """

    @property
    def container(self):
        """ O elemento que contem todos os widgets """
        return self.__container

    def enable(self):
        """ Ativa a interface """
        self.__container.enable()
        self.__container.show()

    def disable(self):
        """ Desativa a interface """
        self.__container.disable()
        self.__container.hide()


class MainMenu(UIScene):
    """ Representa o menu principal """

    def __init__(self, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size, "menu_background")
        pygame_gui.elements.UILabel(
            pg.Rect(0, 10, size[0], 48),
            "Sort it!",
            manager,
            container=self.container,
            object_id="title"
        )
        self.__play_button = pygame_gui.elements.UIButton(
            pg.Rect(10, 100, (size[0] // 2) - 15, 40),
            "Jogar",
            manager,
            container=self.container,
            object_id="green_button"
        )
        self.__exit_button = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 + 5, 100, (size[0] // 2) - 15, 40),
            "Sair",
            manager,
            container=self.container,
            object_id="red_button"
        )

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

    def __init__(self, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size, "menu_background")

        pygame_gui.elements.UILabel(
            pg.Rect(10, 10, 40, 20),
            "Nome:",
            manager,
            container=self.container
        )
        pygame_gui.elements.UITextEntryLine(
            pg.Rect(50, 10, size[0] - 60, 20),
            manager,
            container=self.container
        ).set_text("John Doe")

        pygame_gui.elements.UILabel(
            pg.Rect(10, 40, 40, 20),
            "Modo:",
            manager,
            container=self.container
        )
        pygame_gui.elements.UIDropDownMenu(
            ["Movimentos", "Tempo"],
            "Movimentos",
            pg.Rect(50, 40, size[0]-60, 20),
            manager,
            container=self.container,
        )

        pygame_gui.elements.UILabel(
            pg.Rect(10, 70, 70, 20),
            "Algoritmo:",
            manager,
            container=self.container
        )
        pygame_gui.elements.UIDropDownMenu(
            ["Quick Sort", "Bubble Sort"],
            "Quick Sort",
            pg.Rect(80, 70, size[0]-90, 20),
            manager,
            container=self.container
        )

        self.__play_button = pygame_gui.elements.UIButton(
            pg.Rect(10, 100, (size[0] // 2) - 15, 40),
            "Jogar",
            manager,
            container=self.container,
            object_id="green_button"
        )
        self.__back_button = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 + 5, 100, (size[0] // 2) - 15, 40),
            "Voltar",
            manager,
            container=self.container,
            object_id="red_button"
        )

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.__play_button:
                    return UIState.IN_GAME
                if event.ui_element == self.__back_button:
                    return UIState.MAIN_MENU
        return UIState.SETUP_MENU


class InGameMenu(UIScene):
    """ Tela a ser mostrada durante o jogo """

    def __init__(self, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size)

        font = manager.get_theme().get_font_dictionary().find_font(16, "MatchupPro")

        pygame_gui.elements.UILabel(
            pg.Rect(0, size[1] // 2 - 32, *font.size("John Doe")),
            "John Doe",
            manager,
            container=self.container,
            object_id="blue_label"
        )
        pygame_gui.elements.UILabel(
            pg.Rect(0, size[1] // 2 - 16, *font.size("1642")),
            "1642",
            manager,
            container=self.container,
            object_id="blue_label"
        )

        pygame_gui.elements.UILabel(
            pg.Rect(
                size[0] - font.size("Robô")[0],
                size[1] // 2 - 32,
                *font.size("Robô")
            ),
            "Robô",
            manager,
            container=self.container,
            object_id="red_label"
        )
        pygame_gui.elements.UILabel(
            pg.Rect(
                size[0] - font.size("437")[0],
                size[1] // 2 - 16,
                *font.size("437")
            ),
            "437",
            manager,
            container=self.container,
            object_id="red_label"
        )

        pygame_gui.elements.UILabel(
            pg.Rect(
                size[0] // 2 - 20,
                size[1] // 2,
                40,
                16
            ),
            "1:53",
            manager,
            container=self.container,
            object_id="yellow_label"
        )

    def handle_event(self, event: pg.event.Event):
        return UIState.IN_GAME


class UI:
    """ Envolve o módulo pygame_gui """

    def __init__(self, size: Tuple[int, int]):
        self.__manager = pygame_gui.UIManager(
            size, theme_path="./assets/theme.json"
        )
        self.__state: UIState = UIState.MAIN_MENU
        self.__layouts: Dict[UIState, UIScene] = {
            UIState.MAIN_MENU: MainMenu(self.__manager, size),
            UIState.SETUP_MENU: SetupMenu(self.__manager, size),
            UIState.IN_GAME: InGameMenu(self.__manager, size)
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

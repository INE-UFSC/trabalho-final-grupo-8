""" Módulo de wrapper para a interface """


from abc import ABC, abstractmethod
from typing import Tuple
import pygame as pg
import pygame_gui


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

    @abstractmethod
    def handle_event(self, event: pg.event.Event):
        """ O que deve ser feito para os eventos """

    @property
    def container(self):
        """ O elemento que contem todos os widgets """
        return self.__container

    def enable(self):
        """ Ativa a interface """
        self.__container.enable()

    def disable(self):
        """ Desativa a interface """
        self.__container.disable()


class MainMenu(UIScene):
    """ Representa o menu principal """

    def __init__(self, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size, object_id="#menu-background")
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
            container=self.container
        )
        self.__exit_button = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 + 5, 100, (size[0] // 2) - 15, 40),
            "Sair",
            manager,
            container=self.container
        )

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.__play_button:
                    print("Play")
                elif event.ui_element == self.__exit_button:
                    print("Exit")


class SetupMenu(UIScene):
    """ Seleção do modo de jogo """

    def __init__(self, manager: pygame_gui.UIManager, size: Tuple[int, int]):
        super().__init__(manager, size, object_id="#menu-background")

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

        pygame_gui.elements.UIButton(
            pg.Rect(10, 100, (size[0] // 2) - 15, 40),
            "Jogar",
            manager,
            container=self.container
        )
        pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 + 5, 100, (size[0] // 2) - 15, 40),
            "Voltar",
            manager,
            container=self.container
        )

    def handle_event(self, event: pg.event.Event):
        pass


class UI:
    """ Envolve o módulo pygame_gui """

    def __init__(self, size: Tuple[int, int]):
        self.__manager = pygame_gui.UIManager(
            size, theme_path="./assets/theme.json"
        )
        self.__current_layout = "MainMenu"
        self.__layouts = {
            "MainMenu": MainMenu(self.__manager, size)
            # "SetupMenu": SetupMenu(self.__manager, size)
        }

    def update(self, delta_time: float):
        """ Atualiza conforme o delta time """
        self.__manager.update(delta_time)

    def handle_event(self, event):
        """ Lida com um evento específico """
        self.__layouts[self.__current_layout].handle_event(event)
        self.__manager.process_events(event)

    def draw(self, surface: pg.Surface):
        """ Desenha a interface apropriada na superfície """
        self.__manager.draw_ui(surface)

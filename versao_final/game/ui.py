""" Módulo de wrapper para a interface """


from enum import IntEnum
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Union
import pygame as pg
import pygame_gui
from game.enemy import EnemyInteractor, string_to_behaviour
from game.algorithm import string_to_algorithm
from game.match import Data
from game.state import GameState
from game.utils import end


# Implementar em JSON
info_sorts = {
        "Bubble Sort": ["O algoritmo percorre o array diversas vezes,",
                       "e a cada passagem fazer flutuar para o topo o",
                       "maior elemento da sequência."],

        "Selection Sort": ["A ordenacao e feita de forma que o algoritmo procura",
                           " o menor valor do array e o posiciona na primeira posicao, ",
                           "trocando-o de lugar com o valor que ocupava tal posicao,",
                           " entao a busca pelo segundo menor comeca e ao fim ",
                           "posiciona o segundo menor valor na segunda posicao",
                           "e assim por diante."],

        "InsertionSort": ["Essa ordenação funciona como organizar cartas na mão, onde há",
        " uma parte organizada e outra não. A ordenação acontece avançando para a parte não organizada",
        " um item por vez, esse item é posto no lugar certo na parte ordenada, verificando do ultimo item organizado",
        " até o primero, parando quando encontrar um número menor"
        ],

        "IterativeQuicksort": "bla",

        "RecursiveQuicksort": ["O QuickSort escolhe o ulitmo como pivô da operação de ordenação e o comparará com elementos anteriores",
        " os separando em três grupos: menor, maior e igual. Isso três arrays distintos que precisam ser ordenados(exceto o de igualdade). ",
        " Para que isso aconteça, basta aplicar de novo a operação de quicksort em cada um desses arrays, até que eles fiquem com um elemento cada",
        " após isso, basta juntar os arrays e o resultado será o vetor ordenado "],
        
        "Quicksort (Lomuto)": ["O QuickSort escolhe o ulitmo como pivô da operação de ordenação e o comparará com elementos anteriores",
        " os separando em três grupos: menor, maior e igual. Isso três arrays distintos que precisam ser ordenados(exceto o de igualdade). ",
        " Para que isso aconteça, basta aplicar de novo a operação de quicksort em cada um desses arrays, até que eles fiquem com um elemento cada",
        " após isso, basta juntar os arrays e o resultado será o vetor ordenado "]
    }

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

        # Colocar a borda e atualizar conforme for mudando o algoritmo selecionado.
        for i in range(len(info_sorts[str(self.__algorithm.current_state.selected_option)])):
            self.__Bubble = pygame_gui.elements.UILabel(
                pg.Rect(20, (i * 10) + 80, 300, 20),
                info_sorts[str(self.__algorithm.current_state.selected_option)][i],
                manager,
                container=self.container,
                object_id="description",
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

        self.__font = manager.get_theme().get_font_dictionary().find_font(16, "MatchupPro")
        self.__elements = {
            'player_name': pygame_gui.elements.UILabel(
                pg.Rect(0, size[1]//2 - 32, 16, 16),
                "",
                manager,
                container=self.__container,
                object_id="blue_label"
            ),
            'player_score': pygame_gui.elements.UILabel(
                pg.Rect(0, size[1]//2, 16, 16),
                "",
                manager,
                container=self.__container,
                object_id="blue_label"
            ),

            'enemy_name': pygame_gui.elements.UILabel(
                pg.Rect(0, size[1]//2 - 32, 16, 16),
                "",
                manager,
                container=self.__container,
                object_id="red_label",
                anchors={
                    'left': 'right',
                    'right': 'right',
                    'top': 'top',
                    'bottom': 'bottom'
                }
            ),
            'enemy_score': pygame_gui.elements.UILabel(
                pg.Rect(0, size[1]//2, 16, 16),
                "",
                manager,
                container=self.__container,
                object_id="red_label",
                anchors={
                    'left': 'right',
                    'right': 'right',
                    'top': 'top',
                    'bottom': 'bottom'
                }
            ),

            'timer': pygame_gui.elements.UILabel(
                pg.Rect(
                    size[0] // 2 - 20,
                    size[1] // 2,
                    40,
                    16
                ),
                "1:53",
                manager,
                container=self.__container,
                object_id="yellow_label"
            )
        }

    def __update_label(
        self,
        element: str,
        text: Union[str, int]
    ):
        text = str(text)
        self.__elements[element].set_dimensions(self.__font.size(text))
        if element.startswith('enemy'):
            self.__elements[element].set_relative_position((
                -self.__font.size(text)[0],
                self.__elements[element].rect.y
            ))
        elif element == 'timer':
            self.__elements[element].set_position((
                self.__container.rect.w // 2 - self.__font.size(text),
                self.__container.rect.h // 2
            ))
        self.__elements[element].set_text(text)

    @property
    def container(self) -> pygame_gui.elements.UIPanel:
        return self.__container

    def enable(self) -> None:
        if self.__state.match is not None:
            player = self.__state.match.player.data
            enemy = self.__state.match.enemy.data
            # timer = self.__state.match.timer
            self.__update_label('player_name', player.name)
            self.__update_label('player_score', player.score)
            self.__update_label('enemy_name', enemy.name)
            self.__update_label('enemy_score', enemy.score)
        super().enable()

    def handle_event(self, event: pg.event.Event) -> UIState:
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

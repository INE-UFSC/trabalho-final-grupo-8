""" Implementação da interface gráfica """


from enum import IntEnum
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Union
import pygame_gui
import pygame as pg
from pygame_gui.core.ui_element import UIElement
from game.algorithm import string_to_algorithm
from game.enemy import EnemyInteractor, string_to_behaviour
from game.match import Data, SCORE_CHANGED
from game.state import GameState
from game.utils import end


INFO_SORTS = {
    "Bubble Sort": "O algoritmo percorre o array diversas vezes, e a cada passagem fazer flutuar para o topo o maior elemento da sequência.",

    "Selection Sort": "A ordenacao e feita de forma que o algoritmo procura o menor valor do array e o posiciona na primeira posicao, trocando-o de lugar com o valor que ocupava tal posicao, entao a busca pelo segundo menor comeca e ao fim posiciona o segundo menor valor na segunda posicao e assim por diante.",

    "InsertionSort": "Essa ordenação funciona como organizar cartas na mão, onde há uma parte organizada e outra não. A ordenação acontece avançando para a parte não organizada um item por vez, esse item é posto no lugar certo na parte ordenada, verificando do ultimo item organizado até o primero, parando quando encontrar um número menor",

    "Quicksort (Lomuto)": "O QuickSort escolhe o último como pivô da operação de ordenação e o comparará com elementos anteriores os separando em três grupos: menor, maior e igual. Isso três arrays distintos que precisam ser ordenados(exceto o de igualdade). Para que isso aconteça, basta aplicar de novo a operação de quicksort em cada um desses arrays, até que eles fiquem com um elemento cada após isso, basta juntar os arrays e o resultado será o vetor ordenado."
}


class UIState(IntEnum):
    """ Estados possíveis da interface """
    MAIN_MENU = 0
    SETUP_MENU = 1
    IN_GAME = 2
    VICTORY = 3
    DEFEAT = 4
    INFO_MENU = 5


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
        self.disable()
        self.make_elements()

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

class info(UIScene):
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
    
    
        
        
class MainMenu(UIScene):
    """ A tela inicial do jogo """

    def make_elements(self):
        size = self.container.rect.size
        manager = self.container.ui_manager

        pygame_gui.elements.UILabel(
            pg.Rect(0, 40, size[0], 48),
            "Sort it!",
            manager,
            container=self.container,
            object_id="title"
        )
        self.elements["PlayButton"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 - 80, size[1] - 140, 160, 40),
            "Jogar",
            manager,
            container=self.container,
            object_id="green_button"
        )
        self.elements["ExitButton"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 2 - 80, size[1] - 80, 160, 40),
            "Sair",
            manager,
            container=self.container,
            object_id="red_button"
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["PlayButton"]:
                    return UIState.SETUP_MENU
                if event.ui_element == self.elements["ExitButton"]:
                    end()
        return UIState.MAIN_MENU


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
        self.elements["InfoButton"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0]/2 + 10, size[1] - 60, (size[0] // 2) - 25, 40),
            "Info",
            manager,
            container=self.container,
            object_id="info_button"
        )
        self.elements["PlayButton"] = pygame_gui.elements.UIButton(
            pg.Rect(10, size[1] - 60, (size[0] // 2) - 25, 40),
            "Jogar",
            manager,
            container=self.container,
            object_id="green_button"
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.elements["AlgorithmSelector"]:
                    self.elements[
                        "AlgorithmDescription"].html_text = INFO_SORTS[event.text]
                    self.elements["AlgorithmDescription"].rebuild()
                    # self.elements["AlgorithmDescription"].set_active_effect(
                    #     pygame_gui.TEXT_EFFECT_TYPING_APPEAR
                    # )
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["InfoButton"]:
                    return UIState.INFO_MENU
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
                        self.__state.match = self.__state.match_factory.create()
                    except ValueError:
                        print("Erro na construção do jogo...")
                    return UIState.IN_GAME
        return UIState.SETUP_MENU


class InGameMenu(UIScene):
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
        elif element == 'timer':
            self.elements[element].set_position((
                self.container.rect.w // 2 - self.__font.size(text),
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
        return UIState.IN_GAME

    def enable(self):
        if self.__state.match is not None:
            player = self.__state.match.player.data
            enemy = self.__state.match.enemy.data
            # timer = self.__state.match.timer
            self.__update_label('PlayerName', player.name)
            self.__update_label('PlayerScore', player.score)
            self.__update_label('EnemyName', enemy.name)
            self.__update_label('EnemyScore', enemy.score)
        super().enable()


class UI:
    """ Envolve o módulo pygame_gui """

    def __init__(self, game_state: GameState, size: Tuple[int, int]):
        self.__manager = pygame_gui.UIManager(
            size,
            theme_path="./assets/theme.json"
        )
        self.__state: UIState = UIState.MAIN_MENU
        self.__layouts: Dict[UIState, UIScene] = {
            UIState.MAIN_MENU: MainMenu(self.__manager, size),
            UIState.SETUP_MENU: SetupMenu(game_state, self.__manager, size),
            UIState.IN_GAME: InGameMenu(game_state, self.__manager, size),
            UIState.INFO_MENU: info(self.__manager, size)
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

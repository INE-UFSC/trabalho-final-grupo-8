""" Módulo para a cena de setup """


from typing import Tuple

import pygame_gui
import pygame as pg

from game.array.algorithm import string_to_algorithm
from game.game.mode import string_to_mode
from game.ui.scene import UIScene, UIState
from game.entity.interactor import EnemyInteractor
from game.entity.data import Data
from game.game.state import GameState


INFO_SORTS = {
    "Bubble Sort": "O algoritmo percorre o array diversas vezes, e a cada passagem faz flutuar para o topo o maior elemento da sequência.",
    "Selection Sort": "A ordenação é feita de forma que o algoritmo procura o menor valor do array e o posiciona na primeira posição, trocando-o de lugar com o valor que ocupava tal posição, entao a busca pelo segundo menor começa e ao fim posiciona o segundo menor valor na segunda posição e assim por diante.",
    "Insertion Sort": "Essa ordenação funciona como organizar cartas na mão, onde há uma parte organizada e outra não. A ordenação acontece avançando para a parte não organizada um item por vez, esse item é posto no lugar certo na parte ordenada, verificando do ultimo item organizado até o primero, parando quando encontrar um número menor",
    "Quicksort (Lomuto)": "O QuickSort escolhe o último como pivô da operação de ordenação e o comparará com elementos anteriores os separando em três grupos: menor, maior e igual. Isso três arrays distintos que precisam ser ordenados(exceto o de igualdade). Para que isso aconteça, basta aplicar de novo a operação de quicksort em cada um desses arrays, até que eles fiquem com um elemento cada após isso, basta juntar os arrays e o resultado será o vetor ordenado.",
    "Quicksort (Hoare)": "O QuickSort de Hoare escolhe dois pointeiros no array, um no início e um no fim. O primeiro ponteiro começará a avançar na direção do segundo e, se encontrar um elemento maior que o segundo, ambos trocam de lugar. Quando isso acontecer o ponteiro da direita começa a se mover em direção ao da esquerda e se encontrar um valor maior, haverá mais uma troca e o outro ponteiro começará a se mover de novo. O processo acaba quando ambos ponteiros se encontram, que significa que o array foi totalmente percorrido e organizado."
}


class Setup(UIScene):
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
                "Bubble Sort",
                "Insertion Sort",
                "Selection Sort",
                "Quicksort (Lomuto)",
                "Quicksort (Hoare)"
            ],
            "Bubble Sort",
            pg.Rect(10, 70, size[0]-20, 20),
            manager,
            container=self.container
        )
        self.elements["AlgorithmDescription"] = pygame_gui.elements.UITextBox(
            INFO_SORTS["Bubble Sort"],
            pg.Rect(10, 100, size[0]-20, 130),
            manager,
            container=self.container
        )
        self.elements["PlayButton"] = pygame_gui.elements.UIButton(
            pg.Rect(10, size[1] - 50, size[0] // 3 - 20, 40),
            "Jogar",
            manager,
            container=self.container,
            object_id="green_button"
        )
        self.elements["InfoButton"] = pygame_gui.elements.UIButton(
            pg.Rect(size[0] // 3 + 10, size[1] - 50, size[0] // 3 - 20, 40),
            "Info",
            manager,
            container=self.container,
            object_id="info_button"
        )
        self.elements["ExitButton"] = pygame_gui.elements.UIButton(
            pg.Rect(
                2 * size[0] // 3 + 10,
                size[1] - 50,
                size[0] // 3 - 20,
                40
            ),
            "Voltar",
            manager,
            container=self.container,
            object_id="red_button"
        )

    def handle_event(self, event: pg.event.Event) -> UIState:
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.elements["AlgorithmSelector"]:
                    self.elements[
                        "AlgorithmDescription"].html_text = INFO_SORTS[event.text]
                    self.elements["AlgorithmDescription"].rebuild()
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements["InfoButton"]:
                    return UIState.BIG_O
                if event.ui_element == self.elements["ExitButton"]:
                    return UIState.MAIN_MENU
                if event.ui_element == self.elements["PlayButton"]:
                    name = self.elements["NameBox"].get_text()
                    mode = self.elements["ModeSelector"].current_state.selected_option
                    algorithm = self.elements["AlgorithmSelector"].current_state.selected_option
                    try:
                        self.__state.match_factory.player.set_data(Data(name))
                        self.__state.match_factory.enemy.set_data(
                            Data("Inimigo"))
                        self.__state.match_factory.enemy.set_interactor(
                            EnemyInteractor(string_to_algorithm(algorithm))
                        )
                        self.__state.match_factory.set_game_mode(
                            string_to_mode(mode)
                        )
                        self.__state.match = self.__state.match_factory.create()
                    except ValueError:
                        return UIState.SETUP_MENU
                    return UIState.IN_GAME
        return UIState.SETUP_MENU

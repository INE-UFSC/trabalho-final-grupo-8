""" Classes que interagem com o array """


from typing import Iterator, Optional
from abc import ABC, abstractmethod

from game.array.array import Array
from game.array.algorithm import Algorithm
from game.array.box import Box
from game.array.command import Command, SwapCommand
from game.entity.behaviour import Behaviour
from game.manager.input import Input
from game.manager.sound import Sound


class Interactor(ABC):
    """ Interage com um array ao ser atualizado """

    @abstractmethod
    def set_array(self, array: Array) -> None:
        """ Associa um novo array ao interactor """

    @abstractmethod
    def update(self) -> None:
        """ Modifica o array """


class PlayerInteractor(Interactor):
    """ Classe responsável pelo controle do player """

    def __init__(self):
        self.__array: Optional[Array] = None

    def __drop_box(self, dragging: Box):
        """ Solta a caixa """
        if self.__array is None:
            return
        for box in self.__array.boxes:
            if (
                box != dragging and
                abs(box.rect.centerx - dragging.rect.centerx) < 8 and
                abs(box.rect.centery - dragging.rect.centery) < 8
            ):
                command = SwapCommand(
                    self.__array,
                    self.__array.boxes.index(dragging),
                    self.__array.boxes.index(box)
                )
                command.execute()
                Sound().play('PlayerMove')
                break
        dragging.dragged = False

    def __handle_mouse(self):
        """ Atualiza conforme os inputs do mouse """
        inputs = Input()
        box_under_cursor = None
        dragging = None

        if self.__array is None:
            return

        for box in self.__array.boxes:
            if box.rect.collidepoint(*inputs.mouse_pos):
                box_under_cursor = box
            if box.dragged:
                dragging = box

        if "MouseDrag" in inputs.just_pressed and dragging is None:
            if box_under_cursor is not None:
                dragging = box_under_cursor
                dragging.dragged = True

        elif dragging is not None and not "MouseDrag" in inputs.pressed:
            self.__drop_box(dragging)

        if dragging is not None:
            dragging.rect.center = inputs.mouse_pos

    def set_array(self, array: Array) -> None:
        if not isinstance(array, Array):
            raise TypeError
        self.__array = array

    def update(self):
        """ Atualiza a interação do player com o seu array """
        self.__handle_mouse()


class EnemyInteractor(Interactor):
    """ Classe responsável pela ordenação do array """

    def __init__(
        self,
        algorithm: Algorithm,
        behaviour: Behaviour,
    ):
        self.__algorithm = algorithm
        self.__behaviour = behaviour
        self.__sort_iterator: Optional[Iterator[Command]] = None

    def set_array(self, array: Array) -> None:
        self.__sort_iterator = self.__algorithm.sort(array)

    def update(self):
        """ Atualiza o timer e checa se o array deve ser organizado """
        if self.__algorithm.is_done():
            return
        if self.__sort_iterator is None:
            return
        if self.__behaviour.should_update():
            try:
                command = next(self.__sort_iterator)
                command.execute()
                Sound().play("EnemyMove")
            except StopIteration:  # Ordenação finalizou...
                pass

""" Classes que interagem com o array """


from typing import Iterator, Optional
from abc import ABC, abstractmethod

from game.array.array import Array
from game.array.algorithm import Algorithm
from game.array.box import Box
from game.array.command import Command, SwapCommand
from game.manager.input import Input
from game.manager.sound import Sound


class Interactor(ABC):
    """ Interage com um array ao ser atualizado """

    @abstractmethod
    def set_array(self, array: Array) -> None:
        """ Associa um novo array ao interactor """

    @abstractmethod
    def update(self) -> None:
        """ Modifica o array, retornando um comando a ser executado """

    @abstractmethod
    def is_done(self) -> bool:
        """ Se o array já foi ordenado """

    @abstractmethod
    def has_moved(self) -> bool:
        """ Se realizou uma mudança do array """


class PlayerInteractor(Interactor):
    """ Classe responsável pelo controle do player """

    def __init__(self):
        self.__array: Optional[Array] = None
        self.__moved = False
        self.__done = False

    def __drop_box(self, dragging: Box) -> None:
        """ Solta a caixa """
        if self.__array is None:
            return
        for box in self.__array.boxes:
            if (
                box != dragging and
                abs(box.rect.centerx - dragging.rect.centerx) < 8 and
                abs(box.rect.centery - dragging.rect.centery) < 8
            ):
                SwapCommand(
                    self.__array,
                    self.__array.boxes.index(dragging),
                    self.__array.boxes.index(box)
                ).execute()
                self.__moved = True
                Sound().play("PlayerMove")
                if self.__array.is_sorted():
                    Sound().play("FinishedSorting")
                    self.__done = True
                break
        dragging.dragged = False

    def update(self) -> None:
        """ Atualiza conforme os inputs do mouse """
        self.__moved = False
        if self.__array is not None:
            box_under_cursor: Optional[Box] = None
            dragging: Optional[Box] = None

            for box in self.__array.boxes:
                if box.rect.collidepoint(*Input().mouse_pos):
                    box_under_cursor = box
                if box.dragged:
                    dragging = box
            if "MouseDrag" in Input().just_pressed and dragging is None:
                if box_under_cursor is not None:
                    dragging = box_under_cursor
                    dragging.dragged = True
            elif dragging is not None and not "MouseDrag" in Input().pressed:
                self.__drop_box(dragging)
            if dragging is not None:
                dragging.rect.center = Input().mouse_pos

    def has_moved(self) -> bool:
        return self.__moved

    def is_done(self) -> bool:
        return self.__done

    def set_array(self, array: Array) -> None:
        if not isinstance(array, Array):
            raise TypeError
        self.__array = array
        self.__done = False


class EnemyInteractor(Interactor):
    """ Classe responsável pela ordenação do array """

    def __init__(
        self,
        algorithm: Algorithm
    ):
        self.__algorithm = algorithm
        self.__done = False
        self.__moved = False
        self.__sort_iterator: Optional[Iterator[Command]] = None

    def set_array(self, array: Array) -> None:
        if not isinstance(array, Array):
            raise TypeError
        self.__sort_iterator = self.__algorithm.sort(array)
        self.__done = False

    def has_moved(self) -> bool:
        return self.__moved

    def is_done(self) -> bool:
        return self.__done

    def update(self) -> None:
        """ Checa se o array deve ser organizado """
        self.__moved = False
        if (
            not self.__done and
            self.__sort_iterator is not None
        ):
            try:
                next(self.__sort_iterator).execute()
                self.__moved = True
                Sound().play("EnemyMove")
            except StopIteration:  # Ordenação finalizou...
                self.__done = True
                Sound().play("FinishedSorting")

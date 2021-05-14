""" Módulos para as caixas de números """


from typing import List, Tuple

import pygame as pg

from game.array.box import Box, BoxFactory


class Array:
    """ Representação gráfica de um array """

    def __init__(self, box_factory: BoxFactory, y_pos: int = 0):
        self.__box_factory = box_factory
        self.__boxes: list[Box] = []
        self.__numbers: list[int] = []
        self.__sorted_numbers: list[int] = []
        self.__should_redraw = True
        self.__y_pos = y_pos

    @property
    def boxes(self):
        """ O array de caixas """
        return self.__boxes

    @property
    def numbers(self):
        """ O array numérico """
        return self.__numbers

    @numbers.setter
    def numbers(self, numbers: List[int]) -> None:
        """ Associa uma lista à esse array """
        self.__numbers = numbers
        self.__sorted_numbers = sorted(numbers)
        self.__boxes = list(map(self.__box_factory.create, numbers))
        self.__should_redraw = True

    @property
    def box_factory(self):
        """ O criador de caixas """
        return self.__box_factory

    def is_sorted(self) -> bool:
        """ Retorna se o array está ordenado """
        return self.__numbers == self.__sorted_numbers

    def __boxes_to_draw(self) -> List[Tuple[pg.Surface, pg.Rect]]:
        """
        Retorna uma lista de tuplas com a
        superfície e a posição das caixas
        """
        boxes: List[Tuple[pg.Surface, pg.Rect]] = []
        dragged = None
        for box in self.__boxes:
            if box.dragged:
                dragged = box
            else:
                boxes.append((box.surface, box.rect))
        if dragged is not None:
            boxes.append((dragged.surface, dragged.rect))
        return boxes

    def __update_positions(self, width: int):
        """ Corrige as posições das caixas conforme a largura e a altura """
        if len(self.__boxes) == 0:
            return
        spacing = (
            width - (len(self.__boxes) * self.__boxes[0].rect.width)
        ) // (len(self.__boxes) - 1)
        for index, box in enumerate(self.__boxes):
            if not box.dragged:
                box.rect.x = index * (box.rect.width + spacing)
                box.rect.y = self.__y_pos

    def draw(self, surface: pg.Surface):
        """ Desenha o array na altura especificada """
        if self.__should_redraw:
            self.__update_positions(surface.get_width())
        surface.blits(
            self.__boxes_to_draw(),  # type: ignore
            doreturn=False
        )

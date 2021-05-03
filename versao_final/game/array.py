""" Módulos para as caixas de números """


from typing import List, Tuple
import pygame as pg


class Box:
    """ A caixa que contém um número """

    def __init__(
        self,
        sprite: pg.Surface,
        font: pg.font.Font,
        number: int,
    ):
        self.__number = number
        self.__sprite = sprite
        self.__font = font
        self.__rect = pg.Rect(0, 0, 16, 16)
        self.__surface = pg.Surface((16, 16), pg.HWSURFACE | pg.SRCALPHA)
        self.__dragged = False

    @property
    def number(self):
        """ O número representado pela caixa """
        return self.__number

    @property
    def rect(self):
        """ A bounding box da caixa """
        return self.__rect

    @property
    def surface(self):
        """ A superfície da caixa """
        return self.__surface

    @property
    def dragged(self):
        """ Se a caixa está sendo arrastada """
        return self.__dragged

    @dragged.setter
    def dragged(self, dragged: bool):
        """ Altera o estado da caixa """
        self.__dragged = dragged

    def draw(self):
        """ Desenha a caixa, podendo receber opcionalmente uma cor """
        text = self.__font.render(str(self.__number), False, (0, 0, 0))
        self.__surface.blit(self.__sprite, (0, 0))
        self.__surface.blit(
            text,
            ((self.__rect.width - text.get_width()) / 2,
             (self.__rect.height - text.get_height()) / 2)
        )


class BoxFactory:
    """ Classe criadora de caixas """

    def __init__(self, sprite: pg.Surface, font: pg.font.Font):
        self.__sprite = sprite
        self.__font = font

    def create(self, number: int) -> Box:
        """ Cria uma caixa conforme determinado número """
        box = Box(self.__sprite, self.__font, number)
        box.draw()
        return box


class Array:
    """ Representação gráfica de um array """

    def __init__(self, box_factory: BoxFactory, y_pos: int = 0):
        self.__box_factory = box_factory
        self.__boxes: list[Box] = []
        self.__numbers: list[int] = []
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
        self.__boxes = list(map(self.__box_factory.create, numbers))
        self.__should_redraw = True

    @property
    def box_factory(self):
        """ O criador de caixas """
        return self.__box_factory

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

    def swap(self, origin: int, destination: int):
        """ Troca a posição de duas caixas no array """
        self.__should_redraw = True
        (self.__boxes[origin], self.__boxes[destination]) = (
            self.__boxes[destination], self.__boxes[origin]
        )
        (self.__numbers[origin], self.__numbers[destination]) = (
            self.__numbers[destination], self.__numbers[origin]
        )

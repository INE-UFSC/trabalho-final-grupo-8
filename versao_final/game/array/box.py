""" Módulo para as caixas de um array """


from typing import Optional, Tuple

import pygame as pg


class Box:
    """ A caixa que contém um número """

    def __init__(
        self,
        outline: pg.Surface,
        color: Tuple[int, int, int],
        font: pg.font.Font,
        number: int,
    ):
        self.__number = number
        self.__outline = outline
        self.__color = color
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

    def draw(self, color: Optional[Tuple[int, int, int]] = None):
        """ Desenha a caixa, podendo receber opcionalmente uma cor """
        text = self.__font.render(str(self.__number), False, (0, 0, 0))
        if color is None:
            color = self.__color
        pg.draw.rect(self.__surface, color, pg.Rect(
            1,
            1,
            (self.__rect.width - 2),
            (self.__rect.height - 2)
        ))
        self.__surface.blit(self.__outline, (0, 0))
        self.__surface.blit(
            text,
            ((self.__rect.width - text.get_width()) / 2,
             (self.__rect.height - text.get_height()) / 2)
        )


class BoxFactory:
    """ Classe criadora de caixas """

    def __init__(self, sprite: pg.Surface, color: Tuple[int, int, int], font: pg.font.Font):
        self.__color = color
        self.__sprite = sprite
        self.__font = font

    def create(self, number: int) -> Box:
        """ Cria uma caixa conforme determinado número """
        box = Box(self.__sprite, self.__color, self.__font, number)
        box.draw()
        return box

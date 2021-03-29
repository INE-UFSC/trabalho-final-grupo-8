""" Representa a caixa de cada número """


import pygame as pg


class NumberBox:
    """ Representa um número em uma caixa """

    def __init__(self, number, color: tuple[int, int, int] = (0, 0, 255)):
        self.__rect = pg.Rect(0, 0, 15, 15)
        self.__surface = pg.Surface((15, 15))
        self.__draw(number, color)

    @property
    def rect(self):
        """ A bounding box da caixa """
        return self.__rect

    @property
    def surface(self):
        """ A superfície da caixa """
        return self.__surface

    def __draw(self, number: int, color: tuple[int, int, int]):
        font = pg.font.SysFont('arial', 12)
        pg.draw.rect(self.__surface, color, pg.Rect(0, 0, 15, 15))
        self.__surface.blit(
            font.render(
                str(number),
                False,
                (255, 255, 255)
            ),
            (0, 0)
        )

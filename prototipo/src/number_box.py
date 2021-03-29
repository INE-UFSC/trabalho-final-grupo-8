""" Representa a caixa de cada número """


import pygame as pg


class NumberBox:
    """ Representa um número em uma caixa """

    def __init__(self, number):
        self.__number = number
        self.__rect = pg.Rect(0, 0, 15, 15)
        self.__surface = pg.Surface((15, 15))
        self.__draw()

    @property
    def rect(self):
        """ A bounding box da caixa """
        return self.__rect

    @property
    def number(self):
        """ O número da caixa """
        return self.__number

    @property
    def surface(self):
        """ A superfície da caixa """
        return self.__surface

    def __draw(self):
        font = pg.font.SysFont('arial', 12)
        pg.draw.rect(self.__surface, (255, 0, 0), pg.Rect(0, 0, 15, 15))
        self.__surface.blit(
            font.render(
                str(self.__number),
                False,
                (255, 255, 255)
            ),
            (0, 0)
        )

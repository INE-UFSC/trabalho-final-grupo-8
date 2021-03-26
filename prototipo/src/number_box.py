import pygame as pg


class NumberBox:
    def __init__(self, number):
        self.__number = number
        self.__surface = pg.Surface((15, 15))
        self.__draw()

    @property
    def surface(self):
        return self.__surface

    def __draw(self):
        font = pg.font.SysFont('arial', 12)
        pg.draw.rect(self.__surface, (255, 0, 0), pg.Rect(0, 0, 15, 15))
        self.__surface.blit(
            font.render(str(self.__number), False, (255, 255, 255)),
            (0, 0)
        )

""" Classe de gerenciamento do display """


from typing import Tuple

import pygame as pg


class Display():
    """ Inicializa a janela """

    def __init__(self, caption: str, resolution: Tuple[int, int], framerate: int = 60):
        pg.init()
        pg.font.init()

        pg.display.set_caption(caption)

        self.__framerate = framerate
        self.__clock = pg.time.Clock()
        self.__window = pg.display.set_mode(
            resolution,
            pg.RESIZABLE | pg.HWSURFACE | pg.DOUBLEBUF | pg.SCALED,
            32
        )
        self.tick()

    def tick(self) -> float:
        """ Atualiza o clock do jogo """
        return self.__clock.tick(self.__framerate) * 0.001

    def draw(self, surface: pg.Surface):
        """ Desenha uma superfície na janela """
        self.__window.fill((0, 0, 0))
        self.__window.blit(surface, (0, 0))
        pg.display.update()

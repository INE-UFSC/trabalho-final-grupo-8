""" Módulo de entrada do projeto """


import pygame as pg
from src.engine import DisplayManager, InputManager
from src.number_box import NumberBox


def main():
    """ Função principal do projeto """

    display = DisplayManager("Jogo dos Arrays", (200, 150))
    inputs = InputManager({
        pg.K_SPACE: 'interact',
        pg.MOUSEBUTTONDOWN: 'mouse'
    })

    surface = pg.Surface((200, 150))
    box = NumberBox(1)
    surface.blit(box.surface, (0, 0))

    while True:
        inputs.update()
        _ = display.tick()
        display.draw(surface)


if __name__ == '__main__':
    main()

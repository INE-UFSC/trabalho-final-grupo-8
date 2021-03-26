""" Módulo de entrada do projeto """


import pygame as pg
from src.engine import DisplayManager, InputManager


def main():
    """ Função principal do projeto """
    display = DisplayManager((200, 150), scale=2)
    inputs = InputManager({
        pg.K_SPACE: 'interact'
    })

    pg.font.init()

    font = pg.font.SysFont('liberation mono', 12)

    surface = pg.Surface((200, 150))

    array = [0, 9, 7, 5, 9, 2, 1, 4]

    for index, number in enumerate(array):
        pg.draw.rect(
            surface,
            (255, 0, 0),
            pg.Rect(index * 18, 70, 15, 15)
        )
        surface.blit(
            font.render(str(number), False, (255, 255, 255)),
            (index * 18 + 5, 70)
        )

    while True:
        inputs.update()
        _ = display.tick()

        display.draw(surface)


if __name__ == '__main__':
    main()

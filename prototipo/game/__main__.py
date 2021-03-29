""" Módulo de entrada do projeto """


import pygame as pg
from game.engine import DisplayManager, InputManager
from game.number_array import NumberArray


def main():
    """ Função principal do projeto """

    display = DisplayManager("Jogo dos Arrays", (200, 150))
    inputs = InputManager({
        pg.K_SPACE: 'interact',
        pg.MOUSEBUTTONDOWN: 'mouse_click'
    })

    surface = pg.Surface((200, 150))
    array = NumberArray(range(10))

    while True:
        inputs.update()
        _ = display.tick()

        surface.fill((0, 0, 0))

        array.handle_mouse(
            inputs.mouse_pos,
            "mouse_click" in inputs.pressed,
            "mouse_click" in inputs.just_pressed
        )

        array.draw(surface, 130, margin=5)
        display.draw(surface)


if __name__ == '__main__':
    main()

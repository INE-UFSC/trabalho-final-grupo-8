""" Módulo de entrada do projeto """


import pygame as pg
from game.engine import DisplayManager, InputManager
from game.number_array import InteractableNumberArray, NumberArray


def main():
    """ Função principal do projeto """

    display = DisplayManager("Jogo dos Arrays", (200, 150))
    inputs = InputManager({
        pg.K_SPACE: 'interact',
        pg.MOUSEBUTTONDOWN: 'mouse_click'
    })

    surface = pg.Surface((200, 150))

    player_array = InteractableNumberArray(range(10), (0, 155, 0))
    enemy_array = NumberArray(range(10), (255, 0, 0))

    while True:
        inputs.update()
        _ = display.tick()

        surface.fill((0, 0, 0))

        player_array.handle_mouse(
            inputs.mouse_pos,
            "mouse_click" in inputs.pressed,
            "mouse_click" in inputs.just_pressed
        )

        enemy_array.draw(surface, 5, margin=5)
        player_array.draw(surface, 130, margin=5)

        display.draw(surface)


if __name__ == '__main__':
    main()

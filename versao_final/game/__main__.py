""" Módulo de entrada do projeto """


import random
import pygame as pg
from game.engine import DisplayManager, InputManager
from game.numbers import InteractableNumberArray, NumberArray
from game.enemy import Enemy
from game.algorithm import Quicksort
from game.ui import UI


def main():
    """ Função principal do projeto """

    display = DisplayManager("Sort it!", (200, 150))
    inputs = InputManager({
        'interact': 'space',
        'click': 'mouse_click',
        'drag': 'mouse_drag'
    })

    surface = pg.Surface((200, 150))
    gui = UI((200, 150))

    array = [random.randint(0, 100) for _ in range(10)]
    player_array = InteractableNumberArray(array, (0, 155, 0))
    enemy_algorithm = Quicksort()
    enemy_array = NumberArray([], (255, 0, 0))
    enemy = Enemy(enemy_algorithm, enemy_array, 1.0)
    enemy.set_array(array)

    while True:
        inputs.update([gui.handle_event])
        delta_time = display.tick()
        surface.fill((0, 0, 0))

        gui.update(delta_time)

        if gui.in_game():
            enemy.update(delta_time)
            player_array.handle_mouse(inputs)
            enemy_array.draw(surface, 5, margin=5)
            player_array.draw(surface, 130, margin=5)

        gui.draw(surface)
        display.draw(surface)


if __name__ == '__main__':
    main()

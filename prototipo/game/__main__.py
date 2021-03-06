""" Módulo de entrada do projeto """


import random
import pygame as pg
from game.engine import DisplayManager, InputManager
from game.number_array import InteractableNumberArray, NumberArray
from game.enemy import Enemy
from game.algorithm import Quicksort


def main():
    """ Função principal do projeto """

    display = DisplayManager("Jogo dos Arrays", (200, 150))
    inputs = InputManager({
        'interact': 'space',
        'click': 'mouse_click',
        'drag': 'mouse_drag'
    })

    surface = pg.Surface((200, 150))

    array = [random.randint(0, 100) for _ in range(10)]
    player_array = InteractableNumberArray(array, (0, 155, 0))
    enemy_algorithm = Quicksort()
    enemy_array = NumberArray([], (255, 0, 0))
    enemy = Enemy(enemy_algorithm, enemy_array, 1.0)
    enemy.set_array(array)

    while True:
        inputs.update()
        delta_time = display.tick()

        surface.fill((0, 0, 0))

        enemy.update(delta_time)
        player_array.handle_mouse(inputs)
        enemy_array.draw(surface, 5, margin=5)
        player_array.draw(surface, 130, margin=5)

        display.draw(surface)


if __name__ == '__main__':
    main()

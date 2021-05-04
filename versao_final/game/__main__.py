""" Módulo de entrada do projeto """


import pygame as pg
from game.algorithm import RecursiveQuicksort, lomuto_partitioner
from game.array import BoxFactory, Array
from game.enemy import EnemyBuilder, TimedBehaviour
from game.engine import DisplayManager, InputManager
from game.player import Player
from game.sound import SoundManager
from game.ui import UI
from game.utils import Timer


SCREEN_SIZE = (400, 300)


def main():
    """ Função principal do projeto """

    display = DisplayManager("Sort it!", SCREEN_SIZE)
    audio = SoundManager('./assets')
    audio.load_sound('move', 'move1.wav')
    inputs = InputManager({
        'interact': 'space',
        'click': 'mouse_click',
        'drag': 'mouse_drag'
    })

    surface = pg.Surface(SCREEN_SIZE)
    gui = UI(SCREEN_SIZE)

    blue_box = pg.image.load('./assets/BlueBox.png').convert_alpha()
    red_box = pg.image.load('./assets/RedBox.png').convert_alpha()
    font = pg.font.Font('./assets/OpenSansPXBold.ttf', 16)

    enemy_array = Array(BoxFactory(red_box, font), y_pos=0)
    player_array = Array(BoxFactory(blue_box, font), y_pos=(SCREEN_SIZE[1]-16))

    enemy_builder = EnemyBuilder()
    enemy_timer = Timer(1.0, auto_start=True, one_shot=False)
    enemy_builder.set_behaviour(TimedBehaviour(enemy_timer))
    enemy_builder.set_algorithm(
        RecursiveQuicksort(lomuto_partitioner, enemy_array)
    )

    enemy = enemy_builder.get_result()

    player_array.numbers = [15, 0, 10, 8, 2, 1, 5, 7]
    enemy_array.numbers = [15, 0, 10, 8, 2, 1, 5, 7]

    player = Player(player_array, inputs)

    while True:
        inputs.update([gui.handle_event])
        delta_time = display.tick()
        enemy_timer.update(delta_time)
        surface.fill((50, 50, 50))

        gui.update(delta_time)

        if gui.in_game():
            player.update()
            enemy.update()
            player_array.draw(surface)
            enemy_array.draw(surface)

        gui.draw(surface)
        display.draw(surface)


if __name__ == '__main__':
    main()

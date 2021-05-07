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
    inputs = InputManager({
        'interact': 'space',
        'click': 'mouse_click',
        'drag': 'mouse_drag'
    })

    audio = SoundManager('./assets')
    audio.load_sound('move', 'move1.wav')
    audio.load_sound('finished', 'finished.wav')

    surface = pg.Surface(SCREEN_SIZE)
    gui = UI(SCREEN_SIZE)

    box_outline = pg.image.load('./assets/BoxOutline.png').convert_alpha()
    font = pg.font.Font('./assets/OpenSansPXBold.ttf', 16)

    enemy_array = Array(
        BoxFactory(box_outline, (255, 0, 77), font),
        y_pos=0
    )
    player_array = Array(
        BoxFactory(box_outline, (41, 173, 255), font),
        y_pos=(SCREEN_SIZE[1]-16)
    )

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
        gui.update(delta_time)

        if gui.in_game():
            player.update()
            enemy.update()
            player_array.draw(surface)
            enemy_array.draw(surface)

        surface.fill((50, 50, 50))
        gui.draw(surface)
        display.draw(surface)


if __name__ == '__main__':
    main()

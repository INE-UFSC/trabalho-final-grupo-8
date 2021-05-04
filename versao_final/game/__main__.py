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


def main():
    """ Função principal do projeto """

    display = DisplayManager("Sort it!", (200, 150))
    audio = SoundManager('./assets')
    audio.load_sound('move', 'move1.wav')
    inputs = InputManager({
        'interact': 'space',
        'click': 'mouse_click',
        'drag': 'mouse_drag'
    })

    surface = pg.Surface((200, 150))
    gui = UI((200, 150))

    blue_box = pg.image.load('./assets/BlueBox.png').convert_alpha()
    red_box = pg.image.load('./assets/RedBox.png').convert_alpha()
    font = pg.font.Font('./assets/OpenSansPXBold.ttf', 16)

    enemy_builder = EnemyBuilder()
    enemy_array = Array(BoxFactory(red_box, font), y_pos=0)
    enemy_timer = Timer(2.0, auto_start=True, one_shot=False)
    enemy_builder.set_behaviour(TimedBehaviour(enemy_timer))
    enemy_builder.set_algorithm(
        RecursiveQuicksort(lomuto_partitioner, enemy_array)
    )

    enemy = enemy_builder.get_result()

    player_array = Array(BoxFactory(blue_box, font), y_pos=134)

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

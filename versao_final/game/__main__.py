""" Módulo de entrada do projeto """


import pygame as pg
from game.player import PlayerInteractor
from game.match import GameEntity, Data, Match
from game.algorithm import RecursiveQuicksort, lomuto_partitioner
from game.array import BoxFactory, Array
from game.enemy import EnemyInteractor, TimedBehaviour
from game.engine import DisplayManager, InputManager
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

    player_array = Array(
        BoxFactory(box_outline, (41, 173, 255), font),
        y_pos=(SCREEN_SIZE[1]-16)
    )
    enemy_array = Array(
        BoxFactory(box_outline, (255, 0, 77), font),
        y_pos=0
    )

    player_array.numbers = [15, 0, 10, 8, 2, 1, 5, 7]
    enemy_array.numbers = [15, 0, 10, 8, 2, 1, 5, 7]

    enemy_timer = Timer(1.0, auto_start=True, one_shot=True)

    player_interactor = PlayerInteractor(inputs)
    enemy_interactor = EnemyInteractor(
        RecursiveQuicksort(lomuto_partitioner),
        TimedBehaviour(enemy_timer)
    )

    player_interactor.set_array(player_array)
    enemy_interactor.set_array(enemy_array)

    player = GameEntity(
        player_array,
        player_interactor,
        Data("Jogador")
    )

    enemy = GameEntity(
        enemy_array,
        enemy_interactor,
        Data("Inimigo")
    )

    match = Match(player, enemy)

    while True:
        inputs.update([gui.handle_event])
        delta_time = display.tick()
        enemy_timer.update(delta_time)
        gui.update(delta_time)
        surface.fill((50, 50, 50))

        if gui.in_game():
            match.update()
            match.draw(surface)

        gui.draw(surface)
        display.draw(surface)


if __name__ == '__main__':
    main()

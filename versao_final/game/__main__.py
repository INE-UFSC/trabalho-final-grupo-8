""" Módulo de entrada do projeto """


import pygame as pg

from game.constants import MOUSE_DRAG, SCREEN_SIZE
from game.manager.input import Input
from game.manager.display import Display
from game.manager.sound import Sound
from game.ui.ui import UI
from game.utils import TimerList
from game.game.state import GameState
from game.array.box import BoxFactory
from game.array.array import Array
from game.entity.interactor import PlayerInteractor
from game.game.match import MatchFactory


def main():
    """ Função principal do projeto """

    # Classes de setup
    display = Display("Sort it!", SCREEN_SIZE)
    Sound('./assets', {
        'PlayerMove': 'move1.wav',
        'EnemyMove': 'move2.wav',
        'FinishedSorting': 'finished.wav'
    })
    inputs = Input({
        pg.MOUSEBUTTONDOWN: 'MouseClick',
        MOUSE_DRAG: 'MouseDrag'
    })
    timers = TimerList()

    # Imagens
    box_outline = pg.image.load('./assets/BoxOutline.png').convert_alpha()
    font = pg.font.Font('./assets/OpenSansPXBold.ttf', 16)
    background = pg.image.load('./assets/background.png')

    # Estado do jogo
    match_factory = MatchFactory()
    match_factory.player.set_interactor(PlayerInteractor())
    match_factory.player.set_array(Array(
        BoxFactory(box_outline, (41, 173, 255), font),
        y_pos=(SCREEN_SIZE[1]-16-48)
    ))
    match_factory.enemy.set_array(Array(
        BoxFactory(box_outline, (255, 0, 77), font),
        y_pos=(48)
    ))
    state = GameState(match_factory)

    # Superfície temporária de desenho
    surface = pg.Surface(SCREEN_SIZE)

    # Interface gráfica
    gui = UI(state, SCREEN_SIZE)

    while True:
        inputs.update([gui.handle_event])
        delta_time = display.tick()
        timers.update(delta_time)
        gui.update(delta_time)

        if gui.in_game():
            surface.blit(background, (0, 0))
        else:
            surface.fill((29, 43, 83))

        gui.draw(surface)

        if gui.in_game():
            state.draw(surface)

        display.draw(surface)


if __name__ == '__main__':
    main()

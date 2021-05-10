""" Módulo de entrada do projeto """


from game.state import GameState
import pygame as pg
from game.player import PlayerInteractor
from game.match import MatchFactory
from game.array import BoxFactory, Array
from game.engine import DisplayManager, InputManager
from game.sound import SoundManager
from game.ui import UI
from game.utils import TimerList

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

    box_outline = pg.image.load('./assets/BoxOutline.png').convert_alpha()
    font = pg.font.Font('./assets/OpenSansPXBold.ttf', 16)

    match_factory = MatchFactory()
    match_factory.player.set_interactor(PlayerInteractor(inputs))
    match_factory.player.set_array(Array(
        BoxFactory(box_outline, (41, 173, 255), font),
        y_pos=(SCREEN_SIZE[1]-16)
    ))
    match_factory.enemy.set_array(Array(
        BoxFactory(box_outline, (255, 0, 77), font),
        y_pos=0
    ))

    state = GameState(match_factory)

    timers = TimerList()

    surface = pg.Surface(SCREEN_SIZE)
    gui = UI(state, SCREEN_SIZE)

    while True:
        inputs.update([gui.handle_event])
        delta_time = display.tick()
        timers.update(delta_time)
        gui.update(delta_time)
        surface.fill((50, 50, 50))

        if gui.in_game():
            state.draw(surface)

        gui.draw(surface)
        display.draw(surface)


if __name__ == '__main__':
    main()

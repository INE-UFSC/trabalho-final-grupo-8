""" Módulo de entrada do projeto """


import pygame as pg
from src.engine import DisplayManager, InputManager
from src.number_box import NumberBox


def main():
    """ Função principal do projeto """

    display = DisplayManager("Jogo dos Arrays", (200, 150))
    inputs = InputManager({
        pg.K_SPACE: 'interact',
        pg.MOUSEBUTTONDOWN: 'mouse_click'
    })

    surface = pg.Surface((200, 150))
    boxes = [NumberBox(number) for number in range(10)]

    dragging = None

    while True:
        inputs.update()
        _ = display.tick()

        surface.fill((0, 0, 0))

        box_under_cursor = None
        for box in boxes:
            if box.rect.collidepoint(*inputs.mouse_pos):
                box_under_cursor = box
            surface.blit(box.surface, box.rect.topleft)

        if "mouse_click" in inputs.just_pressed and dragging is None:
            boxes.append(boxes.pop(boxes.index(box_under_cursor)))
            dragging = box_under_cursor
        elif dragging is not None and "mouse_click" not in inputs.pressed:
            dragging = None

        if dragging is not None:
            dragging.rect.center = inputs.mouse_pos

        display.draw(surface)


if __name__ == '__main__':
    main()

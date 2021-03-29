""" Representação gráfica de um array """


from typing import Optional
import pygame as pg
from game.number_box import NumberBox


class NumberArray:
    """ Array representado por caixas de números """

    def __init__(self, array: list):
        self.__array = list(map(NumberBox, array))
        self.__dragging: Optional[NumberBox] = None
        self.__order_changed = True

    def __get_offset(self, full_width: int):
        return (
            full_width - len(self.__array) * self.__array[0].rect.width
        ) / (len(self.__array) - 1)

    def __drop_box(self):
        for box in self.__array:
            if (
                box != self.__dragging and
                abs(box.rect.centerx - self.__dragging.rect.centerx) < 5 and
                abs(box.rect.centery - self.__dragging.rect.centery) < 5
            ):
                self.switch_positions(
                    self.__array.index(self.__dragging),
                    self.__array.index(box)
                )
                break
        self.__order_changed = True
        self.__dragging = None

    def __update_positions(self, total_width: int, y_pos: int, margin: int):
        offset = self.__get_offset(total_width - 2 * margin)
        for index, box in enumerate(self.__array):
            box.rect.x = margin + index * (box.rect.width + offset)
            box.rect.y = y_pos

    def switch_positions(self, origin: int, destination: int):
        """ Troca a posição de duas caixas no array """
        origin_box = self.__array[origin]
        destination_box = self.__array[destination]
        self.__array[origin] = destination_box
        self.__array[destination] = origin_box

    def handle_mouse(self, mouse_pos: tuple, mouse_pressed: bool, mouse_just_pressed: bool):
        """ Atualiza conforme os inputs do mouse """
        box_under_cursor = None
        for box in self.__array:
            if box.rect.collidepoint(*mouse_pos):
                box_under_cursor = box

        if mouse_just_pressed and self.__dragging is None:
            if box_under_cursor is not None:
                self.__dragging = box_under_cursor

        elif self.__dragging is not None and not mouse_pressed:
            self.__drop_box()

        if self.__dragging is not None:
            self.__dragging.rect.center = mouse_pos

    def draw(self, surface: pg.Surface, y_pos: int, margin: int = 0):
        """ Desenha o array em uma superfície com base na altura """
        if self.__order_changed:
            self.__update_positions(surface.get_width(), y_pos, margin)
            self.__order_changed = False

        boxes_to_draw = [
            (box.surface, box.rect.topleft) for box in self.__array if box != self.__dragging
        ]
        if self.__dragging is not None:
            boxes_to_draw.append(
                (self.__dragging.surface, self.__dragging.rect.topleft)
            )

        surface.blits(boxes_to_draw, doreturn=False)  # type: ignore

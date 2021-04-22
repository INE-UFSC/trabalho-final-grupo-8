""" Representação gráfica de um array """


from typing import List, Optional, Tuple
import pygame as pg
from game.engine import InputManager


class NumberBox:
    """ Representa um número em uma caixa """

    def __init__(self, number, color: Tuple[int, int, int] = (0, 0, 255)):
        self.__rect = pg.Rect(0, 0, 15, 15)
        self.__surface = pg.Surface((15, 15))
        self.__draw(number, color)

    @property
    def rect(self):
        """ A bounding box da caixa """
        return self.__rect

    @property
    def surface(self):
        """ A superfície da caixa """
        return self.__surface

    def __draw(self, number: int, color: Tuple[int, int, int]):
        font = pg.font.SysFont('notosans', 8)
        text = font.render(str(number), False, (255, 255, 255))
        pg.draw.rect(self.__surface, color, pg.Rect(0, 0, 15, 15))
        self.__surface.blit(
            text,
            ((15 - text.get_width()) / 2, (15 - text.get_height()) / 2)
        )


class NumberArray:
    """ Classe base para o array """

    def __init__(self, array: List[int], color: Tuple[int, int, int] = (0, 0, 255)):
        self.__color = color
        self.__array = list(map(lambda a: NumberBox(a, color), array))
        self.__order_changed = True

    @property
    def array(self):
        """ O array de caixas """
        return self.__array

    @array.setter
    def array(self, array: List[int]):
        self.__array = list(map(lambda a: NumberBox(a, self.__color), array))
        self.__order_changed = True

    @property
    def order_changed(self):
        """ Se houve alteração na ordem das caixas """
        return self.__order_changed

    @order_changed.setter
    def order_changed(self, order_changed: bool):
        """ Atualiza o estado de alteração """
        self.__order_changed = order_changed

    @property
    def boxes_to_draw(self):
        """ A lista de boxes no padrão recebido pela função blits """
        return [(box.surface, box.rect.topleft) for box in self.__array]

    def __get_offset(self, full_width: int):
        """ O intervalo de espaçamento entre as caixas """
        return (
            full_width - len(self.__array) * self.__array[0].rect.width
        ) / (len(self.__array) - 1)

    def update_positions(self, total_width: int, y_pos: int, margin: int):
        """ Atualiza a posição de cada caixa """
        offset = self.__get_offset(total_width - 2 * margin)
        for index, box in enumerate(self.__array):
            box.rect.x = margin + index * (box.rect.width + offset)
            box.rect.y = y_pos

    def switch_positions(self, origin: int, destination: int):
        """ Troca a posição de duas caixas no array """
        self.order_changed = True
        origin_box = self.__array[origin]
        destination_box = self.__array[destination]
        self.__array[origin] = destination_box
        self.__array[destination] = origin_box

    def draw(self, surface: pg.Surface, y_pos: int, margin: int = 0):
        """ Desenha o array em uma superfície com base na altura """
        if self.__order_changed:
            self.update_positions(surface.get_width(), y_pos, margin)
            self.__order_changed = False
        surface.blits(self.boxes_to_draw, doreturn=False)  # type: ignore


class InteractableNumberArray(NumberArray):
    """ Array representado por caixas de números, interagível pelo mouse """

    def __init__(self, array: List[int], color: Tuple[int, int, int] = (0, 0, 255)):
        super().__init__(array, color)
        self.__dragging: Optional[NumberBox] = None

    @property
    def boxes_to_draw(self):
        """ Lista de caixas, com a caixa sendo carregada a última a ser desenhada """
        boxes_to_draw = [
            (box.surface, box.rect.topleft) for box in self.array if box != self.__dragging
        ]
        if self.__dragging is not None:
            boxes_to_draw.append(
                (self.__dragging.surface, self.__dragging.rect.topleft)
            )
        return boxes_to_draw

    def __drop_box(self):
        """ Solta a caixa, checando se a posição deve ser alterada """
        self.order_changed = True
        for box in self.array:
            if (
                box != self.__dragging and
                abs(box.rect.centerx - self.__dragging.rect.centerx) < 8 and
                abs(box.rect.centery - self.__dragging.rect.centery) < 8
            ):
                self.switch_positions(
                    self.array.index(self.__dragging),
                    self.array.index(box)
                )
                break
        self.__dragging = None

    def handle_mouse(self, inputs: InputManager):
        """ Atualiza conforme os inputs do mouse """
        box_under_cursor = None
        for box in self.array:
            if box.rect.collidepoint(*inputs.mouse_pos):
                box_under_cursor = box

        if "drag" in inputs.just_pressed and self.__dragging is None:
            if box_under_cursor is not None:
                self.__dragging = box_under_cursor

        elif self.__dragging is not None and not "drag" in inputs.pressed:
            self.__drop_box()

        if self.__dragging is not None:
            self.__dragging.rect.center = inputs.mouse_pos

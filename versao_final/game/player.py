""" Módulo para a implementação do player """


from game.array import Array, Box
from game.engine import InputManager


class Player:
    """ Classe responsável pelo controle do player """

    def __init__(self, array: Array, inputs: InputManager):
        self.__array = array
        self.__inputs = inputs

    def __drop_box(self, dragging: Box):
        """ Solta a caixa """
        for box in self.__array.numbers:
            if (
                box != dragging and
                abs(box.rect.centerx - dragging.rect.centerx) < 8 and
                abs(box.rect.centery - dragging.rect.centery) < 8
            ):
                self.__array.swap(
                    self.__array.numbers.index(dragging),
                    self.__array.numbers.index(box)
                )
                break
        dragging.dragged = False

    def __handle_mouse(self):
        """ Atualiza conforme os inputs do mouse """
        box_under_cursor = None
        dragging = None

        for box in self.__array.numbers:
            if box.rect.collidepoint(*self.__inputs.mouse_pos):
                box_under_cursor = box
            if box.dragged:
                dragging = box

        if "drag" in self.__inputs.just_pressed and dragging is None:
            if box_under_cursor is not None:
                dragging = box_under_cursor
                dragging.dragged = True

        elif dragging is not None and not "drag" in self.__inputs.pressed:
            self.__drop_box(dragging)

        if dragging is not None:
            dragging.rect.center = self.__inputs.mouse_pos

    def update(self):
        """ Atualiza a interação do player com o seu array """
        self.__handle_mouse()

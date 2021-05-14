""" Módulo de exceções """


class AttributesNotSetException(Exception):
    """ Lançada em builder quando os atributos não foram totalemente definidos """

    def __init__(self):
        super().__init__("Atributos não definidos no Builder")

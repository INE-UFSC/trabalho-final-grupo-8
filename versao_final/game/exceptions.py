""" Módulo de exceções """


class AttributesNotSetException(Exception):
    """ Lançada quando os atributos não foram totalmente definidos """

    def __init__(self):
        super().__init__("Atributos não definidos")

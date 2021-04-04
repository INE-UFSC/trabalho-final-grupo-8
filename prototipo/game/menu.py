import pygame
import pygame_menu


class Menu:
    def __init__(self):
        pass

    def menu(self):
        pygame.init()
        surface = pygame.display.set_mode((1280, 1024))     # Mexer na resolução.

        mytheme = pygame_menu.Theme(background_color=(29, 43, 82),
                                    title_background_color=(255, 255, 255),
                                    title_font_shadow=True,
                                    title_font=pygame_menu.font.FONT_8BIT,
                                    title_font_color=(29, 43, 82),
                                    widget_padding=25)

        menu = pygame_menu.Menu("Jogo da Ordenacao", 800, 700, theme=mytheme)   # Mudar o nome do jogo? UTF-8

        self.__name = menu.add.text_input('Name :', font_color=(0, 0, 0))     # adicionar o player ao banco de dados.
        self.__difficulty = menu.add.selector("dificuldade: ", [('Dificil', 3), ('Medio', 2), ('Facil', 1)], font_color=(0, 0, 0))
        self.__mododeJogo = menu.add.selector("Modo de Jogo: ", [('tempo', 2), ('Movimentos', 1)], font_color=(0, 0, 0))
        self.__ArrayParaOrdenar = menu.add.text_input('Array para ser ordenado :', font_color=(0, 0, 0))    # formatar.
        button1 = menu.add.button('Play', background_color=(40, 176, 255), font_color=(0, 0, 0))    # fazer o play funcionar.
        button2 = menu.add.button('Quit', pygame_menu.events.EXIT, background_color=(255, 2, 76), font_color=(0, 0, 0))

        button2.set_float(True)
        button2.translate(100, 0)
        button1.translate(-100, 0)
        menu.mainloop(surface)

    @property
    def Modo(self):
        return self.__mododeJogo

    @property
    def ArrayParaOrdenar(self):
        return self.__ArrayParaOrdenar

    @property
    def Difficulty(self):
        return self.__difficulty

    @property
    def Name(self):
        return self.__name


if __name__ == '__main__':
    Menu().menu()

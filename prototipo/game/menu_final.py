import pygame
import pygame_menu
from menu import Menu
from placar import Placar


class Menu_final:
    def __init__(self):
        pass

    def menu_final(self):
        pygame.init()

        surface = pygame.display.set_mode((1000, 800))     # Mexer na resolução.

        x = "derrota"
        txt = cor = menu = ""
        if x is "vitoria":
            mytheme = pygame_menu.Theme(background_color=(29, 43, 82),
                                        title_background_color=(255, 255, 255),
                                        title_font_shadow=True,
                                        title_font=pygame_menu.font.FONT_8BIT,
                                        title_font_color=(40, 40, 255),
                                        widget_padding=25)
            menu = pygame_menu.Menu("VITORIA", 800, 700, theme=mytheme)
            txt = "VOCE VENCEU!!!"
            cor = (40, 40, 255)

        elif x is "derrota":
            mytheme = pygame_menu.Theme(background_color=(29, 43, 82),
                                        title_background_color=(255, 255, 255),
                                        title_font_shadow=True,
                                        title_font=pygame_menu.font.FONT_8BIT,
                                        title_font_color=(255, 40, 40),
                                        widget_padding=25)
            menu = pygame_menu.Menu("DERROTA", 800, 700, theme=mytheme)
            txt = "VOCE PERDEU!!!"
            cor = (255, 40, 40)

        menu.add_label(txt, font_size=75, font_color=cor, font_name=pygame_menu.font.FONT_NEVIS, font_shadow=True)

        button1 = menu.add.button('Menu', Menu.menu(), pygame_menu.events.EXIT, background_color=(50, 170, 70), # Menu.menu() nao funciona
                                      font_color=(0, 0, 0))

        button2 = menu.add.button('Placar', Placar.exibirPlacar(), background_color=(50, 170, 70),
                                      font_color=(0, 0, 0))     # Placar nao existe ainda.
        button2.set_float(True)
        button2.translate(100, 0)
        button1.translate(-100, 0)
        menu.mainloop(surface)


if __name__ == '__main__':
    Menu_final().menu_final()

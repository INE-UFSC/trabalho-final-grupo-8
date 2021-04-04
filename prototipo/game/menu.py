import pygame
import pygame_menu


def menu():
    pygame.init()
    surface = pygame.display.set_mode((1280, 1024)) # Mexer na resolução.

    mytheme = pygame_menu.Theme(background_color=(29, 43, 82),
                                title_background_color=(255, 255, 255),
                                title_font_shadow=True,
                                title_font=pygame_menu.font.FONT_8BIT,
                                title_font_color=(29, 43, 82),
                                widget_padding=25)

    menu = pygame_menu.Menu("Jogo da Ordenacao", 800, 700, theme=mytheme)   # Mudar o nome do jogo.

    menu.add.text_input('Name :', font_color=(0, 0, 0))     # adicionar o player ao banco de dados.
    menu.add.selector("dificuldade: ", [('Dificil', 3), ('Medio', 2), ('Facil', 1)], font_color=(0, 0, 0))
    menu.add.selector("Modo de Jogo: ", [('tempo', 2), ('Movimentos', 1)], font_color=(0, 0, 0))
    # menu.add.text_input('Array para ser ordenado :', font_color=(0, 0, 0))  definir o array
    button1 = menu.add.button('Play', background_color=(40, 176, 255), font_color=(0, 0, 0))    # fazer o play funcionar.
    button2 = menu.add.button('Quit', pygame_menu.events.EXIT, background_color=(255, 2, 76), font_color=(0, 0, 0))

    button2.set_float(True)
    button2.translate(100, 0)
    button1.translate(-100, 0)
    menu.mainloop(surface)


if __name__ == '__main__':
    menu()

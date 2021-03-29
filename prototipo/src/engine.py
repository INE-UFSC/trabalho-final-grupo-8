""" Classes de gerenciamento """


import sys
import pygame as pg


class DisplayManager:
    """ Inicializa a janela """

    def __init__(self, caption: str, resolution: tuple[int, int], framerate=60):
        pg.init()
        pg.font.init()

        pg.display.set_caption(caption)

        self.__framerate = framerate
        self.__clock = pg.time.Clock()
        self.__window = pg.display.set_mode(
            resolution,
            pg.RESIZABLE | pg.HWSURFACE | pg.DOUBLEBUF | pg.SCALED,
            32
        )
        self.tick()

    def tick(self) -> float:
        """ Atualiza o clock do jogo """
        return self.__clock.tick(self.__framerate) * 0.001 * self.__framerate

    def draw(self, surface: pg.Surface):
        """ Desenha uma superfície na janela """
        self.__window.fill((0, 0, 0))
        self.__window.blit(surface, (0, 0))
        pg.display.update()


class InputManager:
    """ Gerencia as teclas pressionadas """

    def __init__(self, mappings: dict[int, str]):
        self.__mappings = mappings
        self.__pressed: set[str] = set()
        self.__just_pressed: set[str] = set()
        self.__mouse_pos = (0, 0)

    @property
    def pressed(self):
        """ As teclas pressionadas """
        return self.__pressed

    @property
    def just_pressed(self):
        """ As teclas pressionadas no frame atual """
        return self.__just_pressed

    @property
    def mouse_pos(self):
        """ A posição do mouse """
        return self.__mouse_pos

    def update(self):
        """ Atualiza as teclas """
        self.__just_pressed.clear()
        self.__mouse_pos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type in (pg.KEYDOWN, pg.KEYUP) and event.key in self.__mappings:
                action_name = self.__mappings[event.key]
                if event.type == pg.KEYDOWN:
                    self.__pressed.add(action_name)
                    self.__just_pressed.add(action_name)
                elif action_name in self.__pressed:
                    self.__pressed.remove(action_name)
            elif (
                event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP) and
                pg.MOUSEBUTTONDOWN in self.__mappings
            ):
                action_name = self.__mappings[pg.MOUSEBUTTONDOWN]
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.__pressed.add(action_name)
                    self.__just_pressed.add(action_name)
                elif event.type == pg.MOUSEBUTTONUP:
                    self.__pressed.remove(action_name)

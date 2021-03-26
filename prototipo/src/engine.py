""" Classes de gerenciamento """


import sys
import pygame as pg
import tkinter as tk


class DisplayManager:
    """ Inicializa a janela """

    def __init__(self, resolution: tuple[int, int], scale: int = 1):
        pg.init()
        pg.display.set_caption("Jogo dos Arrays")

        self.__framerate = 60
        self.__clock = pg.time.Clock()
        self.__window = pg.display.set_mode(
            (resolution[0] * scale, resolution[1] * scale), 0, 32
        )
        print(self.__get_resolution())
        self.tick()
        
    def __get_resolution(self):
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        return (screen_width, screen_height)

    def tick(self) -> float:
        """ Atualiza o clock do jogo """
        return self.__clock.tick(self.__framerate) * 0.001 * self.__framerate

    def draw(self, surface: pg.Surface):
        """ Desenha uma superfície na janela """
        self.__window.fill((0, 0, 0))
        self.__window.blit(
            pg.transform.scale(surface, self.__window.get_size()), (0, 0)
        )
        pg.display.update()


class InputManager:
    """ Gerencia as teclas pressionadas """

    def __init__(self, mappings: dict[int, str]):
        self.__mappings = mappings
        self.__pressed: set[str] = set()
        self.__just_pressed: set[str] = set()

    @property
    def pressed(self):
        """ As teclas pressionadas """
        return self.__pressed

    @property
    def just_pressed(self):
        """ As teclas pressionadas no frame atual """
        return self.__just_pressed

    def update(self):
        """ Atualiza as teclas """
        self.__just_pressed.clear()

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

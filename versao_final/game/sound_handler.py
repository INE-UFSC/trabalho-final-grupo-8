import pygame as pg
import random
from os import listdir
from os.path import isfile, join, splitext

#Essa classe um factory de efeitos sonoros que também é um singleton, porque o mixer de sons só precisa ser iniciado uma vez

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class SoundHandler():
    def __init__(self):
        self.__path = "./assets/"
        pg.mixer.init()
        
    def move_sfx(self):
        audios = ["move1.wav", "move2.wav"]
        pg.mixer.Sound(self.__path + random.choice(audios)).play()
    
    def array_completo(self):
        pg.mixer.Sound(self.__path + "Array Completo.wav")

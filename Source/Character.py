import sys as SYS
import pygame as PY
import pygame.display as PD
import pygame.image as PI
import pygame.event as PE
import pygame.sprite as PS
from abc import ABCMeta, abstractmethod


#  abstract Character class
class BaseClass(PS.Sprite):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

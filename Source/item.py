import os as OS
import sys as SYS
import pygame as PY
import pygame.display as PD
import pygame.event as PE
import pygame.image as PI
import pygame.sprite as PS
import Setup
from Character import BaseClass
from smooth import Entity
Dir = OS.getcwd()
PROJECTILE_SPEED = 3
MAX_DISTANCE = 200


class Item(Entity):
    # startRect is the Rect of the sprite that generates the projectile
    # direction is an int that specifies which direction projectile moves
    # 0: up, 1: right, 2: down, 3: left
    def __init__(self, x, y, imagePath):
        IMAGES = None
        Entity.__init__(self)
        if not IMAGES:
            self.load_images(imagePath)
        self.image = self.IMAGES
        self.distance = 0
        self.isPickedUp = False
        self.rect = self.image.get_rect()
    # Starting position of projectile equals starting position of
        self.rect.centerx = x
        self.rect.centery = y

    def load_images(self, imagePath):
        self.IMAGES = PI.load(imagePath).convert_alpha()
        # self.IMAGES = PY.transform.scale(picture, (32, 32))
    # targetRect is the sprite of the target of the projectile
    # Returns 1 if the projectile hit its target
    # Returns 0 if the projectile has not reached its max range
    # Returns -1 if the projectile has passed its max range

    def pickedUp(self, targetSprite):
        if PS.collide_rect(self, targetSprite):
            self.kill()
            self.isPickedUp = True

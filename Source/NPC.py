import os as OS
import sys as SYS
import random
import pygame as PY
import pygame.display as PD
import pygame.event as PE
import pygame.image as PI
import pygame.sprite as PS
import Setup
import LevelOne
import Projectile
from smooth import Entity
import Functions
from Character import BaseClass
from Screen import Globals
SPEED = 1

Dir = OS.getcwd()


MIN_MOVE_DURATION = 20
MAX_MOVE_DURATION = 50

MIN_WAIT_DURATION = 25
MAX_WAIT_DURATION = 75

MAX_X = 50
MAX_Y = 50

TIME_UPDATE = 5


class NPC(Entity):
    def __init__(self, image_path):
        IMAGES = None
        self.image_path = image_path
        Entity.__init__(self)
        if not IMAGES:
            self.load_images()
        self.image = self.IMAGES[0]
        self.rect = self.image.get_rect()
        self.image_tracker = 0
        self.direction = 0
        self.moveCounter = 0  # allows for smooth movement
        self.moveDuration = 0  # randomly generated for random movements
        self.counter = 0  # used to make npc move more slowly
        self.isMoving = False  # indicates if npc is currently moving
        self.change_direction = False
        self.image_timer = 0

        #  Boundaries for the NPC
        # self.MIN_X_POS = self.rect.width/2
        # self.MAX_X_POS = Globals.WORLD.realwidth - self.rect.width/2
        # self.MIN_Y_POS = self.rect.height/2
        # self.MAX_Y_POS = Globals.WORLD.realheight - self.rect.height/2

        # choose starting position
        # self.rect.centerx = random.randint(self.MIN_X_POS, self.MAX_X_POS)
        # self.rect.centery = random.randint(self.MIN_Y_POS, self.MAX_Y_POS)

    #  load NPC sprite
    def load_images(self):
        self.IMAGES = []
        sheet = PI.load(self.image_path).convert()
        key = sheet.get_at((0, 0))
        for i in range(3):
            for j in range(4):
                surface = PY.Surface((32, 32)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i*32, j*32, 32, 32))
                self.IMAGES.append(surface)

    def update_image(self, image_num, change_direction = False, cutscene = False):
        if self.image_timer > TIME_UPDATE or change_direction or cutscene:
            self.image = self.IMAGES[image_num]
            self.image.convert_alpha()
            self.image_tracker = (self.image_tracker+1) % 3
            self.image_timer = 0
            self.change_direction = False
        else:
            self.image_timer += 1

    #  move NPC, then detect for collisions and throw projectiles as necessary
    def update(self, wallMap):
        # Determines whether we need to decide on a new movement direction
        if self.moveCounter >= self.moveDuration:
            # Determines if NPC should move or stand still
            moveVal = random.randint(0, 3)
            if moveVal <= 2:  # 75% chance of standing still
                self.isMoving = False
                self.moveCounter = 0  # reset moveCounter
                self.moveDuration = random.randint(MIN_WAIT_DURATION, MAX_WAIT_DURATION)
                isCollision = False
            else:  # 25% chance of moving
                self.isMoving = True
                self.moveCounter = 0  # reset moveCounter
                self.moveDuration = random.randint(
                    MIN_MOVE_DURATION,
                    MAX_MOVE_DURATION)  # new moveDuration
                # decides which direction to move in
                temp = self.direction
                self.direction = random.randint(0, 3)
                if temp != self.direction:
                    self.change_direction = True
                isCollision = False
        else:
            self.moveCounter += 1  # increment moveCounter

        if self.isMoving:  # npc currently moving
            if self.moveCounter % 2 == 0:  # makes NPCs move more slowly
                if self.direction == 0:  # up movement
                    self.rect.centery -= SPEED
                    self.update_image(self.image_tracker*4+3, self.change_direction)
                    # adjust in case results in collision
                    self.collide(0, -self.rect.centery, wallMap)
                elif self.direction == 1:  # right movement
                    self.rect.centerx += SPEED
                    self.update_image(self.image_tracker*4+2, self.change_direction)
                    # adjust in case results in collision
                    self.collide(self.rect.centerx, 0, wallMap)
                elif self.direction == 2:  # down movement
                    self.rect.centery += SPEED
                    self.update_image(self.image_tracker*4, self.change_direction)
                    # adjust in case results in collision
                    self.collide(0, self.rect.centery, wallMap)
                else:  # left movement
                    self.rect.centerx -= SPEED
                    self.update_image(self.image_tracker*4+1, self.change_direction)
                    # adjust in case results in collision
                    self.collide(-self.rect.centerx, 0, wallMap)
    #  check for collisions with other sprites

    def collide(self, xvel, yvel, wallMap):
        FADEOUTTIME = 0.2
        for p in wallMap:
            if PS.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                elif xvel < 0:
                    self.rect.left = p.rect.right
                elif yvel > 0:
                    self.rect.bottom = p.rect.top
                elif yvel < 0:
                    self.rect.top = p.rect.bottom
                else:
                    continue


class Sheep(NPC):
    def __init__(self, image_path, x = 0, y = 0):
        NPC.__init__(self, image_path)
        self.image_path = image_path
        IMAGES = []
        if not IMAGES:
            self.load_images()
        self.image = self.IMAGES[self.image_tracker]
        self.rect = self.image.get_rect()
        self.startx = self.rect.centerx
        self.starty = self.rect.centery
        self.rect.centerx = x
        self.rect.centery = y
        self.change_direction = False
        self.image_timer = 0

    #  load NPC sprite
    def load_images(self):
        Sheep.IMAGES = []
        sheet = PI.load(self.image_path).convert_alpha()
        key = sheet.get_at((0, 0))
        for i in range(3):
            for j in range(4):
                surface = PY.Surface((32, 32)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i*32, j*32, 32, 32))
                Sheep.IMAGES.append(surface)

    def update_image(self, image_num, change_direction):
        if self.image_timer > TIME_UPDATE or change_direction:
            self.image = Sheep.IMAGES[image_num]
            self.image.convert_alpha()
            self.image_tracker = (self.image_tracker+1) % 3
            self.image_timer = 0
            self.change_direction = False
        else:
            self.image_timer += 1


class Wagon(NPC):
    def __init__(self, image_path, x = 0, y = 10):
        NPC.__init__(self, image_path)
        self.image_path = image_path
        self.IMAGES = []
        if not self.IMAGES:
            self.load_images()
        self.image = self.IMAGES[2]
        self.rect = self.image.get_rect()
        self.startx = self.rect.centerx
        self.starty = self.rect.centery
        self.rect.centerx = x * 32
        self.rect.centery = y * 32
        self.change_direction = False
        self.image_timer = 0
        self.image_tracker = 1
        self.isBroken = False
        self.direction = 2
    #  load NPC sprite

    def load_images(self):
        self.IMAGES = []
        sheet = PI.load(self.image_path).convert_alpha()
        key = sheet.get_at((0, 0))
        for i in range(3):
            for j in range(4):
                surface = PY.Surface((100, 92)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i*100, j*92, 100, 92))
                self.IMAGES.append(surface)

    def update_image(self, image_num):
        if self.image_timer > TIME_UPDATE:
            self.image = self.IMAGES[image_num]
            self.image.convert_alpha()
            self.image_tracker = (self.image_tracker+1) % 3
            self.image_timer = 0
        else:
            self.image_timer += 1

    def update(self):
        if self.isBroken == False:
            self.update_image(self.image_tracker*4 + self.direction)
            self.move()

    def move(self):
        if self.direction == 0:
            self.rect.centery += SPEED
        elif self.direction == 1:
            self.rect.centerx -= SPEED
        elif self.direction == 2:
            self.rect.centerx += SPEED
        elif self.direction == 3:
            self.rect.centery -= SPEED

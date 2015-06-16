import os as OS
import sys as SYS
import pygame as PY
import pygame.display as PD
import pygame.event as PE
import pygame.image as PI
import pygame.sprite as PS
import pygame.mixer as PX
import Setup
from Screen import Globals
from Character import BaseClass
from smooth import Entity
import Player
Dir = OS.getcwd()
PROJECTILE_SPEED = 4
MAX_DISTANCE = 300
TIME_UPDATE = 5
whirlpool_path = OS.path.join(OS.path.dirname(Dir), 'Images/waterPuddle.png')


hurt_sound = OS.path.join(OS.path.dirname(Dir), 'Sounds/hurtSound.wav')

class Projectile(Entity):
    # startRect is the Rect of the sprite that generates the projectile
    # direction is an int that specifies which direction projectile moves
    # 0: up, 1: right, 2: down, 3: left
    def __init__(self, startRect, direction, PROJECTILE_IMAGES, imagePath = None, isPlayer = False):
        PX.init()
        self.hurtSound = PX.Sound(hurt_sound)
        self.hurtSound.set_volume(Globals.VOLUME/200.0)

        self.IMAGES = PROJECTILE_IMAGES
        Entity.__init__(self)
        if not self.IMAGES:
            self.load_images(imagePath)
        self.image = self.IMAGES[0]
        self.image_timer = 0
        self.image_tracker = 0
        self.direction = direction
        self.distance = 0
    # Determines whether or not we should worry about orienting the position of the projectile
        self.isPlayer = isPlayer
        self.rect = self.image.get_rect()
    # Starting position of projectile equals starting position of
        self.rect.centerx = startRect.centerx
        self.rect.centery = startRect.centery

    def load_images(self, imagePath):
        # Loads Fireball spritesheet
        self.IMAGES = []
        self.image = PI.load(imagePath).convert_alpha()
        fireball_sheet = PI.load(imagePath).convert_alpha()
        key = fireball_sheet.get_at((0, 0))
        for i in range(5):
            for j in range(4):
                surface = PY.Surface((32, 32)).convert()
                surface.set_colorkey(key)  # sets colorkey to top left corner's color
                surface.blit(fireball_sheet, (0, 0), (i*32, j*32, 32, 32))
                self.IMAGES.append(surface)

    # targetRect is the sprite of the target of the projectile
    # Returns 1 if the projectile hit its target
    # Returns 0 if the projectile has not reached its max range
    # Returns -1 if the projectile has passed its max range
    def update(self, targetSpriteGroup = None):

        # If reached max range
        if self.distance >= MAX_DISTANCE:
            self.kill()

        # If there are enemies
        if targetSpriteGroup != None:
            for targetSprite in targetSpriteGroup:
                # If collided
                if PS.collide_rect(self, targetSprite):
                    # Removes this sprite from all groups.
                    # Should delete from screen
                    self.kill()
                    if isinstance(targetSprite, Player.Player):
                        Globals.HERO.health -= 10
                        self.hurtSound.play()
                    else:
                        targetSprite.health -= 4
                        targetSprite.status = "burn"
        if self.isPlayer:
        # Move the projectile
            if self.direction == 0 or self.direction == "moveup":  # up
                self.update_image(self.image_tracker*4 + 2)
                self.rect.centery -= PROJECTILE_SPEED
            elif self.direction == 1 or self.direction == "moveright":  # right
                self.update_image(self.image_tracker*4)
                self.rect.centerx += PROJECTILE_SPEED
            elif self.direction == 2 or self.direction == "movedown":  # down
                self.update_image(self.image_tracker*4 + 3)
                self.rect.centery += PROJECTILE_SPEED
            elif self.direction == 3 or self.direction == "moveleft":  # left
                self.update_image(self.image_tracker*4 + 1)
                self.rect.centerx -= PROJECTILE_SPEED
        else:
            if self.direction == 0 or self.direction == "moveup":  # up
                # self.update_image(self.image_tracker*4 + 2)
                self.rect.centery -= PROJECTILE_SPEED
            elif self.direction == 1 or self.direction == "moveright":  # right
                # self.update_image(self.image_tracker*4)
                self.rect.centerx += PROJECTILE_SPEED
            elif self.direction == 2 or self.direction == "movedown":  # down
                # self.update_image(self.image_tracker*4 + 3)
                self.rect.centery += PROJECTILE_SPEED
            elif self.direction == 3 or self.direction == "moveleft":  # left
                # self.update_image(self.image_tracker*4 + 1)
                self.rect.centerx -= PROJECTILE_SPEED
            self.update_image(self.image_tracker)
        self.distance += PROJECTILE_SPEED

    def update_image(self, image_num):
        if self.image_timer > TIME_UPDATE:
            self.image = self.IMAGES[image_num]
            self.image.convert_alpha()
            if self.isPlayer:
                self.image_tracker = (self.image_tracker+1) % 4
            else:
                self.image_tracker = (self.image_tracker+1) % len(self.IMAGES)
            self.image_timer = 0
        else:
            self.image_timer += 1


class Special(Entity):
    def __init__(self, hero, direction, distance):
        Entity.__init__(self)
        self.inner_rect = PY.Rect(64, 64, 64, 64)
        self.inner_rect.center = hero.rect.center
        self.outer_rect = PY.Rect(128, 128, 128, 128)
        self.outer_rect.center = hero.rect.center
        self.direction = direction
        self.distance = distance

    def update(self, targetSpriteGroup = None):
        if self.direction == "moveup":  # up
            self.inner_rect.centery -= self.distance
        elif self.direction == "moveright":  # right
            self.inner_rect.centerx += self.distance
        elif self.direction == "movedown":  # down
            self.inner_rect.centery += self.distance
        elif self.direction == "moveleft":  # left
            self.inner_rect.centerx -= self.distance
        self.outer_rect.center = self.inner_rect.center
        if targetSpriteGroup != None:
            for targetSprite in targetSpriteGroup:
                # If collided
                if PY.Rect.colliderect(self.inner_rect, targetSprite.rect):
                    if targetSprite.status == "burn":
                        targetSprite.health -= (600-self.distance)/300 * 10 * 1.5
                    else:
                        targetSprite.health -= (600-self.distance)/300 * 10
                elif PY.Rect.colliderect(self.outer_rect, targetSprite.rect):
                    if targetSprite.status == "burn":
                        targetSprite.health -= (600-self.distance)/300 * 5 * 1.5
                    else:
                        targetSprite.health -= (600-self.distance)/300 * 5

            self.kill()

class Whirlpool(Entity):
    def __init__(self, boss, hero, direction):
        Entity.__init__(self)
        self.IMAGES = []
        if not self.IMAGES:
            self.load_images()
        self.image = self.IMAGES[0]
        self.rect = self.image.get_rect()
        if direction == 0:
            self.rect.center = (boss.centery - 100, boss.centerx)
        if direction == 2:
            self.rect.center = (boss.centery + 100, boss.centerx)       
        if direction == 1:
            self.rect.center = (boss.centery, boss.centerx+100)           
        if direction == 3:
            self.rect.center = (boss.centery, boss.centerx-100)
        self.image_tracker = 0
        self.image_timer = 0
        self.rect = Globals.WORLD.camera.apply(self.rect)
    def load_images(self):
        whirlpool = PI.load(whirlpool_path).convert_alpha()
        key = whirlpool.get_at((0,0))
        for i in range(3):
            surface = PY.Surface((64,26)).convert()
            surface.set_colorkey(key)
            surface.blit(whirlpool, (0,0), (i*64, 0, 64, 26))
            self.IMAGES.append(surface)
    def update(self, hero):
        for i in hero:
            if self.rect.colliderect(i.rect):
                i.health -= 1
                i.speed = .7
            else:
                i.speed = 3.0
        self.update_image()
    def update_image(self):
        if self.image_timer > TIME_UPDATE:
            self.image = self.IMAGES[self.image_tracker]
            self.image_tracker = (self.image_tracker +1) % 3
        else:
            self.image_timer += 1

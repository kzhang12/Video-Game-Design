import os as OS
import sys as SYS
import pygame as PG
import time
import pygame.image as PI
import pygame.time as PT
from smooth import Entity
from Screen import Globals
SPEED = 1

Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir), 'Images/npc.png')
firewood_image = OS.path.join(OS.path.dirname(Dir), 'Images/firewood.png')

MIN_MOVE_DURATION = 20
MAX_MOVE_DURATION = 50

MIN_WAIT_DURATION = 50
MAX_WAIT_DURATION = 150

MAX_X = 50
MAX_Y = 50


class HeadsUpDisplay(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.rect = PG.Rect(0, 550, 800, 50)
        self.display = PG.Surface((self.rect.width, self.rect.height))
        self.time = 1000
        self.supplyCount = 0
        picture = PI.load(firewood_image).convert_alpha()
        self.supplyImage = PG.transform.scale(picture, (32, 32))
        self.cooldownTimer = time.time()
        self.cooldownTimer2 = time.time()
        self.static_score = 0

    def update(self):
        # self.display = Globals.WORLD.camera.apply(self.display)
        if self.cooldownTimer <= 50:
            self.cooldownTimer += .71
        if self.cooldownTimer2 <= 50:
            self.cooldownTimer2 += .71
        currTime = time.time()

        elapsedTime = currTime - self.cooldownTimer
        percentageTimeLeft = int(elapsedTime*50)
        if percentageTimeLeft >= 100:
            percentageTimeLeft = 100

        elapsedTime2 = currTime - self.cooldownTimer2
        # print elapsedTime2
        percentageTimeLeft2 = int(elapsedTime2*10)
        if percentageTimeLeft2 >= 100:
            percentageTimeLeft2 = 100

        self.display.fill((190, 60, 10))
        self.healthText = Globals.FONT.render("Health:", True, (255, 255, 255))
        self.display.blit(self.healthText, (0, 15))
        self.healthBarBack = PG.Surface((100, 20))
        self.healthBarBack.fill((255, 0, 0))
        self.display.blit(self.healthBarBack, (75, 15))
        self.healthBarFront = PG.Surface((100-(100 - Globals.HERO.health), 20))
        self.healthBarFront.fill((0, 255, 0))
        self.display.blit(self.healthBarFront, (75, 15))
        self.cooldownText = Globals.FONT.render("Cooldown:", True, (255, 255, 255))
        self.display.blit(self.cooldownText, (200, 15))
        self.cooldownBarBack = PG.Surface((100, 10))
        self.cooldownBarBack.fill((0, 0, 255))
        self.display.blit(self.cooldownBarBack, (275, 15))
        self.cooldownBarFront = PG.Surface((100 - (100-percentageTimeLeft), 10))
        self.cooldownBarFront.fill((0, 255, 255))
        self.display.blit(self.cooldownBarFront, (275, 15))
        self.cooldownBarBack2 = PG.Surface((100, 10))
        self.cooldownBarBack2.fill((0, 0, 255))
        self.display.blit(self.cooldownBarBack2, (275, 30))
        self.cooldownBarFront2 = PG.Surface((100 - (100-percentageTimeLeft2), 10))
        self.cooldownBarFront2.fill((0, 255, 255))
        self.display.blit(self.cooldownBarFront2, (275, 30))
        self.timeText = Globals.FONT.render("Time: " + str(self.time), True, (255, 255, 255))
        self.display.blit(self.timeText, (400, 15))
        self.scoreText = Globals.FONT.render("Score: " + str(self.static_score), True, (255, 255, 255))
        self.display.blit(self.scoreText, (500, 15))
        self.supplyText = Globals.FONT.render("Supply:", True, (255, 255, 255))
        self.display.blit(self.supplyText, (600, 15))
        self.supplyTracker = Globals.FONT.render("x " + str(self.supplyCount), True, (255, 255, 255))
        if self.supplyCount > 0:
            self.display.blit(self.supplyTracker, (712, 15))
            self.display.blit(self.supplyImage, (675, 10))
        Globals.SCREEN.blit(self.display, (0, 550))

    def updateHealth(self):
        pass

    def updateSupply(self, item):
        self.supplyCount += 1

    def resetSupply(self):
        self.supplyCount = 0

    def updateTime(self, time):
        self.time = time

    def updateCooldown(self):
        self.cooldownTimer = time.time()

    def updateCooldown2(self):
        self.cooldownTimer2 = time.time()

    def updateScore(self, score):
        self.static_score += score
        Globals.SCORE = self.static_score

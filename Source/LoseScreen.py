import os as OS
import Setup
import sys as SYS
import pygame as PG
import pygame.mouse as PM
import pygame.display as PDI
import pygame.event as PE
import pygame.font as PF
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX
import Player
import Enemy
import Setup
import Menu as Menu
import Score
from Screen import BaseState as State
from Screen import Globals
Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir), 'Images/lose_screen.jpg')
sound_path = OS.path.join(OS.path.dirname(Dir), 'Sounds/screen_start.wav')


class LoseScreen(State):
    FADEINTIME = 2.0
    FADEOUTTIME = 0.2

    def __init__(self, score):
        Globals.WORLD.clear()
        State.__init__(self)
       
        PX.stop() 
        Globals.ISMAINMENU = True
         
        self.color = PC.Color("black")
        self.time = 0.0
        Globals.WORLD.clear()
        Globals.SCREEN.fill(PC.Color("black"))
        self.score = score
        Globals.ISLEVELONE = False

    def render(self):
        Globals.SCREEN.fill(PC.Color("black"))
        sheet = PI.load(image_path).convert()
        Globals.SCREEN.blit(sheet, (0, 0))

    def update(self, time):
        self.time += time
        if self.time < LoseScreen.FADEINTIME:
            ratio = self.time / LoseScreen.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.RUNNING = False
        elif event.type == PG.KEYDOWN and event.key == PG.K_SPACE:
            PX.music.fadeout(int(LoseScreen.FADEOUTTIME*1000))
            Globals.STATE = Score.Score_Screen(self.score)

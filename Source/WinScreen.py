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
image_path = OS.path.join(OS.path.dirname(Dir), 'Images/win_screen.jpg')


class WinScreen(State):
    FADEINTIME = 2.0
    FADEOUTTIME = 0.2

    def __init__(self, score):
        State.__init__(self)
        self.color = PC.Color("black")
        self.time = 0.0
       
        PX.stop() 
        Globals.ISMAINMENU = True
        
        Globals.WORLD.clear()
        Globals.SCREEN.fill(PC.Color("black"))
        self.score = score
        Globals.ISLEVELONE = False

    def render(self):
        surf = Globals.FONT.render("Victory",
                                   True, self.color)
        width, height = surf.get_size()
        sheet = PI.load(image_path).convert()
        Globals.SCREEN.blit(sheet, (0, 0))
        Globals.SCREEN.blit(surf, (Globals.WIDTH/2 - width/2,
                            Globals.HEIGHT/4 - height/2))

    def update(self, time):
        self.time += time
        if self.time < WinScreen.FADEINTIME:
            ratio = self.time / WinScreen.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.RUNNING = False
        elif event.type == PG.KEYDOWN and event.key == PG.K_SPACE:
            PX.music.fadeout(int(WinScreen.FADEOUTTIME*1000))
            Globals.STATE = Score.Score_Screen(Globals.CURRENT_PLAYER[3])

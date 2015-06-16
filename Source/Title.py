import sys as SYS
import os as OS
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
from Screen import BaseState as State
from Screen import Globals
import Menu as Menu
Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir), 'Images/title_screen.png')
sound_path = OS.path.join(OS.path.dirname(Dir), 'Sounds/screen_load.flac')


class Title_Screen(State):

    FADEINTIME = 1.5
    HOLDTIME = 3.8
    FADEOUTTIME = 1.5
    MUSICFILE = sound_path

    def __init__(self):
        State.__init__(self)
        self.color = PC.Color("black")
        Globals.SCREEN.fill(PC.Color("black"))
        self.playSound = True
        self.time = 0

    def render(self):
        surf = Globals.FONT.render("Guardian of the Elements",
                                   True, self.color)
        width, height = surf.get_size()
        sheet = PI.load(image_path).convert()
        Globals.SCREEN.blit(sheet, (0, 0))
        Globals.SCREEN.blit(surf, (Globals.WIDTH/2 - width/2,
                            Globals.HEIGHT/4 - height/2))

    def update(self, time):
        self.time += time
        if self.time < Title_Screen.FADEINTIME:
            ratio = self.time / Title_Screen.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)
        elif self.time <= Title_Screen.HOLDTIME:
            self.sound = PX.Sound(Title_Screen.MUSICFILE)
            if self.playSound:
                self.sound.play()
                self.playSound = False
        else:
            Globals.STATE = Menu.Menu()

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.RUNNING = False
        elif event.type == PG.KEYDOWN and event.key == PG.K_SPACE:
            # self.sound.fadeout(int(Title_Screen.FADEOUTTIME*1000))
            Globals.STATE = Menu.Menu()

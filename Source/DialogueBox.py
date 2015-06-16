import os as OS
import sys as SYS
import pygame as PY
import pygame.draw as PD
import pygame.display as PDI
import pygame.image as PI
import pygame.event as PE
import pygame.time as PT
import pygame.mixer as PX
import pygame.color as PC
import pygame.joystick as PJ
import Functions
import Setup
import Character
import Score
import LevelOne
import WinScreen
import LoseScreen
import Projectile
import string
from Character import BaseClass
from smooth import wallMap
from smooth import Grass
from smooth import Sand
from smooth import Grey_brick
from smooth import Entity
from Screen import Globals
Dir = OS.getcwd()

PJ.init()
if PJ.get_count() > 0:
    joystick = PJ.Joystick(0)
    joystick.init()

class Dialogue_box:

    def __init__(self, data=None, x=0, y=0):
        self.current_string = []
        self.fontobject = Globals.FONT
        self.screen = Globals.SCREEN

        data_path = OS.path.join(OS.path.dirname(Dir), 'Data')
        data_path1 = OS.path.join(data_path, data)
        self.text = open(data_path1, 'r')
        self.width = 0
        for line in self.text:
            self.temp = self.fontobject.size(line)[0]
            if self.temp > self.width:
                self.width = self.temp
            if "@" in line:
                self.width += len(Globals.CURRENT_PLAYER[0])
        self.rect = PY.Rect(x, y, self.width, 20)
        self.text.close()
        self.text = open(data_path1, 'r')
        self.isOpen = True

    def update(self):
        FirstTime = True

        for line in self.text:
            Fast = False
            if not FirstTime:
                key = self.get_key()
                if key == 27:
                    return 0

            self.current_string = []
            for i in range(len(line)):
                if i != len(line)-1:
                    PD.rect(self.screen, (0, 0, 0), self.rect)

                for event in PE.get():
                    if event.type == PY.QUIT:
                        Globals.RUNNING = False
                    elif event.type == PY.KEYDOWN or event.type == PY.JOYBUTTONDOWN:
                        Fast = True
                timer = 0
                current_char = line[i]
                if current_char == '@' or current_char == '#' or current_char == '%':
                    if current_char == '@':
                        name = Globals.CURRENT_PLAYER[0]
                    if current_char == '%':
                        name = Globals.CURRENT_PLAYER[1]
                    if current_char == '#':
                        name = Globals.CURRENT_PLAYER[2]
                    for j in range(len(name)):
                        PD.rect(self.screen, (0, 0, 0), self.rect)
                        timer = 0
                        name_char = name[j]
                        self.current_string.append("".join(name_char))
                        message = string.join(self.current_string, "")
                        self.screen.blit(self.fontobject.render
                                         (message, 1, (255, 255, 255)),
                                         self.rect)
                        while timer < 700000 and not Fast:
                            timer += 1
                        PDI.flip()
                elif current_char != '\n':
                    self.current_string.append("".join(current_char))
                    message = string.join(self.current_string, "")
                    self.screen.blit(self.fontobject.render
                                     (message, 1, (255, 255, 255)), self.rect)
                    while timer < 700000 and not Fast:
                        timer += 1
                PDI.flip()
            FirstTime = False
        self.text.close()
        key = self.get_key()
        self.isOpen = False

    def get_key(self):
        while 1:
            event = PE.poll()
            if event.type == PY.KEYDOWN or event.type == PY.JOYBUTTONDOWN:
                return 27
            else:
                pass

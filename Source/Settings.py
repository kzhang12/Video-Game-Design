import os as OS
import Setup
import Menu
import sys as SYS
import pygame as PG
import pygame.mouse as PM
import pygame.draw as PD
import pygame.display as PDI
import pygame.event as PE
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX
import pygame.font as PF
import pygame.key as PK
from Screen import BaseState as State
from Screen import Globals
import LevelOne as GS
import Score as Score
import string
Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir), 'Images/menu_screen.jpg')
menu_select = OS.path.join(OS.path.dirname(Dir), 'Sounds/menuSelect.wav')
INTERVAL = 20


class Settings(State):

    def __init__(self, bright, vol):
        State.__init__(self)
        self.color = PC.Color("black")
        self.time = 0.0
        Globals.FONT = PF.SysFont("monospace", 15)
        Globals.SCREEN.fill(PC.Color("black"))
        self.hover = [False, False, False, False, False]
        self.lastHover = [False, False, False, False, False]
        self.brightness_up = []
        self.brightness_down = []
        self.volume_up = []
        self.volume_down = []
        self.exit = []
        self.brightness_pos = bright
        self.volume_pos = vol
        PX.init()
        self.menuSelect = PX.Sound(menu_select)
        self.menuSelect.set_volume(Globals.VOLUME/200.0)

    def render(self):
        # Background
        sheet = PI.load(image_path).convert()
        Globals.SCREEN.blit(sheet, (0, 0))
        # Title
        surf = Globals.FONT.render("Settings", True, self.color)
        self.width, height = surf.get_size()
        Globals.SCREEN.blit(surf, (0 + self.width/2, 0 + height/2))
        # Brightness
        surf = Globals.FONT.render("Brightness", True, self.color)
        self.width, height = surf.get_size()
        Globals.SCREEN.blit(surf, (20, 100 + Globals.HEIGHT/2))
        # Volume
        surf = Globals.FONT.render("Volume", True, self.color)
        self.width, height = surf.get_size()
        Globals.SCREEN.blit(surf, (20, 140 + Globals.HEIGHT/2))
        # Figures out whether or not it is mouse rollover
        # Brightness Up Button
        if not self.hover[0]:
            self.BRIGHTNESS_UP = Globals.FONT.render("+", True, self.color)
            if self.lastHover[0] == False:
                self.lastHover[0] = True
                self.menuSelect.play()
        else:
            self.BRIGHTNESS_UP = Globals.FONT.render("+",
                                                True, PC.Color("black"),
                                                PC.Color("white"))
            self.lastHover[0] = False

        Globals.SCREEN.blit(
            self.BRIGHTNESS_UP,
            (350, Globals.HEIGHT/2+100))
        self.brightness_up_button_rect = self.BRIGHTNESS_UP.get_rect(topleft=(350,
                                                    Globals.HEIGHT/2 + 100))
        self.brightness_up_button = [self.brightness_up_button_rect.left,
                         self.brightness_up_button_rect.right,
                         self.brightness_up_button_rect.top,
                         self.brightness_up_button_rect.bottom]
        # Brightness Down Button
        if not self.hover[1]:
            self.BRIGHTNESS_DOWN = Globals.FONT.render("-", True, self.color)
            if self.lastHover[1] == False:
                self.lastHover[1] = True
                self.menuSelect.play()
        else:
            self.BRIGHTNESS_DOWN = Globals.FONT.render("-",
                                                True, PC.Color("black"),
                                                PC.Color("white"))
            self.lastHover[1] = False
        # TODO position buttons correctly
        Globals.SCREEN.blit(
            self.BRIGHTNESS_DOWN,
            (125, Globals.HEIGHT/2+100))
        self.brightness_down_button_rect = self.BRIGHTNESS_DOWN.get_rect(topleft=(125,
                                                    Globals.HEIGHT/2 + 100))
        self.brightness_down_button = [self.brightness_down_button_rect.left,
                         self.brightness_down_button_rect.right,
                         self.brightness_down_button_rect.top,
                         self.brightness_down_button_rect.bottom]
        # Volume Up Button
        if not self.hover[2]:
            self.VOLUME_UP = Globals.FONT.render("+", True, self.color)
            if self.lastHover[2] == False:
                self.lastHover[2] = True
                self.menuSelect.play()
        else:
            self.VOLUME_UP = Globals.FONT.render("+",
                                                True, PC.Color("black"),
                                                PC.Color("white"))
            self.lastHover[2] = False
        # TODO position buttons correctly
        Globals.SCREEN.blit(
            self.VOLUME_UP,
            (350, Globals.HEIGHT/2+140))
        self.volume_up_button_rect = self.VOLUME_UP.get_rect(topleft=(350,
                                                    Globals.HEIGHT/2 + 140))
        self.volume_up_button = [self.volume_up_button_rect.left,
                         self.volume_up_button_rect.right,
                         self.volume_up_button_rect.top,
                         self.volume_up_button_rect.bottom]
        # Volume Down Button
        if not self.hover[3]:
            self.VOLUME_DOWN = Globals.FONT.render("-", True, self.color)
            if self.lastHover[3] == False:
                self.lastHover[3] = True
                self.menuSelect.play()
        else:
            self.VOLUME_DOWN = Globals.FONT.render("-",
                                                True, PC.Color("black"),
                                                PC.Color("white"))
            self.lastHover[3] = False
        # TODO position buttons correctly
        Globals.SCREEN.blit(
            self.VOLUME_DOWN,
            (125, Globals.HEIGHT/2+140))
        self.volume_down_button_rect = self.VOLUME_DOWN.get_rect(topleft=(125,
                                                    Globals.HEIGHT/2 + 140))
        self.volume_down_button = [self.volume_down_button_rect.left,
                         self.volume_down_button_rect.right,
                         self.volume_down_button_rect.top,
                         self.volume_down_button_rect.bottom]

        # Exit Button
        if not self.hover[4]:
            self.EXIT = Globals.FONT.render("Exit", True, self.color)
            if self.lastHover[4] == False:
                self.lastHover[4] = True
                self.menuSelect.play()
        else:
            self.EXIT = Globals.FONT.render("Exit",
                                                True, PC.Color("black"),
                                                PC.Color("white"))
            self.lastHover[4] = False
        # TODO position buttons correctly
        Globals.SCREEN.blit(
            self.EXIT,
            (20, Globals.HEIGHT/2+180))
        self.exit_button_rect = self.EXIT.get_rect(topleft=(20,
                                                    Globals.HEIGHT/2 + 180))
        self.exit_button = [self.exit_button_rect.left,
                         self.exit_button_rect.right,
                         self.exit_button_rect.top,
                         self.exit_button_rect.bottom]
    
        # Scales
        self.brightness_scale = PG.Rect(142, Globals.HEIGHT/2 + 100,
                                        200, 15)
        self.brightness_cursor = PG.Rect(240 + self.brightness_pos, Globals.HEIGHT/2 + 100,
                                        4, 15)
        self.volume_scale = PG.Rect(142, Globals.HEIGHT/2 + 140,
                                        200, 15)
        self.volume_cursor = PG.Rect(240 + self.volume_pos, Globals.HEIGHT/2 + 140,
                                        4, 15)
        PG.draw.rect(Globals.SCREEN, (0, 150, 0), self.brightness_scale)
        PG.draw.rect(Globals.SCREEN, (0, 150, 0), self.volume_scale)
        PG.draw.rect(Globals.SCREEN, (0, 0, 255), self.brightness_cursor)
        PG.draw.rect(Globals.SCREEN, (0, 0, 255), self.volume_cursor)
        PG.display.update()

    def update(self, time):
        self.time += time
        if self.time < Menu.FADEINTIME:
            ratio = self.time / Menu.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)
        position = PM.get_pos()
        if self.inrange(self.brightness_up_button, position):
            self.hover[0] = True
        else:
            self.hover[0] = False

        if self.inrange(self.brightness_down_button, position):
            self.hover[1] = True
        else:
            self.hover[1] = False

        if self.inrange(self.volume_up_button, position):
            self.hover[2] = True
        else:
            self.hover[2] = False

        if self.inrange(self.volume_down_button, position):
            self.hover[3] = True
        else:
            self.hover[3] = False

        if self.inrange(self.exit_button, position):
            self.hover[4] = True
        else:
            self.hover[4] = False

    def inrange(self, ranges, position):
        if (position[0] <= ranges[1]and position[0] >= ranges[0])and (position[1] <= ranges[3] and position[1] >= ranges[2]):
            return True
        else:
            return False

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.RUNNING = False
        elif event.type == PG.MOUSEBUTTONDOWN:
            position = PM.get_pos()
            if self.brightness_up_button_rect.collidepoint(position):
                if self.brightness_pos < 100:
                    self.brightness_pos += INTERVAL
                Globals.BRIGHTNESS = self.brightness_pos
            if self.brightness_down_button_rect.collidepoint(position):
                if self.brightness_pos > -100:
                    self.brightness_pos -= INTERVAL
                Globals.BRIGHTNESS = self.brightness_pos
            if self.volume_up_button_rect.collidepoint(position):
                if self.volume_pos < 100:
                    self.volume_pos += INTERVAL
            if self.volume_down_button_rect.collidepoint(position):
                if self.volume_pos > -100:
                    self.volume_pos -= INTERVAL
            if self.exit_button_rect.collidepoint(position):
                Globals.VOLUME = self.volume_pos + 100
                PX.music.fadeout(int(Score.Score_Screen.FADEOUTTIME*1000))
                Globals.STATE = Menu.Menu()

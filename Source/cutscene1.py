import sys as SYS
import time
import pygame as PG
import os as OS
import pygame.display as PDI
import pygame.draw as PD
import pygame.event as PE
import pygame.font as PF
import pygame.time as PT
import pygame.sprite as PS
import pygame.color as PC
import pygame.mixer as PX
import pygame.image as PI
import pygame.joystick as PJ
import DialogueBox as DB
from Screen import BaseState as State
from Screen import Globals
import LevelOne as GS
import LevelTwo
import Player
import NPC
import smooth
import Enemy
import Setup
Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir),
                          'Images/brick_wall_tiled_perfect.png')

Dir = OS.getcwd()
mom_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/mom_sprite.png')
dad_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/dad.png')
elder_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/elder.png')
firelord_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/FireLord.png')

PJ.init()
if PJ.get_count() > 0:
    joystick = PJ.Joystick(0)
    joystick.init()


class Cutscene(State):
    def __init__(self):
        State.__init__(self)
        self.rect1 = PG.Rect(0, 550, 800, 50)
        self.rect2 = PG.Rect(0, 0, 800, 50)
        self.rect3 = PG.Rect(750, 0, 50, 800)
        self.rect4 = PG.Rect(0, 0, 50, 800)
        smooth.loadtiles()
        Globals.WORLD = smooth.World("map.txt")
        Globals.WORLD.camera = smooth.Camera(smooth.complex_camera,
                                             Globals.WORLD,
                                             Globals.WORLD.realwidth,
                                             Globals.WORLD.realheight)

        self.npc1 = NPC.NPC(mom_image_path)
        self.npc2 = NPC.NPC(dad_image_path)
        self.npc1.rect.center = (451, 752)
        self.npc2.rect.center = (451, 752)
        self.Timer = 0
        self.npc1.image_tracker = 0

    def update(self, time):
        Globals.WORLD.background(Globals.SCREEN)
        Globals.WORLD.dr(Globals.SCREEN)
        Globals.WORLD.update(self.npc1)
        #PG.draw.rect(Globals.SCREEN, (0, 0, 0), self.rect1)
        #PG.draw.rect(Globals.SCREEN, (0, 0, 0), self.rect2)
        #PG.draw.rect(Globals.SCREEN, (0, 0, 0), self.rect3)
        #PG.draw.rect(Globals.SCREEN, (0, 0, 0), self.rect4)
        if self.Timer == 0:
            Globals.WORLD.addEntity(self.npc1)
        if self.Timer < 150:
            key = PG.event.get()
            for event in key:
                if event.type == PG.KEYDOWN or event.type == PG.JOYBUTTONDOWN:
                    self.Timer = 181
            Globals.WORLD.background(Globals.SCREEN)
            Globals.WORLD.dr(Globals.SCREEN)
            Globals.WORLD.update(self.npc1)
            set_timer = self.Timer % 10
            if set_timer == 0:
                self.npc1.rect.centery += 3
                self.npc1.update_image(self.npc1.image_tracker*4, False, True)
            self.Timer += 1
            PDI.flip()
        if self.Timer == 175:
            self.npc1.update_image(self.npc1.image_tracker*4+3, False, True)
            Globals.WORLD.addEntity(self.npc2)
        if self.Timer == 176:
            Dialogue = DB.Dialogue_box('cutscene1_dialogue.txt')
            while Dialogue.isOpen:
                Dialogue.update()
        self.Timer += 1
        if self.Timer == 183:
            Globals.WORLD.addEntity(self.npc2)
            self.npc1.rect.centery += 60
            self.npc1.update_image(self.npc1.image_tracker*4+3, True)
            self.endScene()
        #PG.draw.rect(Globals.SCREEN, (0, 0, 0), self.rect1)
        #PG.draw.rect(Globals.SCREEN, (0, 0, 0), self.rect2)
        #PG.draw.rect(Globals.SCREEN, (0, 0, 0), self.rect3)
        #PG.draw.rect(Globals.SCREEN, (0, 0, 0), self.rect4)
    def endScene(self):
        fpsClock = PT.Clock()
        DURATION = 2000.0
        start_time = PT.get_ticks()
        ratio = 0.0
        while ratio < 1.0:
            current_time = PT.get_ticks()
            ratio = (current_time - start_time)/DURATION
            if ratio > 1.0:
                ratio = 1.0
            value = int(255*ratio)
            fade_color = PC.Color(0, 0, 0, 0)
            fade_color.a = value
            # PD.rect(Globals.SCREEN, fade_color, (0,0,400,300))
            surf = PG.Surface((800, 600))
            surf.set_alpha(value)
            surf.fill((0, 0, 0))
            Globals.SCREEN.blit(surf, (0, 0))
            PDI.flip()
            fpsClock.tick(60)
        PX.stop()
        Globals.ISMAINMENU = False
        Globals.STATE = GS.LevelOne()


class Cutscene2(State):
    def __init__(self):
        State.__init__(self)
        self.rect = PG.Rect(0, 500, 800, 100)
        self.display = PG.Surface((self.rect.width, self.rect.height))
        self.display.fill((0, 0, 0))
        smooth.loadtiles()
        Globals.WORLD.clear()
        Globals.WORLD = smooth.World("map.txt")
        Globals.WORLD.camera = smooth.Camera(smooth.complex_camera,
                                             Globals.WORLD,
                                             Globals.WORLD.realwidth,
                                             Globals.WORLD.realheight)
        # Initializing village elder
        self.elder = NPC.NPC(elder_image_path)
        self.elder.rect.center = (77 * Setup.PIXEL_SIZE, 25 * Setup.PIXEL_SIZE - 8)
        Globals.WORLD.addEntity(self.elder)
        self.elder.image = self.elder.IMAGES[2]
        # Initializing fire lord
        self.firelord = NPC.NPC(firelord_image_path)
        self.firelord.image = self.firelord.IMAGES[6]
        self.firelord.rect.center = (77 * Setup.PIXEL_SIZE, 26 * Setup.PIXEL_SIZE+8)
        Globals.WORLD.addEntity(self.firelord)
        self.hero = Globals.HERO
        self.hero.rect.center = (88*32, 25*32)            
        self.hero.image = self.hero.IMAGES[1]
        Globals.WORLD.addEntity(self.hero)
        self.Timer = 0

    def update(self, time):
        Globals.WORLD.background(Globals.SCREEN)
        Globals.WORLD.dr(Globals.SCREEN)
        Globals.WORLD.update(self.firelord)
        Dialogue = DB.Dialogue_box('cutscene6_dialogue.txt')
        while self.Timer < 200:
            key = PG.event.get()
            for event in key:
                if event.type == PG.KEYDOWN or event.type == PG.JOYBUTTONDOWN:
                    self.Timer = 801
            Globals.WORLD.background(Globals.SCREEN)
            Globals.WORLD.dr(Globals.SCREEN)
            Globals.WORLD.update(self.firelord)
            set_timer = self.Timer % 4
            if set_timer == 0:
                self.firelord.rect.centerx += 3
                self.firelord.update_image(self.firelord.image_tracker*4+2, False, True)
                self.elder.rect.centerx += 3
                self.elder.update_image(self.elder.image_tracker*4+2, False, True)
            self.Timer += 1
            PDI.flip()
        if self.Timer == 210:
            while Dialogue.isOpen:
                Dialogue.update()
        if self.Timer > 250:
            self.endScene()

        self.Timer += 1

    def endScene(self):
        fpsClock = PT.Clock()
        DURATION = 2000.0
        start_time = PT.get_ticks()
        ratio = 0.0
        while ratio < 1.0:
            current_time = PT.get_ticks()
            ratio = (current_time - start_time)/DURATION
            if ratio > 1.0:
                ratio = 1.0
            value = int(255*ratio)
            fade_color = PC.Color(0, 0, 0, 0)
            fade_color.a = value
            # PD.rect(Globals.SCREEN, fade_color, (0,0,400,300))
            surf = PG.Surface((800, 600))
            surf.set_alpha(value)
            surf.fill((0, 0, 0))
            Globals.SCREEN.blit(surf, (0, 0))
            PDI.flip()
            fpsClock.tick(60)
        PX.stop()    
        Globals.ISMAINMENU = False
        Globals.STATE = GS.LevelOne()


class Cutscene3(State):

    def __init__(self):
        State.__init__(self)
        smooth.loadtiles()
        self.rect = PG.Rect(0, 500, 800, 100)
        self.display = PG.Surface((self.rect.width, self.rect.height))
        self.display.fill((0, 0, 0))
        Globals.WORLD.clear()
        Globals.WORLD = smooth.World("map.txt")
        Globals.WORLD.camera = smooth.Camera(smooth.complex_camera,
                                             Globals.WORLD,
                                             Globals.WORLD.realwidth,
                                             Globals.WORLD.realheight)
        # Initializing village elder
        self.elder = NPC.NPC(elder_image_path)
        self.elder.rect.center = (77 * Setup.PIXEL_SIZE+150, 25 * Setup.PIXEL_SIZE - 8)
        Globals.WORLD.addEntity(self.elder)
        self.elder.image = self.elder.IMAGES[2]
        # Initializing fire lord
        self.firelord = NPC.NPC(firelord_image_path)
        self.firelord.image = self.firelord.IMAGES[6]
        self.firelord.rect.center = (77 * Setup.PIXEL_SIZE+150, 26 * Setup.PIXEL_SIZE+8)
        Globals.WORLD.addEntity(self.firelord)
        self.hero = Globals.HERO
        self.hero.image = self.hero.IMAGES[1]
        Globals.WORLD.addEntity(self.hero)
        self.Timer = 0

    def update(self, time):
        Globals.WORLD.background(Globals.SCREEN)
        Globals.WORLD.dr(Globals.SCREEN)
        Globals.WORLD.update(self.firelord)
        Dialogue = DB.Dialogue_box('cutscene7_dialogue.txt')
        while self.Timer < 20:
            Globals.WORLD.background(Globals.SCREEN)
            Globals.WORLD.dr(Globals.SCREEN)
            Globals.WORLD.update(self.firelord)
            self.Timer += 1
        if self.Timer == 25:
            while Dialogue.isOpen:
                Dialogue.update()
        while self.Timer < 200 and self.Timer > 30:
            key = PG.event.get()
            for event in key:
                if event.type == PG.KEYDOWN or event.type == PG.JOYBUTTONDOWN:
                    self.Timer = 651
            Globals.WORLD.background(Globals.SCREEN)
            Globals.WORLD.dr(Globals.SCREEN)
            Globals.WORLD.update(self.firelord)
            set_timer = self.Timer % 4
            if set_timer == 0:
                self.firelord.rect.centerx -= 3
                self.firelord.update_image(self.firelord.image_tracker*4+1, False, True)
                self.elder.rect.centerx -= 3
                self.elder.update_image(self.elder.image_tracker*4+1, False, True)
            self.Timer += 1
            PDI.flip()
        while self.Timer < 450 and self.Timer > 30:
            key = PG.event.get(PG.KEYDOWN)
            for event in key:
                if event.type == PG.KEYDOWN:
                    self.Timer = 651
            Globals.WORLD.background(Globals.SCREEN)
            Globals.WORLD.dr(Globals.SCREEN)
            Globals.WORLD.update(self.firelord)
            set_timer = self.Timer % 4
            if set_timer == 0:
                self.firelord.rect.centery += 3
                self.firelord.update_image(self.firelord.image_tracker*4, False, True)
                self.elder.rect.centerx -= 3
                self.elder.update_image(self.elder.image_tracker*4+1, False, True)
            self.Timer += 1
            PDI.flip()
        while self.Timer < 650 and self.Timer > 30:
            key = PG.event.get()
            for event in key:
                if event.type == PG.KEYDOWN or event.type == PG.JOYBUTTONDOWN:
                    self.Timer = 651
            Globals.WORLD.background(Globals.SCREEN)
            Globals.WORLD.dr(Globals.SCREEN)
            Globals.WORLD.update(self.firelord)
            set_timer = self.Timer % 4
            if set_timer == 0:
                self.firelord.rect.centery += 3
                self.firelord.update_image(self.firelord.image_tracker*4, False, True)
                self.elder.rect.centery -= 3
                self.elder.update_image(self.elder.image_tracker*4+3, False, True)
            self.Timer += 1
            PDI.flip()
        if self.Timer > 651:
            self.endScene()
        self.Timer += 1

    def endScene(self):
        fpsClock = PT.Clock()
        DURATION = 2000.0
        start_time = PT.get_ticks()
        ratio = 0.0
        while ratio < 1.0:
            current_time = PT.get_ticks()
            ratio = (current_time - start_time)/DURATION
            if ratio > 1.0:
                ratio = 1.0
            value = int(255*ratio)
            fade_color = PC.Color(0, 0, 0, 0)
            fade_color.a = value
            # PD.rect(Globals.SCREEN, fade_color, (0,0,400,300))
            surf = PG.Surface((800, 600))
            surf.set_alpha(value)
            surf.fill((0, 0, 0))
            Globals.SCREEN.blit(surf, (0, 0))
            PDI.flip()
            fpsClock.tick(60)
        PX.stop()    
        Globals.ISMAINMENU = False
        Globals.STATE = GS.LevelOne()

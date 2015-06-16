import sys as SYS
import random
import time
import pygame as PG
import os as OS
import pygame.display as PD
import pygame.event as PE
import pygame.font as PF
import pygame.time as PT
import pygame.sprite as PS
import pygame.color as PC
import pygame.mixer as PX
import pygame.image as PI
import DialogueBox as DB
import Player
import Enemy
import Setup
import smooth
import LevelOne
import LoseScreen
import cutscene1
import item
import NPC
from Screen import BaseState as State
from Screen import Globals
import WinScreen
import Score as Score
Dir = OS.getcwd()
sword_in_stone_image = OS.path.join(OS.path.dirname(Dir),
                                    'Images/sword_in_stone.png')
stone_mound_image = OS.path.join(OS.path.dirname(Dir), 'Images/stoneMound.png')


RUNNING = True
SCREEN = None
WIDTH = None
HEIGHT = None
TILES = {}
WORLD = None
CAMERA = None
LOSE_TIME = 1000
PROJECTILE_COUNTER = 50
SWORD_COUNTER = 50
levelTwoEvents = [True, True]



class LevelTwo(State):
    FADEINTIME = 1.0
    FADEOUTTIME = 0.2
    CYCLE = 1.0
    detection = False

    def __init__(self):
        State.__init__(self)
        Globals.WORLD.clear()
        Globals.WORLD = smooth.World("map2.txt")
        self.time = 0.0
        self.alpha = 255
        Globals.WORLD.camera = smooth.Camera \
            (smooth.complex_camera, \
             Globals.WORLD, \
             Globals.WORLD.realwidth, Globals.WORLD.realheight)
        # Declare sprite groups
        self.enemyGroup = PS.Group()  # enemy sprite group
        self.enemyProjectileGroup = PS.Group()  # projectile sprite group
        self.heroGroup = PS.Group()  # hero sprite group
        self.heroProjectileGroup = PS.Group()  # projectile sprite group
        self.heroSword = PS.Group()  # sword sprite group
        self.items = PS.Group()  # items to be picked up
        self.npcGroup = PS.Group()  # non-player character group
        # Done declaring sprite groups
        self.wait = 0
        # create firewood item
        # self.items.add(self.firewood)
        # Globals.WORLD.addEntity(self.items)

        '''
        for i in range(5):

            enemy = Enemy.Enemy(random.randint(0,  Globals.WORLD.realwidth), random.randint(0, Globals.WORLD.realheight),True)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
        '''
        # for i in range(Setup.NUM_VILLAINS):
        #     enemy = Enemy.Enemy()
        #     self.enemyGroup.add(enemy)
        #     Globals.WORLD.addEntity(enemy)
        # for i in range(Setup.NUM_VILLAINS):
        #     npc = NPC.NPC()
        #     self.npcGroup.add(npc)
        #     Globals.WORLD.addEntity(npc)
        self.heroGroup = PS.Group()
        self.hero = Globals.HERO
        self.startTime = time.time()
        self.lastTime = 0
        self.surf2 = PG.Surface((800, 600))
        self.surf = Globals.FONT.render(str(LOSE_TIME), True, (0, 0, 0))
        self.score = 50
        self.sword_timer = 0
        self.firstTime = True
        if levelTwoEvents[1] == True:
            self.hero.rect.center = (32, 26*32)
            self.heroGroup.add(self.hero)
            Globals.WORLD.addEntity(self.hero)
            self.sword_in_stone = item.Item(54*Setup.PIXEL_SIZE, 26*Setup.PIXEL_SIZE, sword_in_stone_image)
            Globals.WORLD.addEntity(self.sword_in_stone)
            self.items.add(self.sword_in_stone)
        else:
            self.sword_in_stone = item.Item(54*Setup.PIXEL_SIZE, 26*Setup.PIXEL_SIZE, stone_mound_image)
            Globals.WORLD.addEntity(self.sword_in_stone)
            self.items.add(self.sword_in_stone)
            self.hero.rect.center = (51*32, 26*32)
            self.heroGroup.add(self.hero)
            Globals.WORLD.addEntity(self.hero)
            enemy = Enemy.Enemy(48*32, 24*32, True, 0, 0)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(50*32, 28*32, True, 0, 0)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(384, 832, True, 0, 0)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(384, 864, True, 0, 0)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(1472, 576, True, 0, 0)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(1472, 1120, True, 0, 0)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(640, 576, True, 0, 0)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(640, 1120, True, 0, 0)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(1280, 224, True, 0, 0)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(1280, 1472, True, 0, 0)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)

    def render(self):
        Globals.HUD.update()

    def update(self, newTime):
        self.surf2.fill((0, 0, 0))
        self.surf2.set_alpha(self.alpha)
        if self.alpha > 0:
            self.alpha -= 5
        self.time = self.time + newTime

        self.currTime = time.time()  # Current time
        self.elapsedTime = int(self.currTime - self.startTime)  # elapsed time
        self.score = LOSE_TIME - self.elapsedTime
        Globals.HUD.updateTime(self.score)
        if not self.elapsedTime == self.lastTime:
            self.surf = Globals.FONT.render(str(self.score), True, (0, 0, 0))
        self.lastTime = self.elapsedTime
        if self.elapsedTime > LOSE_TIME:
            Globals.SCREEN.fill(Setup.BLACK)
            Globals.STATE = LoseScreen.LoseScreen(self.score)
        if self.time > self.CYCLE:
            self.time = 0.0
        if self.time < 0.33:
            image_counter = 0
        elif self.time < 0.66:
            image_counter = 1
        else:
            image_counter = 2
        Globals.WORLD.background(Globals.SCREEN)
        Globals.WORLD.dr(Globals.SCREEN)
        Globals.WORLD.update(self.hero)
        # self.group.draw(Globals.SCREEN)
        #Globals.SCREEN.blit(self.surf, (500, 100))  # Drawing clock
        #Globals.SCREEN.blit(self.surf2, (0, 0))
        playerX = self.hero.rect.centerx
        playerY = self.hero.rect.centery
        key = PG.key.get_pressed()
        for event in PE.get():
            if event.type == PG.QUIT:
                Globals.RUNNING = False
        if key[PG.K_1]:
            Globals.STATE = LevelOne.LevelOne()
        if key[PG.K_ESCAPE]:
            Globals.RUNNING = False
        elif key[PG.K_w]:
            self.hero.speed = 8.0
        elif not key[PG.K_w]:
            self.hero.speed = 3.0
        # Projectile Logic
        # if key[PG.K_r]:
        #    if self.projectile_counter % PROJECTILE_COUNTER == 0:
        #        temp = self.hero.shoot_projectile(Globals.STATE.heroProjectileGroup)
        #        Globals.WORLD.addEntity(temp)
        #    self.projectile_counter += 1
        # elif not key[PG.K_r]:
        #    self.projectile_counter = 0

        # Sword Logic
        if key[PG.K_e] and not Player.events[4]:
            if self.currTime - self.sword_timer >= 0:
                self.hero.attacking = True
        elif not key[PG.K_e]:
            self.hero.attacking = False
        elif key[PG.K_SPACE]:
            pass
        if key[PG.K_DOWN] and not key[PG.K_LEFT] \
                and not key[PG.K_RIGHT] and not key[PG.K_UP]:
            self.hero.movedown(image_counter)
        elif key[PG.K_LEFT] and not key[PG.K_RIGHT] \
                and not key[PG.K_UP] and not key[PG.K_DOWN]:
            self.hero.moveleft(image_counter)
        elif key[PG.K_RIGHT] and not key[PG.K_UP] \
                and not key[PG.K_LEFT] and not key[PG.K_DOWN]:
            self.hero.moveright(image_counter)
        elif key[PG.K_UP] and not key[PG.K_RIGHT] \
                and not key[PG.K_LEFT] and not key[PG.K_DOWN]:
            self.hero.moveup(image_counter)
        else:
            self.hero.moveidle(image_counter)
        playerX = self.hero.rect.centerx
        playerY = self.hero.rect.centery
        self.heroGroup.update(self.enemyGroup, self.npcGroup, smooth.wallMap
                              [playerX/(Setup.GRID_SIZE *
                                        Setup.PIXEL_SIZE),
                               playerY/(Setup.GRID_SIZE *
                                        Setup.PIXEL_SIZE)],
                              self)
        # joystick controls
        '''
        if PJ.get_count() > 0:
            if joystick.get_axis(2) > 0.1:
                self.hero.speed = 8.0
            if joystick.get_button(2) and not Player.events[4]:
                if self.currTime - self.sword_timer >= 0:
                    self.hero.attacking = True
            elif joystick.get_button(0):
                pass
            if joystick.get_axis(1) > 0.1:
                self.hero.movedown(image_counter)
            elif joystick.get_axis(0) < -0.1:
                self.hero.moveleft(image_counter)
            elif joystick.get_axis(0) > 0.1:
                self.hero.moveright(image_counter)
            elif joystick.get_axis(1) < -0.1:
                self.hero.moveup(image_counter)
            else:
                self.hero.moveidle(image_counter)
            playerX = self.hero.rect.centerx
            playerY = self.hero.rect.centery
            self.heroGroup.update(self.enemyGroup, self.npcGroup, smooth.wallMap
                                  [playerX/(Setup.GRID_SIZE *
                                            Setup.PIXEL_SIZE),
                                   playerY/(Setup.GRID_SIZE *
                                            Setup.PIXEL_SIZE)],
                                  self)
        '''
        for enemy in self.enemyGroup:
            enemyX = enemy.rect.centerx
            enemyY = enemy.rect.centery
            enemy.update(smooth.wallMap
                               [enemyX/(Setup.GRID_SIZE * Setup.PIXEL_SIZE),
                                enemyY/(Setup.GRID_SIZE * Setup.PIXEL_SIZE)], self.hero)
        self.npcGroup.update(smooth.wallMap
                               [playerX/(Setup.GRID_SIZE * Setup.PIXEL_SIZE),
                                playerY/(Setup.GRID_SIZE * Setup.PIXEL_SIZE)])

        # Enemy projectiles
        # self.enemyProjectileGroup.update(self.hero)

        for enemy in self.enemyGroup:
            self.heroProjectileGroup.update(enemy)
            self.heroSword.update(self.hero, enemy)
        for i in self.items:
            if Player.events[4]:
                i.pickedUp(self.hero)
                if i.isPickedUp:
                    Globals.STATE = LevelTwoCut()

        if Player.events[5] == False:
            Globals.STATE = cutscene1.Cutscene2()

        if self.hero.health <= 0:
                Globals.STATE = LoseScreen.LoseScreen(0)
        Globals.HUD.updateHealth()

    def currentScore(self):
        return self.score


class LevelTwoCut(State):

    def __init__(self):
        State.__init__(self)
        self.rect = PG.Rect(0, 500, 800, 100)
        self.display = PG.Surface((self.rect.width, self.rect.height))
        self.display.fill((0, 0, 0))
        Globals.WORLD.clear()
        Globals.WORLD = smooth.World("map2.txt")
        Globals.WORLD.camera = smooth.Camera(smooth.complex_camera,
                                             Globals.WORLD,
                                             Globals.WORLD.realwidth,
                                             Globals.WORLD.realheight)
        self.npc1 = Enemy.Enemy(451, 752, True)
        self.npc2 = Enemy.Enemy(451, 752, True)
        self.npc1.image = self.npc1.IMAGES[2]
        self.npc2.image = self.npc2.IMAGES[6]
        self.npc1.image_tracker = 2
        self.npc2.image_tracker = 0
        self.npc1.rect.center = (47*32, 25*32)
        self.npc2.rect.center = (47*32, 27*32)
        self.Timer = 0
        self.hero = Globals.HERO
        self.hero.rect.center = (51*32, 26*32)
        self.sword_in_stone = item.Item(54*Setup.PIXEL_SIZE, 26*Setup.PIXEL_SIZE, sword_in_stone_image)
        Globals.WORLD.addEntity(self.sword_in_stone)

    def update(self, time):
        Globals.WORLD.background(Globals.SCREEN)
        Globals.WORLD.dr(Globals.SCREEN)
        Globals.WORLD.update(self.npc1)
        if self.Timer == 0:
            Globals.WORLD.addEntity(self.hero)
            Globals.WORLD.addEntity(self.npc1)
            Globals.WORLD.addEntity(self.npc2)
        while self.Timer < 150:
            key = PG.event.get(PG.KEYDOWN)
            for event in key:
                if event.type == PG.KEYDOWN:
                    self.Timer = 181
            Globals.WORLD.background(Globals.SCREEN)
            Globals.WORLD.dr(Globals.SCREEN)
            Globals.WORLD.update(self.npc1)
            set_timer = self.Timer % 10
            if set_timer == 0:
                self.npc1.rect.centerx += 4
                self.npc2.rect.centerx += 4
                self.npc1.update_image(self.npc1.image_tracker*4+2)
                self.npc2.update_image(self.npc2.image_tracker*4+2)
            self.Timer += 1
            PD.flip()
            self.hero.image = self.hero.IMAGES[1]
        if self.Timer == 176:
            Dialogue = DB.Dialogue_box("cutscene5_dialogue.txt")
            while Dialogue.isOpen:
                Dialogue.update()
        while self.Timer < 200 and self.Timer > 177:
            key = PG.event.get(PG.KEYDOWN)
            for event in key:
                if event.type == PG.KEYDOWN:
                    self.Timer = 201
            Globals.WORLD.background(Globals.SCREEN)
            Globals.WORLD.dr(Globals.SCREEN)
            Globals.WORLD.update(self.npc1)
            set_timer = self.Timer % 4
            if set_timer == 0:
                self.hero.rect.centerx += 3
                self.hero.update_image(self.hero.image_tracker*4+2, True)
            self.Timer += 1
            PD.flip()
        if self.Timer > 201:
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
            PD.flip()
            fpsClock.tick(60)
        levelTwoEvents[1] = False
        Player.events[4] = False
        self.stone_mound = item.Item(54*Setup.PIXEL_SIZE, 26*Setup.PIXEL_SIZE, stone_mound_image)
        Globals.WORLD.addEntity(self.stone_mound)
        Globals.STATE = LevelTwo()

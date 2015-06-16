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
import LevelFour
import cutscene1
import item
import NPC
from Screen import BaseState as State
from Screen import Globals
import WinScreen
import Score as Score
Dir = OS.getcwd()
wagon_image_path = OS.path.join(OS.path.dirname(Dir),
                                    'Images/Wagon.png')
firelord_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/FireLord.png')

# earth_warrior_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/EarthWarrior.png')


RUNNING = True
SCREEN = None
WIDTH = None
HEIGHT = None
TILES = {}
WORLD = None
CAMERA = None
LOSE_TIME = 1000
PROJECTILE_COUNTER = 50
SWORD_COUNTER = .5
NUM_OPTIONAL = 10


class LevelThree(State):
    FADEINTIME = 1.0
    FADEOUTTIME = 0.2
    CYCLE = 1.0
    detection = False
    phase = [False, False, False, False]

    def __init__(self):
        State.__init__(self)
        Globals.WORLD.clear()
        Globals.WORLD = smooth.World("map3.txt")
        self.time = 0.0
        self.alpha = 255
        self.hero = Globals.HERO
        Globals.WORLD.camera = smooth.Camera \
            (smooth.complex_camera, \
             Globals.WORLD, \
             Globals.WORLD.realwidth, Globals.WORLD.realheight)
        # Declare sprite groups
        self.enemyGroup = PS.Group()  # enemy sprite group
        self.optionalGroup = PS.Group()  # enemies that don't need to be killed
        self.allEnemies = PS.Group()  # both enemyGroup and optionalGroup

        self.enemyProjectileGroup = PS.Group()  # projectile sprite group
        self.heroGroup = PS.Group()  # hero sprite group
        self.heroProjectileGroup = PS.Group()  # projectile sprite group
        self.heroSword = PS.Group()  # sword sprite group
        self.items = PS.Group()  # items to be picked up
        self.wagonGroup = PS.Group()  # non-player character group
        # Done declaring sprite groups
        self.heroGroup = PS.Group()

        self.startTime = time.time()
        self.lastTime = 0
        self.surf2 = PG.Surface((800, 600))
        self.surf = Globals.FONT.render(str(LOSE_TIME), True, (0, 0, 0))
        self.score = 50
        self.hero.rect.center = (5*32, 32)
        self.heroGroup.add(self.hero)
        Globals.WORLD.addEntity(self.hero)
        for i in range(len(LevelThree.phase)):
            LevelThree.phase[i] = False
        self.wait = 0
        self.w1 = NPC.Wagon(wagon_image_path, 20, 11)
        self.w2 = NPC.Wagon(wagon_image_path, 16, 11)
        self.w3 = NPC.Wagon(wagon_image_path, 12, 11)
        self.w4 = NPC.Wagon(wagon_image_path, 8, 11)
        self.w5 = NPC.Wagon(wagon_image_path, 4, 11)
        Globals.WORLD.addEntity(self.w1)
        Globals.WORLD.addEntity(self.w2)
        Globals.WORLD.addEntity(self.w3)
        Globals.WORLD.addEntity(self.w4)
        Globals.WORLD.addEntity(self.w5)
        self.wagonGroup.add(self.w1)
        self.wagonGroup.add(self.w2)
        self.wagonGroup.add(self.w3)
        self.wagonGroup.add(self.w4)
        self.wagonGroup.add(self.w5)
        self.projectile_timer = 0
        self.sword_timer = 0
        # self.v1 = NPC.NPC(villager1_image_path)
        # Create non-objective enemies
        for i in range(NUM_OPTIONAL):
            x = random.randint(12, 130)
            y = random.randint(24, 38)
            if random.randint(0, 2) == 0:  # 33% chance to be melee
                attack_type = 0
            else:
                attack_type = 1
            if random.randint(0, 1) == 0:  # 50% chance of being air/earth
                nation = 1
            else:
                nation = 2

            enemy = Enemy.Enemy(x * Setup.PIXEL_SIZE, y * Setup.PIXEL_SIZE, True, attack_type, nation)
            self.optionalGroup.add(enemy)
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
        if key[PG.K_ESCAPE]:
            Globals.RUNNING = False
        if key[PG.K_w]:
            self.hero.speed = 8.0
        elif not key[PG.K_w]:
            self.hero.speed = 3.0

        # Sword Logic
        if key[PG.K_e] and not Player.events[4]:
            if self.currTime - self.sword_timer >= 1:
                self.hero.attacking = True
                self.sword_timer = self.currTime
            # else:
                # self.sword_timer += 0.1
        elif not key[PG.K_e]:
            self.hero.attacking = False
            # self.sword_timer = 0

        # Projectile Logic
        if key[PG.K_r]:
            if (self.currTime - self.projectile_timer) >= 2:
                temp = self.hero.shoot_projectile(Globals.STATE.heroProjectileGroup)
                Globals.WORLD.addEntity(temp)
                self.projectile_timer = self.currTime
                Globals.HUD.updateCooldown()
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
        # joystick controls
        '''
        if PJ.get_count() > 0:
            if joystick.get_axis(2) > 0.1:
                self.hero.speed = 8.0

            # Sword Logic
            if joystick.get_button(2) and not Player.events[4]:
                if self.currTime - self.sword_timer >= 1:
                    self.hero.attacking = True
                    self.sword_timer = self.currTime
                #else:
                    #self.sword_timer += 0.1
            elif not key[PG.K_e]:
                self.hero.attacking = False
                #self.sword_timer = 0

            # Projectile Logic
            if joystick.get_button(1):
                if (self.currTime - self.projectile_timer) >= 2:
                    temp = self.hero.shoot_projectile(Globals.STATE.heroProjectileGroup)
                    Globals.WORLD.addEntity(temp)
                    self.projectile_timer = self.currTime
                    Globals.HUD.updateCooldown()
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
        '''
        playerX = self.hero.rect.centerx
        playerY = self.hero.rect.centery

        self.allEnemies.add(self.enemyGroup)
        self.allEnemies.add(self.optionalGroup)

        self.heroGroup.update(self.allEnemies, self.wagonGroup, smooth.wallMap[playerX/(Setup.GRID_SIZE * Setup.PIXEL_SIZE), playerY/(Setup.GRID_SIZE*Setup.PIXEL_SIZE)], self)
        self.allEnemies.update(smooth.wallMap[playerX/(Setup.GRID_SIZE * Setup.PIXEL_SIZE), playerY/(Setup.GRID_SIZE * Setup.PIXEL_SIZE)], self.hero)
        self.enemyProjectileGroup.update(self.heroGroup)
        if not self.allEnemies:
            self.heroProjectileGroup.update()
        else:
            self.heroProjectileGroup.update(self.allEnemies)
            self.heroSword.update(self.hero, self.allEnemies)
        # Direction changes
        for wagon in self.wagonGroup:
            if wagon.rect.centerx == 26 * Setup.PIXEL_SIZE and wagon.rect.centery == 11 * Setup.PIXEL_SIZE:
                wagon.direction = 0
            elif wagon.rect.centerx == 26 * Setup.PIXEL_SIZE and wagon.rect.centery == 30 * Setup.PIXEL_SIZE:
                wagon.direction = 2
            elif wagon.rect.centerx == 106 * Setup.PIXEL_SIZE and wagon.rect.centery == 30 * Setup.PIXEL_SIZE:
                wagon.direction = 3
            elif wagon.rect.centerx == 106 * Setup.PIXEL_SIZE and wagon.rect.centery == 21 * Setup.PIXEL_SIZE:
                wagon.direction = 2
        # First stall position for caravan
        if self.w1.rect.centerx == 50 * Setup.PIXEL_SIZE and not LevelThree.phase[0]:
            LevelThree.phase[0] = True
            for wagon in self.wagonGroup:
                wagon.isBroken = True
        # Second stall position for caravan
        if self.w1.rect.centerx == 90 * Setup.PIXEL_SIZE and not LevelThree.phase[1]:
            LevelThree.phase[1] = True
            for wagon in self.wagonGroup:
                wagon.isBroken = True
        # Third stall position for caravan
        if self.w1.rect.centerx == 120 * Setup.PIXEL_SIZE and not LevelThree.phase[2]:
            LevelThree.phase[2] = True
            for wagon in self.wagonGroup:
                wagon.isBroken = True
        # Create First wave of enemies
        if self.w1.rect.centerx == 40 * Setup.PIXEL_SIZE and not LevelThree.phase[0]:
            # Add enemies
            enemy = Enemy.Enemy(57 * Setup.PIXEL_SIZE, 30 * Setup.PIXEL_SIZE, True, 0, 2)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(59 * Setup.PIXEL_SIZE, 30 * Setup.PIXEL_SIZE, True, 1, 1)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(58 * Setup.PIXEL_SIZE, 32 * Setup.PIXEL_SIZE, True, 0, 2)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(59 * Setup.PIXEL_SIZE, 33 * Setup.PIXEL_SIZE, True, 1, 2)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(59 * Setup.PIXEL_SIZE, 34 * Setup.PIXEL_SIZE, True, 0, 1)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
        # Create Second wave of enemies
        if self.w1.rect.centerx == 80 * Setup.PIXEL_SIZE and not LevelThree.phase[1]:
            # Add enemies
            enemy = Enemy.Enemy(98 * Setup.PIXEL_SIZE, 30 * Setup.PIXEL_SIZE, True, 1, 2)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(95 * Setup.PIXEL_SIZE, 30 * Setup.PIXEL_SIZE, True, 1, 1)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(100 * Setup.PIXEL_SIZE, 32 * Setup.PIXEL_SIZE, True, 0, 1)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(99 * Setup.PIXEL_SIZE, 33 * Setup.PIXEL_SIZE, True, 1, 1)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(98 * Setup.PIXEL_SIZE, 34 * Setup.PIXEL_SIZE, True, 0, 1)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
        # Create Third wave of enemies
        if self.w1.rect.centerx == 110 * Setup.PIXEL_SIZE and not LevelThree.phase[2]:
            # Add enemies

            enemy = Enemy.Enemy(127 * Setup.PIXEL_SIZE, 22 * Setup.PIXEL_SIZE, True, 1, 2)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(129 * Setup.PIXEL_SIZE, 22 * Setup.PIXEL_SIZE, True, 1, 1)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(128 * Setup.PIXEL_SIZE, 20 * Setup.PIXEL_SIZE, True, 1, 1)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(129 * Setup.PIXEL_SIZE, 22 * Setup.PIXEL_SIZE, True, 0, 2)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
            enemy = Enemy.Enemy(128 * Setup.PIXEL_SIZE, 20 * Setup.PIXEL_SIZE, True, 0, 1)

            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
        if LevelThree.phase[0] == True and LevelThree.phase[1] == False:
            # First stop
            if self.enemyGroup:
                # While enemies are still alive
                pass
            else:
                for wagon in self.wagonGroup:
                    wagon.isBroken = False

        if LevelThree.phase[1] == True and LevelThree.phase[2] == False:
            # Second stop
            if self.enemyGroup:
                # While enemies are still alive
                pass
            else:
                for wagon in self.wagonGroup:
                    wagon.isBroken = False
        if LevelThree.phase[2] == True and LevelThree.phase[3] == False:
            # Third stop
            if self.enemyGroup:
                # While enemies are still alive
                pass
            else:
                for wagon in self.wagonGroup:
                    wagon.isBroken = False
                LevelThree.phase[3] = True  # Allowed to proceed to final level


        if LevelThree.phase[3] == True:
            if playerX >= 133 * Setup.PIXEL_SIZE:
                if playerY > 19 * Setup.PIXEL_SIZE and playerY < 25 * Setup.PIXEL_SIZE:
                    # TODO: Implement cutscene then go to level 4
                    Player.events[8] = False
                    Globals.STATE = LevelThreeCut()
        if PS.spritecollideany(self.hero, self.wagonGroup) == None:
            self.wagonGroup.update()
        if self.hero.health <= 0:
                Globals.STATE = LoseScreen.LoseScreen(0)

    def currentScore(self):
        return self.score


class LevelThreeCut(State):

    def __init__(self):
        State.__init__(self)
        self.rect = PG.Rect(0, 500, 800, 100)
        self.display = PG.Surface((self.rect.width, self.rect.height))
        self.display.fill((0, 0, 0))
        Globals.WORLD.clear()
        Globals.WORLD = smooth.World("map3.txt")
        Globals.WORLD.camera = smooth.Camera(smooth.complex_camera,
                                             Globals.WORLD,
                                             Globals.WORLD.realwidth,
                                             Globals.WORLD.realheight)
        self.hero = Globals.HERO
        self.hero.image = self.hero.IMAGES[1]
        Globals.WORLD.addEntity(self.hero)
        # Initializing fire lord
        self.firelord = NPC.NPC(firelord_image_path)
        self.firelord.image = self.firelord.IMAGES[6]
        self.firelord.rect.center = (132 * Setup.PIXEL_SIZE, self.hero.rect.centery)
        Globals.WORLD.addEntity(self.firelord)
        self.Timer = 0

    def update(self, time):
        Globals.WORLD.background(Globals.SCREEN)
        Globals.WORLD.dr(Globals.SCREEN)
        Globals.WORLD.update(self.hero)
        Dialogue = DB.Dialogue_box('cutscene8_dialogue.txt')
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
            self.Timer += 1
            PD.flip()
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
            self.Timer += 1
            PD.flip()
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
            self.Timer += 1
            PD.flip()
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
            PD.flip()
            fpsClock.tick(60)
        Globals.STATE = LevelFour.LevelFour()

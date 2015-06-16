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
import Projectile
from Screen import BaseState as State
from Screen import Globals
import WinScreen
import Score as Score
Dir = OS.getcwd()
wagon_image_path = OS.path.join(OS.path.dirname(Dir),
                                    'Images/Wagon.png')
flame_pillar_path = OS.path.join(OS.path.dirname(Dir), 'Images/flamePillar.png')
# earth_warrior_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/EarthWarrior.png')
firelord_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/FireLord.png')
flame_sound = OS.path.join(OS.path.dirname(Dir), 'Sounds/flameSound.wav')

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
NUM_OPTIONAL = 15


class LevelFour(State):
    FADEINTIME = 1.0
    FADEOUTTIME = 0.2
    CYCLE = 1.0
    detection = False
    phase = [False, False, False, False]

    def __init__(self):
        PX.init()
        self.flameSound = PX.Sound(flame_sound)
        #self.flameSound.set_volume(Globals.VOLUME/200.0)

        State.__init__(self)
        Globals.WORLD.clear()
        Globals.WORLD = smooth.World("map4.txt")
        self.time = 0.0
        self.alpha = 255
        self.hero = Globals.HERO
        self.IMAGES = []
        self.load_special()
        Globals.WORLD.camera = smooth.Camera \
            (smooth.complex_camera, \
             Globals.WORLD, \
             Globals.WORLD.realwidth, Globals.WORLD.realheight)
        # Declare sprite groups
        self.bossGroup = PS.Group()  # boss sprite group
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
        for i in range(1):
            if random.randint(0, 2) == 0:  # 33% chance to be melee
                attack_type = 0
            else:
                attack_type = 1
            if random.randint(0, 1) == 0:  # 50% chance of being air/earth
                nation = 1
            else:
                nation = 2
            enemy = Enemy.Boss(10 * Setup.PIXEL_SIZE, 10 * Setup.PIXEL_SIZE)
            self.bossGroup.add(enemy)
            self.allEnemies.add(enemy)
            self.enemyGroup.add(enemy)
            Globals.WORLD.addEntity(enemy)
        self.startTime = time.time()
        self.lastTime = 0
        self.surf2 = PG.Surface((800, 600))
        self.surf = Globals.FONT.render(str(LOSE_TIME), True, (0, 0, 0))
        self.score = 50
        self.hero.rect.center = (1 * Setup.PIXEL_SIZE, 27 * Setup.PIXEL_SIZE)
        self.heroGroup.add(self.hero)
        Globals.WORLD.addEntity(self.hero)
        self.wait = 0
        self.projectile_timer = 0
        self.sword_timer = 0
        self.special = None
        self.special_timer = 0
        self.special_image = 0
        self.abilityStart = 0
        self.startedAbility = False

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
        elif not key[PG.K_e]:
            self.hero.attacking = False

        # Projectile Logic
        if key[PG.K_r]:
            if (self.currTime - self.projectile_timer) >= 2:
                temp = self.hero.shoot_projectile(Globals.STATE.heroProjectileGroup)
                Globals.WORLD.addEntity(temp)
                self.projectile_timer = self.currTime
                Globals.HUD.updateCooldown()
        if key[PG.K_t]:
            if (self.currTime - self.special_timer) >= 10 and not self.startedAbility:
                self.special_timer = self.currTime
                self.abilityStart = 0
                self.startedAbility = True
                Globals.HUD.updateCooldown2()

            if self.abilityStart == 0:
                self.abilityStart = self.currTime
            if self.startedAbility:
                self.special = PG.Rect(0, 0, 1, 1)
                distance = (self.currTime - self.abilityStart)*100
                if distance > 300:
                    distance = 300
                if self.hero.direction == "moveup":  # up
                    self.special.center = (self.hero.rect.centerx, int(self.hero.rect.centery-distance))
                elif self.hero.direction == "moveright":  # right
                    self.special.center = (int(self.hero.rect.centerx+distance), self.hero.rect.centery)
                elif self.hero.direction == "movedown":  # down
                    self.special.center = (self.hero.rect.centerx, int(self.hero.rect.centery+distance))
                elif self.hero.direction == "moveleft":  # left
                    self.special.center = (int(self.hero.rect.centerx-distance), self.hero.rect.centery)

                self.special = Globals.WORLD.camera.apply(self.special)
                PG.draw.circle(Globals.SCREEN, (255, 0, 0),  self.special.center, 3)
        if not key[PG.K_t]:
            if self.startedAbility:

                distance = (self.currTime - self.abilityStart)*100
                if distance < 300:
                    Globals.STATE.heroProjectileGroup.add(Projectile.Special(self.hero, self.hero.direction, distance))
                else:
                    Globals.STATE.heroProjectileGroup.add(Projectile.Special(self.hero, self.hero.direction, 300))
                Globals.SCREEN.blit(self.IMAGES[self.special_image % 6], (self.special.left-32, self.special.top-32))
                self.special_image += 1
            if self.special_image != 0:
                Globals.SCREEN.blit(self.IMAGES[self.special_image%6], (self.special.left-32, self.special.top-32))
                self.special_image = (self.special_image + 1) % 12   
                self.flameSound.play() 
            self.startedAbility = False  
            self.abilityStart = 0  
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
        #joystick controls
        '''
        if PJ.get_count() > 0:
            if joystick.get_axis(2) > 0.1:
                self.hero.speed = 8.0

            # Sword Logic
            if joystick.get_button(2) and not Player.events[4]:
                if self.currTime - self.sword_timer >= 1:
                    self.hero.attacking = True
                    self.sword_timer = self.currTime
            elif not key[PG.K_e]:
                self.hero.attacking = False

            # Projectile Logic
            if joystick.get_button(1):
                if (self.currTime - self.projectile_timer) >= 2:
                    temp = self.hero.shoot_projectile(Globals.STATE.heroProjectileGroup)
                    Globals.WORLD.addEntity(temp)
                    self.projectile_timer = self.currTime
                    Globals.HUD.updateCooldown()
            if joystick.get_button(3):
                if (self.currTime - self.special_timer) >= 10 and not self.startedAbility :
                    self.special_timer = self.currTime
                    self.abilityStart = 0
                    self.startedAbility = True
                    Globals.HUD.updateCooldown2()
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

        if self.hero.health <= 0:
            Globals.STATE = LoseScreen.LoseScreen(0)
        if len(self.bossGroup) == 0:
            Globals.STATE = LevelFourCut()
                    
    def currentScore(self):
        return self.score

    def load_special(self):
        special_sheet = PI.load(flame_pillar_path).convert_alpha()
        key = special_sheet.get_at((0, 0))
        for i in range(3):
            for j in range(2):
                surface = PG.Surface((64, 96)).convert()
                surface.set_colorkey(key)
                surface.blit(special_sheet, (0, 0), (i*64, j*96, 64, 96))
                self.IMAGES.append(surface)


class LevelFourCut(State):

    def __init__(self):
        print 'hi'
        State.__init__(self)
        self.rect = PG.Rect(0, 500, 800, 100)
        self.display = PG.Surface((self.rect.width, self.rect.height))
        self.display.fill((0, 0, 0))
        Globals.WORLD.clear()
        Globals.WORLD = smooth.World("map4.txt")
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
        self.firelord.rect.center = (self.hero.rect.centerx - 50, self.hero.rect.centery)
        Globals.WORLD.addEntity(self.firelord)
        self.Timer = 0

    def update(self, time):
        Globals.WORLD.background(Globals.SCREEN)
        Globals.WORLD.dr(Globals.SCREEN)
        Globals.WORLD.update(self.hero)
        Dialogue = DB.Dialogue_box('cutscene9_dialogue.txt')
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
        Globals.STATE = WinScreen.WinScreen(Globals.SCORE)

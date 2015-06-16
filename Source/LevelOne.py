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
import LevelTwo
import cutscene1
import LevelThree
import LevelFour
import Enemy
import Setup
import smooth
import LoseScreen
import item
import NPC
import HeadsUpDisplay
from Screen import BaseState as State
from Screen import Globals
import Score as Score
Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir),
                          'Images/brick_wall_tiled_perfect.png')
sheep_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/sheepSpriteSheet.png')
villager1_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/villager1.png')
villager2_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/villager2.png')
elder_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/elder.png')

firewood_image = OS.path.join(OS.path.dirname(Dir), 'Images/firewood.png')
cut_sound = OS.path.join(OS.path.dirname(Dir), 'Sounds/Cut.wav')
wood_sound = OS.path.join(OS.path.dirname(Dir), 'Sounds/Wood.wav')
mom_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/mom_sprite.png')
dad_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/dad.png')
elder_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/elder.png')
firelord_image_path = OS.path.join(OS.path.dirname(Dir), 'Images/FireLord.png')

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


class LevelOne(State):
    FADEINTIME = 1.0
    FADEOUTTIME = 0.2
    CYCLE = 1.0
    detection = False

    def __init__(self):
        Globals.ISMAINMENU = False
        Globals.ISLEVELONE = True
        State.__init__(self)
        smooth.loadtiles()
        Globals.WORLD.clear()
        Globals.WORLD = smooth.World("map.txt")
        Globals.WORLD.camera = smooth.Camera(smooth.complex_camera,
                                             Globals.WORLD,
                                             Globals.WORLD.realwidth,
                                             Globals.WORLD.realheight)

        PX.init()  # Initialize sound player
        self.cutSound = PX.Sound(cut_sound)
        self.woodSound = PX.Sound(wood_sound)
        self.cutSound.set_volume(Globals.VOLUME/200.0)
        self.woodSound.set_volume(Globals.VOLUME/200.0)
        # Globals.WORLD = smooth.World()
        self.time = 0.0
        self.alpha = 255
        # Globals.WORLD.camera = smooth.Camera \
        #    (smooth.complex_camera,
        #     Globals.WORLD,
        #     Globals.WORLD.realwidth, Globals.WORLD.realheight)

        # Declare sprite groups
        self.enemyGroup = PS.Group()  # enemy sprite group
        self.enemyProjectileGroup = PS.Group()  # projectile sprite group
        self.heroGroup = PS.Group()  # hero sprite group
        self.heroProjectileGroup = PS.Group()  # projectile sprite group
        self.heroSword = PS.Group()  # sword sprite group
        self.items = PS.Group()  # items to be picked up
        self.npcGroup = PS.Group()  # non-player character group
        # Done declaring sprite groups

        # create firewood item
        self.firewood = item.Item(32*6, 32*6, firewood_image)
        self.items.add(self.firewood)
        Globals.WORLD.addEntity(self.items)

        # for i in range(Setup.NUM_VILLAINS):
        #     enemy = Enemy.Enemy()
        #     self.enemyGroup.add(enemy)
        #     Globals.WORLD.addEntity(enemy)
        # for i in range(Setup.NUM_VILLAINS):
        #     npc = NPC.NPC()
        #     self.npcGroup.add(npc)
        #     Globals.WORLD.addEntity(npc)
        for i in range(4):
            sheep = NPC.Sheep(sheep_image_path, random.randint(70, 200), random.randint(70, 200))
            self.npcGroup.add(sheep)
            Globals.WORLD.addEntity(sheep)

        # Initializing village elder
        self.elder = NPC.NPC(elder_image_path)
        self.elder.rect.center = (71 * Setup.PIXEL_SIZE, 10 * Setup.PIXEL_SIZE)
        Globals.WORLD.addEntity(self.elder)

        # Initializing Villagers
        self.mom = NPC.NPC(mom_image_path)
        self.dad = NPC.NPC(dad_image_path)
        self.v1 = NPC.NPC(villager1_image_path)
        self.v2 = NPC.NPC(villager1_image_path)
        self.v3 = NPC.NPC(villager1_image_path)
        self.v4 = NPC.NPC(villager2_image_path)
        self.v5 = NPC.NPC(villager2_image_path)
        self.v6 = NPC.NPC(villager2_image_path)
        self.v1.rect.center = (26 * Setup.PIXEL_SIZE, 24 * Setup.PIXEL_SIZE)
        self.v4.rect.center = (27 * Setup.PIXEL_SIZE, 24 * Setup.PIXEL_SIZE)
        self.v2.rect.center = (32 * Setup.PIXEL_SIZE, 26 * Setup.PIXEL_SIZE)
        self.v5.rect.center = (33 * Setup.PIXEL_SIZE, 26 * Setup.PIXEL_SIZE)
        self.v3.rect.center = (43 * Setup.PIXEL_SIZE, 25 * Setup.PIXEL_SIZE)
        self.v6.rect.center = (68 * Setup.PIXEL_SIZE, 26 * Setup.PIXEL_SIZE)
        self.dad.rect.center = (451, 752)
        self.mom.rect.center = (451, 812)
        Globals.WORLD.addEntity(self.v1)
        Globals.WORLD.addEntity(self.v2)
        Globals.WORLD.addEntity(self.v3)
        Globals.WORLD.addEntity(self.v4)
        Globals.WORLD.addEntity(self.v5)
        Globals.WORLD.addEntity(self.v6)
        Globals.WORLD.addEntity(self.dad)
        Globals.WORLD.addEntity(self.mom)
        self.npcGroup.add(self.v1)
        self.npcGroup.add(self.v2)
        self.npcGroup.add(self.v3)
        self.npcGroup.add(self.v4)
        self.npcGroup.add(self.v5)
        self.npcGroup.add(self.v6)
        self.heroGroup = PS.Group()
        self.hero = Globals.HERO
        self.heroGroup.add(self.hero)
        Globals.WORLD.addEntity(self.hero)
        self.startTime = time.time()
        self.lastTime = 0
        self.surf2 = PG.Surface((800, 600))
        self.surf = Globals.FONT.render(str(LOSE_TIME), True, (0, 0, 0))
        self.score = 50
        self.firstTime = True
        self.static_score = 0
        self.spaceCounter = 0
        self.wait = 0
        # Fireball quest stuff
        self.fireballQuestCounter = 0
        self.hero = Globals.HERO
        self.heroProjectileGroup = PS.Group()  # projectile sprite group
        self.doneTime = 0

        # If player is returning from level 2 to level 1
        if not Player.events[5]:
            self.hero.rect.center = (85*32, 26*32)
            if Player.events[6]:
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
        else:  # if world is being initialized for first time
            self.hero.rect.center = (11*32, 2*32)
        self.cooldown_timer = 0

    def render(self):
        Globals.HUD.update()


    def update(self, newTime):
        
        
        '''
        if PJ.get_count() > 0:
            joystick_count = PJ.get_count()
            joystick = PJ.Joystick(joystick_count - 1)
            joystick.init()

            joystick_count = PJ.get_count()
            for i in range(joystick_count):
                joystick = PJ.Joystick(i)
                joystick.init()
                # print "Joystick {}".format(i)
            joystick = PJ.Joystick(0)
            joystick.init()
            name = joystick.get_name()
            # print "Joystick name: {}".format(name)
            axes = joystick.get_numaxes()
            # print "Number of axes: {}".format(axes)
            for i in range(axes):
                axis = joystick.get_axis(i)
                # print "Axis {} value: {:>6.3f}".format(i, axis)
            buttons = joystick.get_numbuttons()
            # print "Number of buttons: {}".format(buttons)
            for i in range(buttons):
                button = joystick.get_button(i)
                # print "Button {:>2} value: {}".format(i,button)
            hats = joystick.get_numhats()
            # print "Number of hats: {}".format(hats)
            for i in range(hats):
                hat = joystick.get_hat(i)
                # print "Hat {} value: {}".format(i, str(hat))
        else:
            joystick = None

        '''                               
        
        
        
        
        
        
        
        
        
        

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
        if key[PG.K_2]:
            for i in range(4):
                Player.events[i] = False
            Globals.STATE = LevelTwo.LevelTwo()
        if key[PG.K_3]:
            for i in range(8):
                Player.events[i] = False
            Globals.STATE = LevelThree.LevelThree()
        if key[PG.K_4]:
            for i in range(8):
                Player.events[i] = False
            Globals.STATE = LevelFour.LevelFour()
        if key[PG.K_ESCAPE]:
            Globals.RUNNING = False
        if key[PG.K_w]:
            self.hero.speed = 8.0
        elif not key[PG.K_w]:
            self.hero.speed = 3.0

        if key[PG.K_SPACE]:
            if self.spaceCounter == 0:
                self.spaceCounter += 1
                interactable = []
                list_interactable = []
                for sprite in Globals.WORLD.return_interactable():
                    interactable.append(sprite.rect)
                    list_interactable.append(sprite)
                index = self.hero.action_rect.collidelist(interactable)
                if index != -1:
                    # Play Cut Sound
                    self.cutSound.play()
                    tree = list_interactable[index]
                    if tree.health > 0:
                        tree.health -= 1
                    else:
                        tree.cutDown(smooth.wallMap
                               [playerX/(Setup.GRID_SIZE *
                                         Setup.PIXEL_SIZE),
                                playerY/(Setup.GRID_SIZE *
                                         Setup.PIXEL_SIZE)])
                        firewood = item.Item(tree.rect.centerx, tree.rect.centery-32, firewood_image)
                        self.items.add(firewood)
                        Globals.CURRENT_PLAYER[3] += 10
                        Globals.WORLD.addEntity(firewood)
            elif self.spaceCounter <= 20:
                self.spaceCounter += 1
            else:
                self.spaceCounter = 0
        elif not key[PG.K_SPACE]:
            self.spaceCounter = 0

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
                              self, self.firewood)
        self.enemyGroup.update(smooth.wallMap
                               [playerX/(Setup.GRID_SIZE * Setup.PIXEL_SIZE),
                                playerY/(Setup.GRID_SIZE * Setup.PIXEL_SIZE)], self.hero)
        self.npcGroup.update(smooth.wallMap
                               [playerX/(Setup.GRID_SIZE * Setup.PIXEL_SIZE),
                                playerY/(Setup.GRID_SIZE * Setup.PIXEL_SIZE)])
        self.enemyProjectileGroup.update(self.hero)
        for i in self.items:
            i.pickedUp(self.hero)
            if i.isPickedUp:
                self.woodSound.play()
                self.hero.firewood += 1
                Globals.HUD.updateSupply(self.hero.firewood)
                self.static_score = 10
                Globals.HUD.updateScore(self.static_score)
        if self.firewood.isPickedUp and Player.events[0]:
            dialogue = DB.Dialogue_box("good_job.txt")
            while dialogue.isOpen:
                dialogue.update()
            Player.events[0] = False
            Globals.HUD.resetSupply()
        for enemy in self.enemyGroup:
            self.heroProjectileGroup.update(enemy)
            self.heroSword.update(self.hero, enemy)
        if Player.events[3] == False and Player.events[4] == True:
            # Allows player to move to level 2
            Globals.CURRENT_PLAYER[3] += self.score + self.static_score
            Globals.STATE = LevelTwo.LevelTwo()
        if Player.events[5] == False and Player.events[6] == True:
            # Allows player to begin fireball quest
            # Projectile Logic
            if key[PG.K_r] and self.fireballQuestCounter < 5:
                if (self.currTime - self.cooldown_timer) >= 2:
                    temp = self.hero.shoot_projectile(Globals.STATE.heroProjectileGroup)
                    Globals.WORLD.addEntity(temp)
                    self.cooldown_timer = self.currTime
                    Globals.HUD.updateCooldown()
                    self.fireballQuestCounter += 1
            self.heroProjectileGroup.update()
            if self.fireballQuestCounter == 5:
                # Done with fireball quest
                self.doneTime = time.clock()
                # This trick makes it such that doneTime is only calculated once
                self.fireballQuestCounter += 1
            elif self.fireballQuestCounter == 6:
                if time.clock() - self.doneTime > 2:
                    Player.events[6] = False
                    Globals.HERO.rect = self.hero.rect
                    Globals.STATE = cutscene1.Cutscene3()
            # Sword logic
            if key[PG.K_e]:
                if self.sword_counter % SWORD_COUNTER == 0:
                    self.hero.attacking = True
                self.sword_counter += 1
            elif not key[PG.K_e]:
                self.sword_counter = 0
                self.wait += 1
                if self.wait % 5 == 0:
                    self.hero.attacking = False
        Globals.HUD.updateHealth()
        # joystick controls
        '''
        if PJ.get_count() > 0:
            print PJ.get_count()
            if joystick.get_axis(2) > 0.1:
                self.hero.speed = 8.0
            if joystick.get_button(0):
                if self.spaceCounter == 0:
                    self.spaceCounter += 1
                    interactable = []
                    list_interactable = []
                    for sprite in Globals.WORLD.return_interactable():
                        interactable.append(sprite.rect)
                        list_interactable.append(sprite)
                    index = self.hero.action_rect.collidelist(interactable)
                    if index != -1:
                        # Play Cut Sound
                        self.cutSound.set_volume(0.3)
                        self.cutSound.play()
                        tree = list_interactable[index]
                        if tree.health > 0:
                            tree.health -= 1
                        else:
                            tree.cutDown(smooth.wallMap
                                   [playerX/(Setup.GRID_SIZE *
                                             Setup.PIXEL_SIZE),
                                    playerY/(Setup.GRID_SIZE *
                                             Setup.PIXEL_SIZE)])
                            firewood = item.Item(tree.rect.centerx, tree.rect.centery-32, firewood_image)
                            self.items.add(firewood)
                            Globals.CURRENT_PLAYER[3] += 10
                            Globals.WORLD.addEntity(firewood)
                elif self.spaceCounter <= 20:
                    self.spaceCounter += 1
                else:
                    self.spaceCounter = 0

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
    def currentScore(self):
        return self.score

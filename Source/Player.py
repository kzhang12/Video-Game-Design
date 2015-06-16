import os as OS
import sys as SYS
import pygame as PY
import pygame.display as PD
import pygame.image as PI
import pygame.event as PE
import pygame.sprite as PS
import pygame.time as PT
import pygame.mixer as PX
import DialogueBox as DB
import Functions
import Setup
import Character
import Score
import LevelOne
import LevelTwo
import LevelThree
import WinScreen
import LoseScreen
import Projectile
import Sword
from Character import BaseClass
from smooth import wallMap
from smooth import Grass
from smooth import Sand
from smooth import Grey_brick
from smooth import TriggerBlockSand
from smooth import Entity
from Screen import Globals
import LevelTwo
import LevelThree
Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir),
                          'Images/WarriorSpriteSheet.png')
fireball = OS.path.join(OS.path.dirname(Dir), 'Images/Fireball.png')
sword = OS.path.join(OS.path.dirname(Dir), 'Images/SwordSwing.png')
SOUND_PATH = OS.path.join(OS.path.dirname(Dir), 'Sounds/playerCollision.wav')

fireball_sound = OS.path.join(OS.path.dirname(Dir), 'Sounds/Fireball.wav')
sword_hit_sound = OS.path.join(OS.path.dirname(Dir), 'Sounds/SwordHit.wav')
sword_miss_sound = OS.path.join(OS.path.dirname(Dir), 'Sounds/SwordMiss.wav')


MAX_SPEED = 5.0
DECELERATION_RATE = 0.5
FADEOUTTIME = 0.2
MAX_HEALTH = 100.0
TIME_UPDATE = 5
MELEE_TIME = 20
MELEE_ANIMATION_TIME = 5
events = [True, True, True, True, True, True, True, True, True, True]
# Event list:
# 0: Picks up wood from sheep pen
# 1: Talks to parents for first time
# 2: Village elder tells player to get sword
# 3: Transition from level 1 to level 2
# 4: Picks up sword
# 5: Moves from level 2 back to level 1
# 6: Completes Fireball practice quest
# 7: Moves from level 1 to level 3
# 8: Moves from level 3 to level 4


class Player(Entity):
    def __init__(self):
        IMAGES = None
        NPC_IMAGES = None
        SWORD_IMAGES = None
        Entity.__init__(self)
        if not IMAGES and not SWORD_IMAGES:
            self.load_images()
        self.image_timer = 0
        self.image_tracker = 0
        self.attack_image_tracker = 0
        self.melee_timer = 0
        self.melee_animation_timer = 0
        self.image = Player.IMAGES[2]
        self.attack_image = Player.SWORD_IMAGES[0]
        self.area = None
        self.rect = self.image.get_rect()
        # self.rect.centery = self.rect.centery
        self.rect.centerx = 100
        self.rect.centery = 100
        self.speed = 3.0
        self.direction = "still"
        self.change_direction = False
        self.movepos = [0.0, 0.0]
        self.time = 0.0
        self.moving = False
        self.walls = None
        self.newpos = [0.0, 0.0]
        self.action_rect = PY.Rect(0, 0, 32, 32)
        self.health = MAX_HEALTH
        self.firewood = -1
        self.elderCount = 0  # number of times spoken to elder
        self.attack_direction = 0
        self.previous_direction = 0
        self.sword_counter = 0
        self.attacking = False
        self.wasSwung = False
        self.swordNoise = False
        PX.init()  # Initialize sound player
        self.fireballSound = PX.Sound(fireball_sound)
        self.swordMissSound = PX.Sound(sword_miss_sound)
        self.swordHitSound = PX.Sound(sword_hit_sound)
        self.fireballSound.set_volume(Globals.VOLUME/200.0)
        self.swordMissSound.set_volume(Globals.VOLUME/200.0)
        self.swordHitSound.set_volume(Globals.VOLUME/200.0)

        projectile_counter = 0
        self.swingDelay = 0
        self.potions = PS.Group()

    def update(self, enemyGroup,  npcGroup, spriteGroup, thisLevelOne, item=None):
        self.area = PY.Rect(0, 0, Globals.WORLD.realwidth,
                            Globals.WORLD.realheight-50)
        # PY.draw.rect(Globals.SCREEN, (0, 0, 0), self.action_rect)
        # PY.draw.rect(Globals.SCREEN, (255, 255, 255), self.bottomrect)

        PY.mixer.music.load(SOUND_PATH)
        self.dirty = 1
        newpos = self.rect.move(self.movepos)

        if self.area.contains(newpos):
            if not self.movepos[0] == 0:
                self.rect.left += self.movepos[0]
            if not self.movepos[1] == 0:
                self.rect.bottom += self.movepos[1]
        # if Functions.isCollision(self.rect):
        # PY.mixer.music.play()
        # self.collide(self.movepos[0], 0, spriteGroup, thisLevelOne, item)
        # self.collide(0, self.movepos[1], spriteGroup, thisLevelOne, item)
        # Draw healthbar
        self.healthBarBack = PY.Rect(self.rect.centerx
                                     - 20, self.rect.centery - 40, 40, 8)
        self.healthBarFront = PY.Rect(self.rect.centerx - 20,
                                      self.rect.centery
                                      - 40, 40*(self.health/MAX_HEALTH), 8)
        self.healthBarBack = Globals.WORLD.camera.apply(self.healthBarBack)
        self.healthBarFront = Globals.WORLD.camera.apply(self.healthBarFront)
        #PY.draw.rect(Globals.SCREEN, (255, 0, 0), self.healthBarBack)
        #PY.draw.rect(Globals.SCREEN, (0, 255, 0), self.healthBarFront)
        self.collide(self.movepos[0], 0, spriteGroup, thisLevelOne, item)
        self.collide(0, self.movepos[1], spriteGroup, thisLevelOne, item)
        # self.enemyCollide(self.movepos[0], 0, enemyGroup, thisLevelOne)
        # self.enemyCollide(0, self.movepos[1], enemyGroup, thisLevelOne)
        self.npcCollide(self.movepos[0], 0, npcGroup, thisLevelOne)
        self.npcCollide(0, self.movepos[1], npcGroup, thisLevelOne)
        self.enemyCollide(enemyGroup, thisLevelOne)
        self.eventCollide(Globals.WORLD.get_entities(), thisLevelOne)
        if self.swingDelay != 0:
            self.swingDelay -= 1

        # Checks if player steps on potion
        if self.potions != None:
            # Check if potion is picked up
            for p in self.potions:
                p.pickedUp(self)
                if p.isPickedUp:
                    self.health += 20 * 3

    def load_images(self):
        # Loads player spritesheet
        Player.IMAGES = []
        Player.SWORD_IMAGES = []
        sheet = PI.load(image_path).convert()
        sword_sheet = PI.load(sword).convert()
        key = sheet.get_at((0, 0))
        sword_key = sheet.get_at((0, 0))

        for i in range(3):
            for j in range(4):
                surface = PY.Surface((32, 32)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i*32, j*32, 32, 32))
                Player.IMAGES.append(surface)
                sword_surface = PY.Surface((64, 64)).convert()
                sword_surface.set_colorkey(sword_key)
                sword_surface.blit(sword_sheet, (0, 0), (i*64, j*64, 64, 64))
                Player.SWORD_IMAGES.append(sword_surface)

    def update_image(self, image_num, change_direction):
        if self.image_timer > TIME_UPDATE or change_direction:
            if not self.attacking:
                self.image = Player.IMAGES[image_num]
                self.image.convert_alpha()
                self.image_tracker = (self.image_tracker+1) % 3
                self.image_timer = 0
                self.change_direction = False
            else:
                self.sword_attack()
                self.image = PY.Surface((32, 32)).convert_alpha()
                self.image.fill((0, 0, 0, 0))
                # self.image.convert_alpha()
                self.image_tracker = (self.image_tracker+1) % 3
                self.image_timer = 0
        else:
            self.image_timer += 1
        # self.rect = self.image.get_rect()
        # Player.rect.center = (Setup.WIDTH/2, Setup.HEIGHT/2)  DO WE USE THIS?

    def movedown(self, image_counter):
        if self.direction != 'movedown':  # we just changed directions
            self.movepos = [0.0, 0.0]  # remove deceleration
            self.image_tracker = 0
            self.change_direction = True
        else:
            self.movepos[1] = self.speed

        self.direction = "movedown"
        self.attack_direction = 0
        self.update_image(self.image_tracker*4, self.change_direction)
        self.moving = True
        self.action_rect.width = 32
        self.action_rect.height = 32
        self.action_rect.midtop = self.rect.midbottom
        self.action_rect.centery -= 10
        # self.action_rect = Globals.WORLD.camera.apply(self.action_rect)

    def moveleft(self, image_counter):
        if self.direction != 'moveleft':
            self.movepos = [0.0, 0.0]  # remove deceleration
            self.image_tracker = 0
            self.change_direction = True
        else:
            self.movepos[0] = -self.speed
        self.attack_direction = 1
        self.direction = "moveleft"
        self.update_image(self.image_tracker*4+1, self.change_direction)
        self.moving = True
        self.action_rect.width = 32
        self.action_rect.height = 32
        self.action_rect.midright = self.rect.midleft
        self.action_rect.centerx += 10
        # self.action_rect = Globals.WORLD.camera.apply(self.action_rect)

    def moveright(self, image_counter):
        if self.direction != 'moveright':
            self.movepos = [0.0, 0.0]  # remove deceleration
            self.image_tracker = 0
            self.change_direction = True
        else:
            self.movepos[0] = self.speed
        self.attack_direction = 2
        self.direction = "moveright"
        self.update_image(self.image_tracker*4+2, self.change_direction)
        self.moving = True
        self.action_rect.width = 32
        self.action_rect.height = 32
        self.action_rect.midleft = self.rect.midright
        self.action_rect.centerx -= 10
        # self.action_rect = Globals.WORLD.camera.apply(self.action_rect)

    def moveup(self, image_counter):
        if self.direction != 'moveup':  # we just changed directions
            self.movepos = [0.0, 0.0]  # remove deceleration
            self.image_tracker = 0
            self.change_direction = True
        else:
            self.movepos[1] = -self.speed
        self.attack_direction = 3
        self.direction = "moveup"
        self.update_image(self.image_tracker*4+3, self.change_direction)
        self.moving = True
        self.action_rect.width = 32
        self.action_rect.height = 32
        self.action_rect.midbottom = self.rect.midtop
        self.action_rect.centery += 10
        # self.action_rect = Globals.WORLD.camera.apply(self.action_rect)

    def moveidle(self, image_counter):

        # Implementing deceleration
        if self.movepos != [0, 0]:
            if self.movepos[0] > 0:
                self.movepos[0] -= DECELERATION_RATE
                if self.movepos[0] < 0:
                    self.movepos[0] = 0
            else:  # self.movepos[0] < 0
                self.movepos[0] += DECELERATION_RATE
                if self.movepos[0] > 0:
                    self.movepos[0] = 0
            if self.movepos[1] > 0:
                self.movepos[1] -= DECELERATION_RATE
                if self.movepos[1] < 0:
                    self.movepos[1] = 0
            else:  # self.movepos[1] < 0
                self.movepos[1] += DECELERATION_RATE
                if self.movepos[1] > 0:
                    self.movepos[1] = 0
        # Done with deceleration

        # Makes sure that correct sprite is showing due to direction
        if self.direction == 'moveleft':
            if self.movepos[0] < 0:
                self.update_image(self.image_tracker*4+1, False)
            else:
                if not self.attacking:
                    self.image = Player.IMAGES[5]
                else:
                    self.sword_attack()
            self.attack_direction = 1
            self.action_rect.midright = self.rect.midleft
            self.action_rect.centerx += 10
        elif self.direction == 'moveup':
            if self.movepos[1] < 0:
                self.update_image(self.image_tracker*4+3, False)
            else:
                if not self.attacking:
                    self.image = Player.IMAGES[7]
                else:
                    self.sword_attack()
            self.attack_rect = 3
            self.action_rect.midbottom = self.rect.midtop
            self.action_rect.centery += 10
        elif self.direction == 'movedown':
            if self.movepos[1] > 0:
                self.update_image(self.image_tracker*4, False)
            else:
                if not self.attacking:
                    self.image = Player.IMAGES[4]
                else:
                    self.sword_attack()
            self.attack_direction = 0
            self.action_rect.midtop = self.rect.midbottom
            self.action_rect.centery -= 10
        else:
            if self.movepos[0] > 0:
                self.update_image(self.image_tracker*4+2, False)
            else:
                if not self.attacking:
                    self.image = Player.IMAGES[6]
                else:
                    self.sword_attack()
            self.attack_direction = 2
            self.action_rect.midleft = self.rect.midright
            self.action_rect.centerx -= 10
        # self.direction = 'moveidle'
        self.moving = False

    def collide(self, xvel, yvel, spriteGroup, thisLevelOne, item):
        FADEOUTTIME = 0.2
        attackrect = PY.Rect(0, 0, 32, 32)
        attackrect.center = self.rect.center
        # PY.draw.rect(Globals.SCREEN,PY.Color(0, 0, 0), attackrect)
        key = PY.key.get_pressed()
        for p in spriteGroup:
            if PY.Rect.colliderect(self.rect, p.rect):
                if isinstance(p, Grey_brick) \
                and item != None and item.isPickedUp:
                    spriteGroup.remove(p)
                # elif isinstance(p, ExitBlock):
                #    Globals.STATE = WinScreen.WinScreen(100)
                elif xvel > 0:
                    self.rect.right = p.rect.left
                elif xvel < 0:
                    self.rect.left = p.rect.right
                elif yvel > 0:
                    self.rect.bottom = p.rect.top
                elif yvel < 0:
                    self.rect.top = p.rect.bottom
                else:
                    continue

    def npcCollide(self, xvel, yvel, npcGroup, thisLevelOne):
        key = PY.key.get_pressed()
        for npc in npcGroup:
            if PS.collide_rect(self, npc):
                if xvel > 0:
                    self.rect.right = npc.rect.left
                elif xvel < 0:
                    self.rect.left = npc.rect.right
                elif yvel > 0:
                    self.rect.bottom = npc.rect.top
                elif yvel < 0:
                    self.rect.top = npc.rect.bottom
    # collision detection between hero and enemies

    # def enemyCollide(self, xvel, yvel,enemyGroup, thisLevelOne):
            # key = PY.key.get_pressed()
            # for enemy in enemyGroup:
            # if PS.collide_rect(self, enemy):
            #   if xvel > 0:
            #       self.rect.right = enemy.rect.left
            #   elif xvel < 0:
            #       self.rect.left = enemy.rect.right
            #   elif yvel > 0:
            #       self.rect.bottom = enemy.rect.top
            #   elif yvel < 0:
            #                   self.rect.top = enemy.rect.bottom
#               else:
#       continue
            #   self.health -= 1
            #   if self.health == 0:
            #                    Globals.STATE = LoseScreen.LoseScreen(0)

    def enemyCollide(self, enemyGroup, thisLevelOne):
        key = PY.key.get_pressed()
        for enemy in enemyGroup:
            if self.attacking and self.swingDelay == 0:
                if PY.Rect.colliderect(self.action_rect, enemy.rect):
                    self.swordHitSound.play()
                    enemy.health -= 10
                    self.swingDelay = 36

    def eventCollide(self, spriteGroup, thisLevelOne):
        for p in spriteGroup:
            if PS.Rect.colliderect(self.rect, p.rect):
                if isinstance(p, TriggerBlockSand) and p.event == 1 \
                        and events[1]:
                    # Parents speak to player first time
                    dialogue = DB.Dialogue_box("cutscene2_dialogue.txt")
                    while dialogue.isOpen:
                        dialogue.update()
                    events[1] = False
                elif isinstance(p, TriggerBlockSand) and p.event == 2 \
                        and not events[1] \
                        and events[2] \
                        and self.elderCount == 0:
                    # Elder gives wood cutting quest to player
                    dialogue = DB.Dialogue_box("cutscene3_dialogue.txt")
                    while dialogue.isOpen:
                        dialogue.update()
                    self.elderCount = 1
                elif isinstance(p, TriggerBlockSand) and p.event == 2 \
                        and not events[1] \
                        and events[2] \
                        and self.elderCount == 1 \
                        and self.firewood >= 3:
                    # Elder tells player to get sword
                    dialogue = DB.Dialogue_box("cutscene4_dialogue.txt")
                    while dialogue.isOpen:
                        dialogue.update()
                    Globals.HUD.resetSupply()
                    events[2] = False
                elif isinstance(p, TriggerBlockSand) and p.event == 3 \
                        and not events[2] \
                        and events[3]:
                    # Transition from Level 1 to Level 2
                    events[3] = False
                    # events[4] is set to false in LevelTwo.py
                elif isinstance(p, TriggerBlockSand) and p.event == 3 \
                        and not events[4] \
                        and events[5]:
                    # Transition from Level 2 to Level 1
                    events[5] = False

                    # events[6] is set to false in LevelOne.py

                elif isinstance(p, TriggerBlockSand) and p.event == 4 \
                        and not events[6] \
                        and events[7]:
                    # Transition from Level 1 to Level 3
                    events[7] = False
                    Globals.STATE = LevelThree.LevelThree()
            else:
                pass

    #  shoot projectiles from enemy
    def shoot_projectile(self, Pgroup):
        proj = Projectile.Projectile(self.rect, self.direction, None, fireball, True)
        Pgroup.add(proj)
        self.fireballSound.play()
        return proj

    def sword_attack(self):
        # Checks if is continuous swing
        if self.previous_direction == self.attack_direction:
            # Swing counter
            if self.melee_timer == 0:
                # Separates melee attacks from melee animation
                # Checks if melee animation was done
                if self.melee_animation_timer == 0 and self.attack_image_tracker % 3 == 0 and self.wasSwung:
                    self.melee_timer = (self.melee_timer+1) % MELEE_TIME
                    self.wasSwung = False
                    self.swordNoise = False
                # Swing animation counter
                if self.melee_animation_timer == 0:
                    self.wasSwung = True
                    self.attack_image = self.SWORD_IMAGES[self.attack_image_tracker*4+self.attack_direction]
                    self.attack_image_tracker = (self.attack_image_tracker+1) % 3
                    self.melee_animation_timer = (self.melee_animation_timer + 1) % MELEE_ANIMATION_TIME
                else:
                    self.melee_animation_timer = (self.melee_animation_timer + 1) % MELEE_ANIMATION_TIME

            else:
                self.melee_timer = (self.melee_timer+1) % MELEE_TIME

            if self.attack_image_tracker % 3 == 0 and self.swordNoise == False:
                self.swordMissSound.play()
                self.swordNoise = True

        # Checks if player changed direction
        else:
            self.swordMissSound.play()
            self.attack_image_tracker = 0
            self.melee_timer = 0
            self.attack_image = self.SWORD_IMAGES[self.attack_image_tracker*4+self.attack_direction]
            self.previous_direction = self.attack_direction

        newRect = Globals.WORLD.camera.apply(self.rect)
        Globals.SCREEN.blit(self.attack_image, (newRect.left-16, newRect.top-16))

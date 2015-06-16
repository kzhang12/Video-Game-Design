import os as OS
import sys as SYS
import time
import random
import pygame as PY
import pygame.display as PD
import pygame.event as PE
import pygame.image as PI
import pygame.sprite as PS
import pygame.mixer as PX
import Setup
import LevelOne
import item
from LevelTwo import LevelTwo
import Projectile
from smooth import Entity
import Functions
from Character import BaseClass
from Screen import Globals
SPEED = 1

Dir = OS.getcwd()
image_path = OS.path.join(OS.path.dirname(Dir), 'Images/EarthWarrior.png')
boulder_path = OS.path.join(OS.path.dirname(Dir), 'Images/Boulder.png')
tornado_path = OS.path.join(OS.path.dirname(Dir), 'Images/Tornado.png')
water_path = OS.path.join(OS.path.dirname(Dir), 'Images/waterBall.png')
earth = OS.path.join(OS.path.dirname(Dir), 'Images/earth.png')
wind = OS.path.join(OS.path.dirname(Dir), 'Images/wind.png')
water = OS.path.join(OS.path.dirname(Dir), 'Images/water.png')
boss_path = OS.path.join(OS.path.dirname(Dir), 'Images/waterLeader.png')
healer_path = OS.path.join(OS.path.dirname(Dir), 'Images/healer.png')
health_potion_image = OS.path.join(OS.path.dirname(Dir), 'Images/healthPotion.png')

hurt_sound = OS.path.join(OS.path.dirname(Dir), 'Sounds/hurtSound.wav')

MIN_MOVE_DURATION = 20
MAX_MOVE_DURATION = 50

MIN_WAIT_DURATION = 25
MAX_WAIT_DURATION = 75


PROJECTILE_TIMER = 150
AGGRO_RANGE = 600
ATTACK_OFFSET = 5
ATTACK_TIMER = 50


class Enemy(Entity):
    # attack_type: 0 for melee, 1 for ranged
    # nation: 0 for water, 1 for wind, 2 for earth
    def __init__(self, x, y, boole, attack_type = 0, nation = 0, health = 20.0):
        PX.init()
        self.hurtSound = PX.Sound(hurt_sound)
        self.hurtSound.set_volume(Globals.VOLUME/200.0)

        self.IMAGES = []
        self.PROJECTILE_IMAGES = []
        self.ra = boole
        self.status = None
        self.attack_type = attack_type
        self.nation = nation
        Entity.__init__(self)
        self.image_tracker = 0
        if not self.IMAGES:
            self.load_images()
        self.image = self.IMAGES[self.image_tracker]
        self.rect = self.image.get_rect()
        self.direction = 0
        self.isMoving = False
        self.moveCounter = 0  # allows for smooth enemy movement
        self.moveDuration = 0  # randomly generated for random movements
        self.health = health
        self.max_health = health
        self.attack_rect = (0, 0)
        self.inRange = False

        #  Boundaries for the enemy
        self.MIN_X_POS = self.rect.width/2
        self.MAX_X_POS = Globals.WORLD.realwidth - self.rect.width/2
        self.MIN_Y_POS = self.rect.height/2
        self.MAX_Y_POS = Globals.WORLD.realheight - self.rect.height/2
        self.rect.centerx = x
        self.rect.centery = y
        self.pTimer = 0
        self.attack_timer = 0
        self.burn_timer = 0
        self.burn_counter = 0
        self.aligned = False

    #  load enemy sprite

    def load_images(self):
        if (self.nation == 0):
            sheet = PI.load(water).convert()
            key = sheet.get_at((0, 0))
            sheet2 = PI.load(water_path).convert()
            key2 = sheet2.get_at((0, 0))
            for i in range(4):
                surface = PY.Surface((32, 32)).convert()
                surface.set_colorkey(key2)
                surface.blit(sheet2, (0, 0), (i * 32, 0, 32, 32))
                self.PROJECTILE_IMAGES.append(surface)
        if (self.nation == 1):

            sheet = PI.load(wind).convert()
            key = sheet.get_at((0, 0))
            sheet2 = PI.load(tornado_path).convert()
            key2 = sheet2.get_at((0, 0))
            for i in range(5):
                for j in range(5):
                    surface = PY.Surface((40, 40)).convert()
                    surface.set_colorkey(key2)
                    surface.blit(sheet2, (0, 0), (j*40, i*40, 40, 40))
                    self.PROJECTILE_IMAGES.append(surface)
        if (self.nation == 2):
            sheet = PI.load(earth).convert()
            key = sheet.get_at((0, 0))
            sheet2 = PI.load(boulder_path).convert()
            key2 = sheet2.get_at((0, 0))
            for i in range(8):
                surface = PY.Surface((40, 40)).convert()
                surface.set_colorkey(key2)
                surface.blit(sheet2, (0, 0), (i*40, 0, 40, 40))
                self.PROJECTILE_IMAGES.append(surface)
        for i in range(3):
            for j in range(4):
                surface = PY.Surface((32, 32)).convert()
                surface.set_colorkey(key)
                surface.blit(sheet, (0, 0), (i*32, j*32, 32, 32))
                self.IMAGES.append(surface)

    def update_image(self, image_num):
        image_num = image_num % 12
        self.image = self.IMAGES[image_num]
        self.image.convert_alpha()
        self.image_tracker = (self.image_tracker + 1) % 3

    #  move enemy, then detect for collisions
    # and throw projectiles as necessary
    def update(self, wallMap, hero):
        self.pTimer += 1
        currTime = time.time()    
        if self.status == 'burn':
            if currTime - self.burn_timer >= .5 and self.burn_counter < 6:
                surf = Globals.FONT.render("Burning", True, (255, 0,0))
                width, height = surf.get_size()
                font_rect = PY.Rect(0,0, width, height)
                font_rect.center = (self.rect.centerx, self.rect.centery-60)
                font_rect = Globals.WORLD.camera.apply(font_rect)
                Globals.SCREEN.blit(surf, font_rect)
                self.burn_timer = currTime
                self.health -= 1
                self.burn_counter += 1
            elif self.burn_counter == 6:
                self.burn_counter = 0
                self.status = None
        herorect = hero.rect
        selfrect = self.rect

        attackrect = PY.Rect(0, 0, AGGRO_RANGE, AGGRO_RANGE)
        attackrect.center = selfrect.center
        self.healthBarBack = PY.Rect(self.rect.centerx
                                     - 20, self.rect.centery - 40, 40, 8)
        self.healthBarFront = PY.Rect(self.rect.centerx - 20,
                                      self.rect.centery
                                      - 40, 40*(self.health/self.max_health), 8)
        self.healthBarBack = Globals.WORLD.camera.apply(self.healthBarBack)
        self.healthBarFront = Globals.WORLD.camera.apply(self.healthBarFront)
        PY.draw.rect(Globals.SCREEN, (255, 0, 0), self.healthBarBack)
        PY.draw.rect(Globals.SCREEN, (0, 255, 0), self.healthBarFront)
        y_dist = abs(self.rect.centery - herorect.centery)
        x_dist = abs(self.rect.centerx - herorect.centerx)
        if attackrect.contains(herorect):
            self.inRange = True
        else:
            self.inRange = False
        if (self.inRange):
            if x_dist < y_dist:
                if x_dist >= ATTACK_OFFSET:
                    # Then we prioritize in x direction
                    if (herorect.centerx < selfrect.centerx):
                        self.direction = 3
                    else:  # (herorect.centerx > selfrect.centerx):
                        self.direction = 1
                    self.aligned = False
                else:
                    # Then we are close enough in x direction so we prioritize y
                    if (herorect.centery < selfrect.centery):
                        self.direction = 0
                    else:  # (herorect.centery > selfrect.centery):
                        self.direction = 2
                    self.aligned = True

            else:  # y_dist <= x_dist:
                if y_dist >= ATTACK_OFFSET:
                    # Then we prioritize in y direction
                    if (herorect.centery < selfrect.centery):
                        self.direction = 0
                    else:  # (herorect.centery > selfrect.centery):
                        self.direction = 2
                    self.aligned = False
                else:
                    # Then we are close enough in y direction so we prioritize x
                    if (herorect.centerx < selfrect.centerx):
                        self.direction = 3
                    else:  # (herorect.centerx > selfrect.centerx):
                        self.direction = 1
                    self.aligned = True
            isCollision = False
            # Enemy AI logic
            if self.attack_type == 0:  # melee enemy
                if (x_dist >= 40 or y_dist >= ATTACK_OFFSET) and (y_dist >= 40 or x_dist >= ATTACK_OFFSET):
                    self.move(wallMap)
                else:
                    if self.attack_timer % ATTACK_TIMER == 0:
                        Globals.HERO.health -= 10
                        self.hurtSound.play()
                        self.attack_timer += 1
                    else:
                        self.attack_timer += 1
            else:  # ranged enemy
                if (x_dist >= 400 or y_dist >= ATTACK_OFFSET) and (y_dist >= 400 or x_dist >= ATTACK_OFFSET):
                    self.move(wallMap)
                else:
                    if self.attack_timer % ATTACK_TIMER == 0:
                        self.attack_timer += 1
                    else:
                        self.attack_timer += 1
        else:
            if self.moveCounter >= self.moveDuration:  # need new direction
                moveVal = random.randint(0, 1)
                if moveVal == 0:  # 50% chance of standing still
                    self.isMoving = False
                    self.moveDuration = random.randint(MIN_WAIT_DURATION, MAX_WAIT_DURATION)
                else:
                    self.moveDuration = random.randint(
                                                       MIN_MOVE_DURATION,
                                                       MAX_MOVE_DURATION)  # new moveDuration
                    # decides which direction to move in
                    self.direction = random.randint(0, 3)
                    self.isMoving = True

                self.moveCounter = 0  # reset moveCounter
                isCollision = False
            else:  # do not need new direction
                self.moveCounter += 1  # increment moveCounter
            if (self.ra):
                self.move(wallMap)
        # if not isinstance(Globals.STATE, LevelTwo):
        if self.attack_type == 1:
            if self.pTimer == PROJECTILE_TIMER:
                if self.aligned:
                    # Adds projectile to entity list
                    Globals.WORLD.addEntity(self.shoot_projectile
                                            (Globals.STATE.enemyProjectileGroup))
                    self.pTimer = 0
                else:
                    self.pTimer -= 1
        if self.health <= 0:
            self.kill()
            Globals.CURRENT_PLAYER[3] += 50
            Globals.HUD.updateScore(50)
            if random.randint(1,10) <= 3:  # 30% chance of dropping health potion
                self.healthPotion = item.Item(self.rect.centerx, self.rect.centery, health_potion_image)
                hero.potions.add(self.healthPotion)
                Globals.WORLD.addEntity(hero.potions)
               



    def move(self, wallMap):
        if self.isMoving or self.inRange:
            if self.direction == 0:  # up movement
                self.rect.centery -= 1
                self.update_image(self.image_tracker*4 + 3 + self.nation * 12)
                # adjust in case results in collision
                self.collide(0, -self.rect.centery, wallMap)
            elif self.direction == 1:  # right movement
                self.rect.centerx += 1
                self.update_image(self.image_tracker*4 + 2 + self.nation * 12)
                # adjust in case results in collision
                self.collide(self.rect.centerx, 0, wallMap)
            elif self.direction == 2:  # down movement
                self.rect.centery += 1
                self.update_image(self.image_tracker*4 + self.nation * 12)
                # adjust in case results in collision
                self.collide(0, self.rect.centery, wallMap)
            else:  # left movement
                self.rect.centerx -= 1
                self.update_image(self.image_tracker*4 + 1 + self.nation * 12)
                # adjust in case results in collision
                self.collide(-self.rect.centerx, 0, wallMap)
    #  shoot projectiles from enemy

    def shoot_projectile(self, Pgroup):
        proj = Projectile.Projectile(self.rect, self.direction, self.PROJECTILE_IMAGES)
        Pgroup.add(proj)
        return proj
    #  check for collisions with other sprites

    def collide(self, xvel, yvel, wallMap):
        FADEOUTTIME = 0.2
        for p in wallMap:
            if PS.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                elif xvel < 0:
                    self.rect.left = p.rect.right
                elif yvel > 0:
                    self.rect.bottom = p.rect.top
                elif yvel < 0:
                    self.rect.top = p.rect.bottom
                else:
                    continue

class Boss(Entity):
   def __init__(self, x, y):
       Entity.__init__(self)
       PX.init()
       self.hurtSound = PX.Sound(hurt_sound)
       self.hurtSound.set_volume(Globals.VOLUME/200.0)

       self.health = 200.0
       self.max_health = 200.0
       self.IMAGES = []
       self.PROJECTILE_IMAGES = []
       self.status = None
       self.image_tracker = 0
       if not self.IMAGES:
           self.load_images()
       self.image = self.IMAGES[self.image_tracker]
       self.rect = self.image.get_rect()
       self.direction = 0
       self.isMoving = False
       self.moveCounter = 0  # allows for smooth enemy movement
       self.moveDuration = 0  # randomly generated for random movements
       self.attack_rect = (0, 0)
       self.inRange = False
       self.attacking = False
       #  Boundaries for the enemy
       self.MIN_X_POS = self.rect.width/2
       self.MAX_X_POS = Globals.WORLD.realwidth - self.rect.width/2
       self.MIN_Y_POS = self.rect.height/2
       self.MAX_Y_POS = Globals.WORLD.realheight - self.rect.height/2
       self.rect.centerx = x
       self.rect.centery = y
       self.pTimer = 0
       self.attack_timer = 0
       self.attackVal = 0
       self.burn_timer = 0
       self.burn_counter = 0
       self.aligned = False
       self.phase = False
       self.ra = True
       self.speed = 2
       self.dash_time = 0
   def load_images(self):
       sheet = PI.load(boss_path).convert()
       key = sheet.get_at((0, 0))
       sheet2 = PI.load(water_path).convert()
       key2 = sheet2.get_at((0, 0))
       for i in range(4):
           surface = PY.Surface((32, 32)).convert()
           surface.set_colorkey(key2)
           surface.blit(sheet2, (0, 0), (i*32, 0, 32, 32))
           self.PROJECTILE_IMAGES.append(surface)
       for i in range(3):
           for j in range(4):
               surface = PY.Surface((64, 64)).convert()
               surface.set_colorkey(key)
               surface.blit(sheet, (0, 0), (i*64, j*64, 64, 64))
               self.IMAGES.append(surface)
   def update(self, wallMap, hero):
       self.pTimer += 1
       if (self.health/self.max_health) < .5:
           self.phase = True
       currTime = time.time()    
       if self.status == 'burn':
           if currTime - self.burn_timer >= .5 and self.burn_counter < 6:
               self.burn_timer = currTime
               self.health -= 1
               self.burn_counter += 1
           elif self.burn_counter == 6:
               self.burn_counter = 0
               self.status = None
       self.healthBarBack = PY.Rect(self.rect.centerx
                                    - 20, self.rect.centery - 40, 40, 8)
       self.healthBarFront = PY.Rect(self.rect.centerx - 20,
                                     self.rect.centery
                                     - 40, 40*(self.health/self.max_health), 8)
       self.healthBarBack = Globals.WORLD.camera.apply(self.healthBarBack)
       self.healthBarFront = Globals.WORLD.camera.apply(self.healthBarFront)
       PY.draw.rect(Globals.SCREEN, (255, 0, 0), self.healthBarBack)
       PY.draw.rect(Globals.SCREEN, (0, 255, 0), self.healthBarFront)
       if self.moveCounter >= self.moveDuration:  # need new direction
           moveVal = random.randint(0, 9)
           if moveVal <= 6:  # 50% chance of standing still
               self.isMoving = False
               self.moveDuration = random.randint(MIN_WAIT_DURATION, MAX_WAIT_DURATION)
           else:
               self.moveDuration = random.randint(
                                                  MIN_MOVE_DURATION,
                                                  MAX_MOVE_DURATION)  # new moveDuration
               # decides which direction to move in
               self.direction = random.randint(0, 3)
               self.isMoving = True
           self.moveCounter = 0  # reset moveCounter
           isCollision = False
       else:  # do not need new direction
           self.moveCounter += 1  # increment moveCounter
       if (self.ra and not self.attacking):
           self.move(wallMap)
       # if not isinstance(Globals.STATE, LevelTwo):
       if self.health <= 0:
           self.kill()
           Globals.HUD.updateScore(50)
       if currTime - self.attack_timer >= 3 or self.attacking:
           self.attack(wallMap,hero)
           self.attack_timer = currTime
   def move(self, wallMap):
       if self.isMoving or self.inRange:
           if self.direction == 0:  # up movement
               self.rect.centery -= self.speed
               self.update_image(self.image_tracker*4 + 3)
               # adjust in case results in collision
               self.collide(0, -self.rect.centery, wallMap)
           elif self.direction == 1:  # right movement
               self.rect.centerx += self.speed
               self.update_image(self.image_tracker*4 + 2)
                # adjust in case results in collision
               self.collide(self.rect.centerx, 0, wallMap)
           elif self.direction == 2:  # down movement
               self.rect.centery += self.speed
               self.update_image(self.image_tracker*4)
               # adjust in case results in collision
               self.collide(0, self.rect.centery, wallMap)
           else:  # left movement
               self.rect.centerx -= self.speed
               self.update_image(self.image_tracker*4 + 1)
               # adjust in case results in collision
               self.collide(-self.rect.centerx, 0, wallMap)
   def update_image(self, image_num):
       image_num = image_num % 12
       self.image = self.IMAGES[image_num]
       self.image.convert_alpha()
       self.image_tracker = (self.image_tracker + 1) % 3
   def collide(self, xvel, yvel, wallMap):
       FADEOUTTIME = 0.2
       for p in wallMap:
           if PS.collide_rect(self, p):
               if xvel > 0:
                   self.rect.right = p.rect.left
               elif xvel < 0:
                   self.rect.left = p.rect.right
               elif yvel > 0:
                   self.rect.bottom = p.rect.top
               elif yvel < 0:
                   self.rect.top = p.rect.bottom
               else:
                   continue
   def attack(self,wallMap, hero):        
      currTime = time.time()
      if not self.attacking:
          if self.phase == False:
              self.attackVal = random.randint(0,100)
          else:
              self.attackVal = random.randint(0,110)
          self.attacking = True
      y_dist = abs(self.rect.centery - hero.rect.centery)
      x_dist = abs(self.rect.centerx - hero.rect.centerx)
      if self.attackVal < 30:

          if self.dash_time == 0:
              self.align(hero,x_dist, y_dist)
              if (x_dist >= 250 or y_dist >= ATTACK_OFFSET) and (y_dist >= 250 or x_dist >= ATTACK_OFFSET):
                  self.isMoving = True
                  self.move(wallMap)
              else:
                  self.dash_time +=1
          else:
              if self.dash_time < 50:
                 self.dash(currTime, wallMap)
                 if PS.collide_rect(hero,self):
                     hero.health -= 1
                     self.hurtSound.play()
              else:
                 self.attacking = False
                 self.speed = 2
                 self.dash_time = 0
      elif self.attackVal < 60:
          self.align(hero, x_dist, y_dist)
          if (x_dist >= 250 or y_dist >= ATTACK_OFFSET) and (y_dist >= 250 or x_dist >= ATTACK_OFFSET):

              self.isMoving = True
              self.move(wallMap)
          else:
              if self.aligned:
                  Globals.WORLD.addEntity(self.shoot_projectile
                                           (Globals.STATE.enemyProjectileGroup))
              self.attacking = False   
      elif self.attackVal < 80:
          self.align(hero, x_dist, y_dist)
          if (x_dist >= 250 or y_dist >= ATTACK_OFFSET) and (y_dist >= 250 or x_dist >= ATTACK_OFFSET):
              self.isMoving = True
              self.move(wallMap)           
          else:
              temp = Projectile.Whirlpool(self.rect,hero,self.direction)
              Globals.WORLD.addEntity(temp)
              Globals.STATE.enemyProjectileGroup.add(temp)
              self.attacking = False
      elif self.attackVal < 100:
          spawn = random.randint(0,2) + 1
          for i in range(spawn):
              x_rand = random.randint(-30,30) + self.rect.centerx
              y_rand = random.randint(-30, 30) + self.rect.centery
              attack_type = random.randint(0,1)
              enemy = Enemy(x_rand, y_rand, True, attack_type, 0, 40.0)
              enemy.speed = 2
              Globals.WORLD.addEntity(enemy)
              Globals.STATE.enemyGroup.add(enemy)
          self.attacking = False
   def dash(self, start_time, wallMap):
       self.speed = 7
       self.move(wallMap)
       self.dash_time += 1
   def align(self, hero, x, y):
       y_dist = y
       x_dist = x
       if x_dist < y_dist:
           if x_dist >= ATTACK_OFFSET:
            # Then we prioritize in x direction
               if (hero.rect.centerx < self.rect.centerx):
                   self.direction = 3
               else:  # (herorect.centerx > selfrect.centerx):
                   self.direction = 1
               self.aligned = False
           else:

               # Then we are close enough in x direction so we prioritize y
               if (hero.rect.centery < self.rect.centery):
                   self.direction = 0
               else:  # (herorect.centery > selfrect.centery):
                   self.direction = 2
               self.aligned = True
       else:  # y_dist <= x_dist:
           if y_dist >= ATTACK_OFFSET:
               # Then we prioritize in y direction
               if (hero.rect.centery < self.rect.centery):
                   self.direction = 0
               else:  # (herorect.centery > selfrect.centery):
                   self.direction = 2
               self.aligned = False

           else:
               # Then we are close enough in y direction so we prioritize x
               if (hero.rect.centerx < self.rect.centerx):
                   self.direction = 3
               else:  # (herorect.centerx > selfrect.centerx):
                   self.direction = 1
               self.aligned = True
       isCollision = False
   def shoot_projectile(self, Pgroup):
       proj = Projectile.Projectile(self.rect, self.direction, self.PROJECTILE_IMAGES)
       Pgroup.add(proj)
       return proj

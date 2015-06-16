import sys as SYS
import os as OS
import random as R
import pygame as PG
import pygame.surface as PS
import pygame.display as PDI
import pygame.event as PE
import pygame.font as PF
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX
import pygame.draw as PD
import LevelOne
import Setup
from Character import BaseClass
import Player
from Screen import Globals
TILES = {}
WORLD = None
entities = PS.LayeredDirty()
interactable = PS.Group()
wallMap = {}
Dir = OS.getcwd()
Image_path = OS.path.join(OS.path.dirname(Dir), 'Images')


def loadtiles():
    """Each tile is 128x128 pixels."""
    global TILES
    file = open("tiles.txt")
    for line in file:
        if not line.isspace():
            code, image = line.strip().split()
            image_path = OS.path.join(Image_path, image)
            tempImage = PI.load(image_path).convert_alpha()
            TILES[code] = tempImage
    file.close()


class World(object):
    """World as loaded from configuration files."""
    camera = None

    def __init__(self, text):
        self.bg = PG.Surface((32, 32))
        self.bg.convert()
        self.bg.fill(PG.Color("#000000"))
        self.map = []
        file = open(text)
        for line in file:
            self.map.append(line.strip())
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.realheight = self.height*TILES.values()[0].get_height()
        self.realwidth = self.width*TILES.values()[0].get_width()
        self.camera = None
        x = y = 0
        gridX = 0  # The x coordinate of collision square
        gridY = 0  # The y coordinate of collision square
        rowNum = 0  # The x position of current pixel square
        colNum = 0  # the y position of current pixel square
        with open(text) as f:
            for row in f:
                if not wallMap.has_key((gridX, gridY)):
                    wallMap[(gridX, gridY)] = PS.Group()
                for col in row:
                    if not wallMap.has_key((gridX, gridY)):
                        wallMap[(gridX, gridY)] = PS.Group()
                    # Types of dirt textures
                    if col == ",":  # Dirt without grass
                        g = Sand(x, y, TILES[','])
                        entities.add(g)
                    if col == "-":
                        g = TriggerBlockSand(x, y, TILES[','], 1)
                        entities.add(g)
                    if col == '+':
                        g = TriggerBlockSand(x, y, TILES[','], 2)
                        entities.add(g)
                    if col == "_":
                        g = TriggerBlockSand(x, y, TILES[','], 3)
                        entities.add(g)
                    if col == "=":
                        g = TriggerBlockSand(x, y, TILES[','], 4)
                        entities.add(g)
                    # Ending types of dirt textures
                    if col == "\\":
                        g = Grey_brick(x, y, TILES['\\'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == "/":
                        g = Platform(x, y, TILES["/"])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == ".":
                        g = Grass(x, y, TILES['.'])
                        entities.add(g)
                    if col == "x":
                        g = Ice(x, y, TILES['x'])
                        entities.add(g)
                    if col == "X":
                        g = Platform(x, y, TILES['X'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == "w":
                        g = Platform(x, y, TILES['w'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == '(':
                        g = Platform(x, y, TILES['('])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    # Loads Ice Pillars
                    if col == 'q':
                        g = Platform(x, y, TILES['q'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'r':
                        g = Platform(x, y, TILES['r'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 's':
                        g = Platform(x, y, TILES['s'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 't':
                        g = Platform(x, y, TILES['t'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    # Loads building
                    if col == 'a':
                        g = Platform(x, y, TILES['a'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'b':
                        g = Platform(x, y, TILES['b'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'c':
                        g = Platform(x, y, TILES['c'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'd':
                        g = Platform(x, y, TILES['d'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'e':
                        g = Platform(x, y, TILES['e'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'f':
                        g = Platform(x, y, TILES['f'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'g':
                        g = Platform(x, y, TILES['g'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'h':
                        g = Platform(x, y, TILES['h'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'i':
                        g = Platform(x, y, TILES['i'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'j':
                        g = Platform(x, y, TILES['j'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'k':
                        g = Platform(x, y, TILES['k'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'l':
                        g = Platform(x, y, TILES['l'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'm':
                        g = Platform(x, y, TILES['m'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'n':
                        g = Platform(x, y, TILES['n'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'o':
                        g = Platform(x, y, TILES['o'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    elif col == 'p':
                        g = Platform(x, y, TILES['p'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    # Done loading building
                    # Loads Tree1
                    if col == 'A':
                        g = Platform(x, y, TILES['A'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'B':
                        g = Platform(x, y, TILES['B'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'C':
                        g = Platform(x, y, TILES['C'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'D':
                        g = Platform(x, y, TILES['D'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'E':
                        g = Platform(x, y, TILES['E'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'F':
                        g = Platform(x, y, TILES['F'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'G':
                        g = Platform(x, y, TILES['G'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'H':
                        g = Platform(x, y, TILES['H'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'I':
                        g = Platform(x, y, TILES['I'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'J':
                        g = Platform(x, y, TILES['J'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'K':
                        g = Platform(x, y, TILES['K'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'L':
                        g = Platform(x, y, TILES['L'])
                        wallMap[(gridX, gridY)].add(g)
                        entities.add(g)
                    if col == 'M':
                        g = Grass(x, y, TILES['M'])
                        entities.add(g)
                    if col == 'N':
                        g = Interactable(x, y, TILES['N'], 3, True)
                        entities.add(g)
                        wallMap[(gridX, gridY)].add(g)
                        interactable.add(g)
                    if col == 'O':
                        g = Interactable(x, y, TILES['O'], 3)
                        entities.add(g)
                        wallMap[(gridX, gridY)].add(g)
                        interactable.add(g)
                    if col == 'P':
                        g = Grass(x, y, TILES['P'])
                        entities.add(g)
                    # Done loading Tree1

                    x += 32
                    colNum += 1
                    gridX = colNum / Setup.GRID_SIZE

                y += 32
                x = 0
                gridX = 0
                colNum = 0
                rowNum += 1
                gridY = rowNum / Setup.GRID_SIZE

    def background(self, screen):
        for y in range(32):
            for x in range(32):
                screen.blit(self.bg, (x*32, y*32))

    def addEntity(self, hero):
        entities.add(hero)

    def get_entities(self):
        return entities

    def dr(self, screen):
        InvertedRect = self.camera.state
        for e in entities:
            if InvertedRect.contains(self.camera.apply(e)):
                screen.blit(e.image, self.camera.apply(e))

    def update(self, target):
        self.camera.update(target)

    def clear(self):
        wallMap.clear()
        entities.empty()

    def return_interactable(self):
        return interactable


class Entity(PS.DirtySprite):

    def __init__(self):
        PS.DirtySprite.__init__(self)


class Platform(Entity):

    def __init__(self, x, y, image):
        Entity.__init__(self)
        self.image = image
        self.image.convert()
        self.rect = PG.Rect(x, y, 32, 32)

    def update(self):
        self.dirty = 1

    def tile(self, x, y):
        """Return proper tile for given tile coordinates."""
        x = (self.width + x) % self.width
        y = (self.height + y) % self.height
        code = self.map[y][x]
        return TILES[code]


class Grass(Platform):

    def __init__(self, x, y, image):
        Platform.__init__(self, x, y, image)


class Ice(Platform):

    def __init__(self, x, y, image):
        Platform.__init__(self, x, y, image)


class Sand(Platform):

    def __init__(self, x, y, image):
        Platform.__init__(self, x, y, image)


class Grey_brick(Platform):

    def __init__(self, x, y, image):
        Platform.__init__(self, x, y, image)


class TriggerBlockSand(Sand):

    def __init__(self, x, y, image, event):
        Sand.__init__(self, x, y, image)
        self.event = event


class Interactable(Platform):

    def __init__(self, x, y, image, health=1, left=False):
        Platform.__init__(self, x, y, image)
        self.health = health
        self.left = left

    def cutDown(self, InteractableGroup):
        if self.left:
            for e in entities:
                if e.rect.top == self.rect.top - 32:
                    if e.rect.left == self.rect.left or e.rect.left == self.rect.left+32 or e.rect.left == self.rect.left+64 or e.rect.left == self.rect.left-32:
                        e.image = TILES['.']
                        InteractableGroup.remove(e)
                        interactable.remove(e)
                elif e.rect.top == self.rect.top - 64:
                    if e.rect.left == self.rect.left or e.rect.left == self.rect.left+32 or e.rect.left == self.rect.left+64 or e.rect.left == self.rect.left-32:
                        e.image = TILES['.']
                        InteractableGroup.remove(e)
                        interactable.remove(e)
                elif e.rect.top == self.rect.top - 96:
                    if e.rect.left == self.rect.left or e.rect.left == self.rect.left+32 or e.rect.left == self.rect.left+64 or e.rect.left == self.rect.left-32:
                        e.image = TILES['.']
                        InteractableGroup.remove(e)
                        interactable.remove(e)
                elif e.rect.top == self.rect.top:
                    InteractableGroup.remove(e)
                    interactable.remove(e)

        else:
            for e in entities:
                if e.rect.top == self.rect.top - 32:
                    if e.rect.left == self.rect.left or e.rect.left == self.rect.left-32 or e.rect.left == self.rect.left-64 or e.rect.left == self.rect.left+32:
                        e.image = TILES['.']
                        InteractableGroup.remove(e)
                        interactable.remove(e)
                elif e.rect.top == self.rect.top - 64:
                    if e.rect.left == self.rect.left or e.rect.left == self.rect.left-32 or e.rect.left == self.rect.left-64 or e.rect.left == self.rect.left+32:
                        e.image = TILES['.']
                        InteractableGroup.remove(e)
                        interactable.remove(e)
                elif e.rect.top == self.rect.top - 96:
                    if e.rect.left == self.rect.left or e.rect.left == self.rect.left-32 or e.rect.left == self.rect.left-64 or e.rect.left == self.rect.left+32:
                        e.image = TILES['.']
                        InteractableGroup.remove(e)
                        interactable.remove(e)
                elif e.rect.top == self.rect.top:
                    InteractableGroup.remove(e)
                    interactable.remove(e)
        InteractableGroup.remove(self)
        interactable.remove(self)


class Camera(object):

    def __init__(self, camera_func, world, x, y):
        self.camera_func = camera_func
        self.state = PG.Rect(0, 0, x, y)
        self.world = world
        self.set(x, y)

    def set(self, x, y):
        self.x = (self.world.realwidth+x) % self.world.realwidth
        self.y = (self.world.realheight+y) % self.world.realheight

    def left(self):
        self.set(self.x-100, self.y)

    def right(self):
        self.set(self.x+100, self.y)

    def up(self):
        self.set(self.x, self.y-100)

    def down(self):
        self.set(self.x, self.y+100)

    def apply(self, target):
        if not isinstance(target, PG.Rect):
            return target.rect.move(self.state.topleft)
        else:
            return target.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+Globals.WIDTH/2, -t+Globals.HEIGHT/2, w, h

    l = min(0, l)
    l = max(-(camera.width-Globals.WIDTH), l)
    t = max(-(camera.height-Globals.HEIGHT), t)
    t = min(0, t)
    return PG.Rect(l, t, w, h)

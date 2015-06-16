import Setup
import sys as SYS
import pygame as PG
import pygame.mouse as PM
import pygame.display as PDI
import pygame.event as PE
import pygame.font as PF
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX
import pygame.joystick as PJ
import Player
import Enemy
import LevelOne
import Title as Title
import HeadsUpDisplay
from Screen import BaseState as State
from Screen import Globals
import smooth
import os as OS

Dir = OS.getcwd()
screen_start_sound = OS.path.join(OS.path.dirname(Dir), 'Sounds/screen_start.wav')
loop_sound = OS.path.join(OS.path.dirname(Dir), 'Sounds/loopMusic.ogg')

INTERVAL = .01


def main():
    initialize()
    loop()
    finalize()


def initialize():
    passed, failed = PG.init()
    PJ.init()
    Globals.SCREEN = PDI.set_mode((800, 600), PG.DOUBLEBUF | PG.HWSURFACE)
    Globals.WIDTH = Globals.SCREEN.get_width()
    Globals.HEIGHT = Globals.SCREEN.get_height()
    Globals.FONT = PF.Font(None, 56)
    Globals.STATE = Title.Title_Screen()
    Globals.HERO = Player.Player()
    Globals.HUD = HeadsUpDisplay.HeadsUpDisplay()

    Globals.brightness = PG.Surface((800, 600))
    PX.init()
    Globals.MENU_MUSIC = PX.Sound(screen_start_sound)
    Globals.MUSIC = PX.Sound(loop_sound)



def loop():
    clock = PT.Clock()
    leftover = 0.0
    updates = 0
    up = 0
    isPlayingMenu = False
    isPlaying = False
    while Globals.RUNNING:
        if not isPlayingMenu:
            if Globals.ISMAINMENU:
                Globals.MENU_MUSIC.set_volume(Globals.VOLUME/200.0)
                Globals.MENU_MUSIC.play(-1)
                isPlayingMenu = True
        else:
            if not Globals.ISMAINMENU:
                isPlayingMenu = False

        if not isPlaying:
            if Globals.ISLEVELONE:
                Globals.MUSIC.set_volume(Globals.VOLUME/200.0)
                print 'playing'
                Globals.MUSIC.play(-1)
                isPlaying = True
        else:
            
            if not Globals.ISLEVELONE:
                Globals.MUSIC.stop()
        
        start_time = PT.get_ticks()
        Globals.STATE.render()
        if Globals.BRIGHTNESS < 0:
            Globals.brightness.fill((0, 0, 0))
            Globals.brightness.set_alpha(-1 * Globals.BRIGHTNESS/100.0 * 100)
            Globals.SCREEN.blit(Globals.brightness, (0, 0))
        elif Globals.BRIGHTNESS > 0:
            Globals.brightness.fill((255, 255, 255))
            Globals.brightness.set_alpha(Globals.BRIGHTNESS/100.0 * 100)
            Globals.SCREEN.blit(Globals.brightness, (0, 0))
        PDI.flip()
        updates = 0
        clock.tick(60)
        last = PT.get_ticks()
        elapsed = (last - start_time) / 1000.0
        Globals.STATE.update(elapsed)
        leftover += elapsed
        for event in PE.get():
            if event.type == PG.QUIT:
                Globals.RUNNING = False
            else:
                Globals.STATE.event(event)


def finalize():
    PDI.quit()
    PX.quit()
    PG.quit()
    SYS.exit()

if __name__ == "__main__":
    main()

import os as OS
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
import Player
import Enemy
import Setup
import Menu as Menu
from Screen import BaseState as State
from Screen import Globals
Dir = OS.getcwd()
data_path = OS.path.join(OS.path.dirname(Dir), 'Data/HighScores.txt')


class Score_Screen(State):
    FADEINTIME = 2.0
    FADEOUTTIME = 0.2

    def __init__(self, score=0):
        State.__init__(self)
        self.color = PC.Color("black")
        self.score = score
        self.time = 0.0
         
        Globals.SCREEN.fill(PC.Color("black"))
        self.changedScore = False
        # temporary filler
        self.name = Globals.CURRENT_PLAYER[0]
        highScores = open(data_path, 'r')
        indexCounter = 0
        self.scoreList = []
        added = False
        # Creating list of top 10 high scores
        for line in highScores:
            if indexCounter < 10:
                line = line.strip()
                player = line.split('@', 1)
                if self.score > int(player[1]) and (not added):
                    # Insert score in right place
                    self.scoreList.append((self.name, str(self.score)))
                    added = True
                    indexCounter += 1
                self.scoreList.append((player[0], player[1]))
                indexCounter += 1
        # If new score is lower than lowest score and there is still space
        if indexCounter < 10 and (not added):
            self.scoreList.append((self.name, str(self.score)))

        # Done creating list of high scores
        highScores.close()

        highScores = open(data_path, 'w')
        for entry in self.scoreList:
            highScores.write(entry[0] + '@' + entry[1] + '\n')
        highScores.close()

    def render(self):
        counter = 0
        # Go through array and print out scores
        for entry in self.scoreList:
            # make new score appear on screen
            surf = Globals.FONT.render(entry[0] + " " + entry[1], True,
                                       self.color)
            width, height = surf.get_size()
            Globals.SCREEN.blit(surf, (0, 0 + counter * height))
            counter += 1

    def update(self, time):
        self.time += time
        if self.time < Score_Screen.FADEINTIME:
            ratio = self.time / Score_Screen.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)

    def event(self, event):
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.RUNNING = False
        elif event.type == PG.KEYDOWN and event.key == PG.K_SPACE:
            PX.music.fadeout(int(Score_Screen.FADEOUTTIME*1000))
            Globals.STATE = Menu.Menu()

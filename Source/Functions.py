# Functions.py
# Andrew Ding
# Last edited: 10/04/2014


import sys as SYS
import os as OS
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
from Screen import BaseState as State
from Screen import Globals
import Menu as Menu

# isCollision function checks whether playerRect collides with the edges
# of the screen and optionally with otherRect.
# @param playerRect: rect for the player unit
# @param otherRect: rect for the other unit
# @return boolean: True if collision occurs, False if no collision occurs


def isCollision(playerRect, otherRect=None):  # otherRect is optional

    # Player boundary coordinates
    playerLeftPos = playerRect.centerx - playerRect.width/2
    playerRightPos = playerRect.centerx + playerRect.width/2
    playerTopPos = playerRect.centery - playerRect.height/2
    playerBottomPos = playerRect.centery + playerRect.height/2

    # Checking if there is collision with environment
    if playerLeftPos <= 0 or \
        playerRightPos >= Setup.WIDTH or \
        playerTopPos <= 0 or \
            playerBottomPos >= Setup.HEIGHT:
            # Collision detected against environment
            return True

    if (otherRect is not None):   # Both playerRect and otherRect were passed
        # Additionally checking if playerRect collided with otherRect

        # Other boundary coordinates
        otherLeftPos = otherRect.centerx - otherRect.width/2
        otherRightPos = otherRect.centerx + otherRect.width/2
        otherTopPos = otherRect.centery - otherRect.height/2
        otherBottomPos = otherRect.centery + otherRect.height/2

        # Checking if player collides with other

        # Horizontal collision check
        if playerRightPos == otherLeftPos or playerLeftPos == otherRightPos:
            # Checking that the vertical positions overlap
            if playerTopPos >= otherBottomPos or \
                    playerBottomPos <= otherTopPos:
                return True

        # Vertical collision check
        if playerTopPos == otherBottomPos or playerBottomPos == otherTopPos:
            # Checking that the horizontal positions overlap
            if playerLeftPos <= otherRightPos or \
                    playerRightPos >= otherLeftPos:
                return True
    return False  # No collision detected

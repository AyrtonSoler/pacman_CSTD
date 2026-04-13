#—————————————————— IMPORTS –——————————————————#
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from random import choice
import pandas as pd
import numpy as np
import math
import os

#——————————————————— CLASS —–——————————————————#
class Ghost:
    def __init__(self, map, mc, x_mc, y_mc, type):
        self.MC = mc                # control matrix
        self.XPxToMC = x_mc         # vector with x-coords
        self.YPxToMC = y_mc         # vector with y-coords
        # self.map = map              # map in pixels
        self.pos = [180, 130]       # starting position
        self.size = 20              # draw size
        self.dir = choice([2, 4])   # not moving
        self.type = type            # ghost type


    def loadTextures(self, textures):
        self.textures = textures


    def follow(self, pacmanXY):
        return

    def random(self):
        x = self.XPxToMC[self.pos[0]]
        y = self.YPxToMC[self.pos[1]]
        # Check intersection
        if(x >= 0 and y >= 0):
            # Get possible options
            options = []
            for i in range(4):
                if self.MC[y][x] & 2 ** (i):
                    options.append(i + 1)
            # Delete returns (if another option exists)
            # go_back = self.dir - 2 if self.dir - 2 > 0 else self.dir + 2
            if len(options) > 1:
                options.remove(self.dir - 2 if self.dir - 2 > 0 else self.dir + 2)

            # Choose
            self.dir = choice(options)
        # Move
        match self.dir:
            case 1:         # UP
                self.pos[1] -= 1
            case 2:         #RIGHT
                self.pos[0] += 1
            case 3:         #DOWN
                self.pos[1] += 1
            case 4:         #LEFT
                self.pos[0] -= 1
        return

    def update(self, pacmanXY):
        match self.type:
            case 0:
                self.random()
            case 1:
                self.follow(pacmanXY)
            case 2:
                self.follow(pacmanXY)
            case 3:
                self.follow(pacmanXY)
        return

    def draw(self):
        # Activate textures
        glColor3f(1.0,1.0,1.0)
        glEnable(GL_TEXTURE_2D)
        # Front face
        glBindTexture(GL_TEXTURE_2D, self.textures)
        glBegin(GL_QUADS)
        shift = 10
        glTexCoord2f(0.0, 0.0)
        glVertex2d(self.pos[0] + shift, self.pos[1] + shift)
        glTexCoord2f(0.0, 1.0)
        glVertex2d(self.pos[0] + shift, self.pos[1] + shift + self.size)
        glTexCoord2f(1.0, 1.0)
        glVertex2d(self.pos[0] + shift + self.size, self.pos[1] + shift + self.size)
        glTexCoord2f(1.0, 0.0)
        glVertex2d(self.pos[0] + shift + self.size, self.pos[1] + shift)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        return

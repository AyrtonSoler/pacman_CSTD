import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import os
import numpy as np
import pandas as pd

class Pacman:
    def __init__(self, map, mc, x_mc, y_mc):
        self.MC = mc            # control matrix
        self.XPxToMC = x_mc     # vector with x-coords
        self.YPxToMC = y_mc     # vector with y-coords
        self.map = map          # map in pixels
        self.pos = [180, 208]   # starting position
        self.size = 20          # draw size
        self.dir = 0            # not moving

    def loadTextures(self, textures, id):
        self.textures = textures
        self.Id = id

    def update(self, dir):
        x = self.XPxToMC[self.pos[0]]
        y = self.YPxToMC[self.pos[1]]
        # Go and return
        if self.dir % 2 == dir % 2:
            self.dir = dir
        # Move according to intersection
        if(x >= 0 and y >= 0):
            if(dir > 0):
                if self.MC[y][x] & 2 ** (dir - 1):
                    self.dir = dir
        # Check collision
            if(self.dir > 0):
                if not (self.MC[y][x] & 2 ** (self.dir - 1)):
                    self.dir = 0
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

    def draw(self):
        # Activate textures
        glColor3f(1.0,1.0,1.0)
        glEnable(GL_TEXTURE_2D)
        # Front face
        glBindTexture(GL_TEXTURE_2D, self.textures[1])
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

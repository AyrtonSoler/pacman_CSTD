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
    def __init__(self, mapa, mc, x_mc, y_mc):
        self.MC = mc            # control matrix
        self.XPxToMC = x_mc     # vector with x-coords
        self.YPxToMC = y_mc     # vector with y-coords
        self.mapa = mapa        # map in pixels
        self.start = 1          # starting point bool
        self.size = 20          # draw size

    def loadTextures(self, textures, id):
        self.textures = textures
        self.Id = id

    def update(self, dir):
        if self.start:
            self.start = 0
            self.pos = [190, 216]
            return
        else:
            # Go to fast fruit
            self.pos[1] -= 1
        return


    def draw(self):
        # Activate textures
        glColor3f(1.0,1.0,1.0)
        glEnable(GL_TEXTURE_2D)
        # Front face
        glBindTexture(GL_TEXTURE_2D, self.textures[1])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2d(self.pos[0], self.pos[1])
        glTexCoord2f(0.0, 1.0)
        glVertex2d(self.pos[0], self.pos[1] + self.size)
        glTexCoord2f(1.0, 1.0)
        glVertex2d(self.pos[0] + self.size, self.pos[1] + self.size)
        glTexCoord2f(1.0, 0.0)
        glVertex2d(self.pos[0] + self.size, self.pos[1])
        glEnd()
        glDisable(GL_TEXTURE_2D)
        return

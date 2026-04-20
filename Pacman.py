#—————————————————— IMPORTS –——————————————————#
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

#——————————————————— CLASS —–——————————————————#
class Pacman:
    def __init__(self, mc, x_mc, y_mc):
        self.pos = [180, 208]   # starting position
        self.XPxToMC = x_mc     # vector with x-coords
        self.YPxToMC = y_mc     # vector with y-coords
        self.size = 20          # draw size
        self.MC = mc            # control matrix
        self.dir = 0            # not moving

#————————————————— FUNCTIONS ——————————————————#
    def loadTextures(self, textures):
        self.textures = textures

    def update(self, dir):
        x = self.XPxToMC[self.pos[0]]
        y = self.YPxToMC[self.pos[1]]
        # Go and return, but don't stop
        if self.dir % 2 == dir % 2 and dir:
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
        # Move | UP(1), RIGHT(2), DOWN(3) or LEFT(4)
        if self.dir:
            self.pos[(self.dir & 1)] += 1 if (self.dir & 2) else -1

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

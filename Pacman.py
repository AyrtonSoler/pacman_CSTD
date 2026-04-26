#—————————————————— IMPORTS –——————————————————#
from sys import breakpointhook
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

#——————————————————— CLASS —–——————————————————#
class Pacman:
    def __init__(self, mc, XPxToMC, YPxToMC, XMCToPx, YMCToPx):
        self.XPxToMC = XPxToMC  # vector from pixels to x-coords
        self.YPxToMC = YPxToMC  # vector from pixels to y-coords
        self.XMCToPx = XMCToPx  # vector from x-coords to pixels
        self.YMCToPx = YMCToPx  # vector from y-coords to pixels
        self.pos = [180, 208]   # starting position
        self.size = 20          # draw size
        self.MC = mc            # control matrix
        self.dir = 0            # not moving
        # Create a dictionary for efficiently
        # hiding eaten dots
        self.xMap = {}
        self.yMap = {}
        for i in XMCToPx:
            self.xMap[i] = []
        for i in YMCToPx:
            self.yMap[i] = []

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
        self.route()
        return

    def draw(self, open):
        # Activate textures
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures[open])
        glPushMatrix()
        # Image center and rotation
        shift = 10
        half = self.size / 2
        cx = self.pos[0] + shift + half
        cy = self.pos[1] + shift + half
        angle = 0
        glTranslatef(cx, cy, 0)
        match self.dir:
            case 0: angle = 0
            case 1: angle = 270
            case 2: angle = 0
            case 3: angle = 90
            case 4: angle = 180
        glRotatef(angle, 0, 0, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2d(-half, -half)
        glTexCoord2f(0.0, 1.0)
        glVertex2d(-half,  half)
        glTexCoord2f(1.0, 1.0)
        glVertex2d( half,  half)
        glTexCoord2f(1.0, 0.0)
        glVertex2d( half, -half)
        glEnd()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
        return

    def mapdraw(self, key, segment, horizontal):
        glColor3f(0,0,0)
        glBegin(GL_QUADS)
        lmargin, rmargin = 15, 25
        if horizontal:
            glVertex2d(segment[0] + lmargin, key + lmargin)
            glVertex2d(segment[1] + rmargin, key + lmargin)
            glVertex2d(segment[1] + rmargin, key + rmargin)
            glVertex2d(segment[0] + lmargin, key + rmargin)
        else:
            glVertex2d(key + lmargin, segment[0] + lmargin)
            glVertex2d(key + lmargin, segment[1] + rmargin)
            glVertex2d(key + rmargin, segment[1] + rmargin)
            glVertex2d(key + rmargin, segment[0] + lmargin)
        glEnd()
        return

    def route(self):
        sz = 20
        x, y = self.pos[0], self.pos[1]
        map = self.xMap[x] if self.dir & 1 else self.yMap[y]
        p = y if self.dir & 1 else x

        for idx, segment in enumerate(map):
            if p < segment[0] - 1:
                map.insert(idx, [p, p])
                break
            if p == segment[0] - 1:
                segment[0] -= 1
                break
            if segment[0] <= p and p <= segment[1]:
                break
            if p == segment[1] + 1:
                segment[1] += 1
                break

        if not len(map):
            map.append([p, p])
        elif p > map[-1][1]:
            map.append([p, p])

        for idx in range(len(map) - 1):
            if map[idx][1] + 1 >= map[idx + 1][0]:
                map[idx][1] = map[idx + 1][1]
                del map[idx + 1]
                break

        # Draw rectangles
        for key in self.xMap:
            for segment in self.xMap[key]:
                self.mapdraw(key, segment, False)
        for key in self.yMap:
            for segment in self.yMap[key]:
                self.mapdraw(key, segment, True)

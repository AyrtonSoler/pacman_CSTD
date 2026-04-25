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
        self.route()    # <--
        for key in self.xMap:
            print(len(self.xMap[key]), end = ' ')
        print()
        for key in self.yMap:
            print(len(self.yMap[key]), end = ' ')
        print()
        print()
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
        shift, lmargin, rmargin = 15, 15, 25
        if horizontal:
            glVertex2d(segment[0] + shift, key + lmargin)
            glVertex2d(segment[1] + shift, key + lmargin)
            glVertex2d(segment[1] + shift, key + rmargin)
            glVertex2d(segment[0] + shift, key + rmargin)
        else:
            glVertex2d(key + lmargin, segment[0] + shift)
            glVertex2d(key + lmargin, segment[1] + shift)
            glVertex2d(key + rmargin, segment[1] + shift)
            glVertex2d(key + rmargin, segment[0] + shift)
        glEnd()
        return

    def route(self):
        x = self.pos[0]
        y = self.pos[1]
        sz = 20 if self.dir & 2 else 0
        if self.dir & 1:
            for idx, segment in enumerate(self.xMap[x]):
                # Insert segment before
                if y < segment[0] - 1:
                    self.xMap[x].insert(idx, [y, y])
                    break
                # Coords belong to this segment
                if y == segment[0] - 1:
                    segment[0] -= 1
                    # Join with prev
                    if(idx > 0):
                        if(self.xMap[x][idx - 1][1] >= segment[0]):
                            self.xMap[x][idx - 1][1] = segment[1]
                            del self.xMap[x][idx]
                    break
                if y == segment[1] + 1:
                    segment[1] += 26
                    # Join with next
                    if(idx < len(self.xMap[x]) - 1):
                        if(segment[1] >= self.xMap[x][idx + 1][0]):
                            self.xMap[x][idx][1] = self.xMap[x][idx + 1][1]
                            del self.xMap[x][idx + 1]
                    break
                if y >= segment[0] and y <= segment[1]:
                    break
            # Insert segment after
            if len(self.xMap[x]) == 0:
                self.xMap[x].append([y, y])
            elif y > self.xMap[x][-1][1] + 1:
                self.xMap[x].append([y, y])
        else:
            for idx, segment in enumerate(self.yMap[y]):
                # Insert segment before
                if x < segment[0] - 1:
                    self.yMap[y].insert(idx, [x, x])
                    break
                # Coords belong to this segment
                if x == segment[0] - 1:
                    segment[0] -= 1
                    # Join with prev
                    if(idx > 0):
                        if(self.yMap[y][idx - 1][1] >= segment[0]):
                            self.yMap[y][idx - 1][1] = segment[1]
                            del self.yMap[y][idx]
                    break
                if x == segment[1] + 1:
                    segment[1] += 26
                    # Join with next
                    if(idx < len(self.yMap[y]) - 1):
                        if(segment[1] >= self.yMap[y][idx + 1][0]):
                            self.yMap[y][idx][1] = self.yMap[y][idx + 1][1]
                            del self.yMap[y][idx + 1]
                    break
                if x > segment[0] and x < segment[1]:
                    break
            # Insert segment after
            if len(self.yMap[y]) == 0:
                self.yMap[y].append([x, x])
            elif x > self.yMap[y][-1][1] + 1:
                self.yMap[y].append([x, x])
        # Draw rectangles
        for key in self.xMap:
            for segment in self.xMap[key]:
                self.mapdraw(key, segment, False)
        for key in self.yMap:
            for segment in self.yMap[key]:
                self.mapdraw(key, segment, True)

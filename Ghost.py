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

    #Dumb ghost
    def follow(self, pacmanXY):
        #Nodes arent regular, needs translation to px
        xMC = [0, 30, 71, 114, 156, 199, 242, 286, 328, 358]
        yMC = [0, 51, 90, 130, 168, 208, 244, 282, 320, 360]
        x = self.XPxToMC[self.pos[0]]
        y = self.YPxToMC[self.pos[1]]
        
        #Check intersection
        if(x >= 0 and y >= 0):
            # Get possible options
            options = []
            for i in range(4):
                if self.MC[y][x] & 2 ** (i):
                    options.append(i + 1)
            # Delete returns (if another option exists)
            go_back = self.dir - 2 if self.dir - 2 > 0 else self.dir + 2
            if len(options) > 1:
                options.remove(go_back)
            #Calculate future positions
            future_nodes = []
            for i in options:
                fx, fy = x, y
                match i:
                    case 1:         # UP
                        fy -= 1
                    case 2:         #RIGHT
                        fx += 1
                    case 3:         #DOWN
                        fy += 1
                    case 4:         #LEFT
                        fx -= 1

                future_nodes.append((fx, fy))
            #Calculate distance
            distance = []
            for (fx, fy) in future_nodes:
                #translate node to Pixels (like the movie [Adam Sandler, 2015])
                px = xMC[fx]
                py = yMC[fy]
                #Manhattan
                d = abs(pacmanXY[0] - px) + abs(pacmanXY[1] - py)
                #euclidian
                #d = (pacmanXY[0] - px)**2 + (pacmanXY[1] - py)**2
                print(d)
                distance.append(d)
            # Choose
            min_distance = min(distance)
            #tie
            candidates = []
            for i in range(len(distance)):
                if distance[i] == min_distance:
                    candidates.append(options[i])
            self.dir = choice(candidates)
            
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


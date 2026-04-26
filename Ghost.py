#—–—————————————————— Team —–——————————————————#
# Franco De Escondrillas Vázquez | A01739410
# Victor Ayrton Urrutia Soler | A01739157
# Octavio Hernández Loyo | A01739304
# Enrique Jiménez Cruz | A01739769
# April 25th, 2026


#—————————————————— IMPORTS –——————————————————#
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from random import choice
from OpenGL.extensions import CURRENT_GL_VERSION
import pandas as pd
import numpy as np
import heapq
import math
import os

#——————————————————— CLASS —–——————————————————#
class Ghost:
    def __init__(self, mc, xMCtoPx, yMCtoPx, xPXtoMC, yPXtoMC, type):
        self.cur_edge = [0, 0]      # edge the ghost is taking
        self.xMCtoPx = xMCtoPx      # x-coords to pixels
        self.yMCtoPx = yMCtoPx      # y-coords to pixels
        self.xPXtoMC = xPXtoMC      # pixels to x-coords
        self.yPXtoMC = yPXtoMC      # pixels to y-coords
        self.pos = [180, 165]       # starting position
        self.type = type            # ghost type
        self.bounce = 1             # beginning idle
        self.size = 20              # draw size
        self.dir = 1                # moving direction
        self.MC = mc                # control matrix

#————————————————— FUNCTIONS ——————————————————#
    def loadTextures(self, textures):
        self.textures = textures

    def update(self, pacman, ghost1, ghost2):
        # Go out of the box
        if(self.pos[0] == 180 and self.pos[1] == 130 and self.dir == 1):
            self.dir = choice([2, 4]) # Go left or right randomly
            self.cur_edge = [43, 53] if self.dir & 2 else [53, 43]
            return
        # Move with an algorithm
        match self.type:
            case 0:
                self.follow(pacman)
            case 1:
                self.random()
            case 2:
                self.hunt(pacman, ghost2)
            case 3:
                self.hunt(pacman, ghost1)

    def vibe(self):
        if self.pos[0] == 210:
            self.bounce = -1
        if self.pos[0] == 150:
            self.bounce = 1
        # Move
        self.pos[0] += self.bounce
        return

    def random(self):
        # Get MC coords
        x = self.xPXtoMC[self.pos[0]]
        y = self.yPXtoMC[self.pos[1]]
        # Check intersection
        if(x >= 0 and y >= 0):
            # Get possible options
            options = []
            for i in range(4):
                if self.MC[y][x] & (1 << i):
                    options.append(i + 1)
            # Delete returns (if another option exists)
            if len(options) > 1:
                options.remove(self.dir - 2 if self.dir - 2 > 0 else self.dir + 2)
            # Choose
            self.dir = choice(options)
        # Move
        self.pos[(self.dir & 1)] += 1 if (self.dir & 2) else -1
        return

    def follow(self, pacman):
        # Get MC coords
        x = self.xPXtoMC[self.pos[0]]
        y = self.yPXtoMC[self.pos[1]]
        #Check intersection
        if(x >= 0 and y >= 0):
            # Get possible options
            options = []
            for i in range(4):
                if self.MC[y][x] & (2 ** i):
                    options.append(i + 1)
            # Delete returns (if another option exists)
            go_back = self.dir - 2 if self.dir - 2 > 0 else self.dir + 2
            if len(options) > 1:
                options.remove(go_back)
            best_c = options[0]
            best_d = 1e9
            #Calculate future positions
            for i in options:
                nx, ny = x, y
                if i == 1:
                    ny -= 1
                elif i == 2:
                    nx += 1
                elif i == 3:
                    ny += 1
                elif i == 4:
                    nx -= 1

                d = (pacman.pos[0] - self.xMCtoPx[nx]) ** 2 + (pacman.pos[1] - self.yMCtoPx[ny]) ** 2
                if(d < best_d):
                    best_c = i
                    best_d = d
            self.dir = best_c
        # Move
        self.pos[(self.dir & 1)] += 1 if (self.dir & 2) else -1
        return


    def hunt(self, pacman, ghost):
        # Get MC coords
        x = self.xPXtoMC[self.pos[0]]
        y = self.yPXtoMC[self.pos[1]]
        # If intersection, choose with A*
        if(x >= 0 and y >= 0):
            self.dir = self.a_star([x, y], pacman, ghost)
        # Move
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

#————————————————— ALGORITHMS —————————————————#
    # Returns the best movement direction using A* algorithm
    def a_star(self, pos, pacman, ghost):
        # Nodes represented as [priority, x_coord, y_coord, parent]
        start = [0, pos[0], pos[1], -1]
        current = start
        open = [start]
        parent = {}
        close = []
        # Criteria: node is adjacent and is not the start
        while not self.adj(pacman.pos, current) or current == start:
            current = heapq.heappop(open)
            if self.node_id(current) in close:
                continue
            close.append(self.node_id(current))
            parent[self.node_id(current)] = current[3]
            # Get neighbours
            neighbours = []
            for i in range(4):
                if self.MC[current[2]][current[1]] & (1 << i):
                    dir = 1 if ((i + 1) & 2) else -1
                    if((i + 1) & 1):    # Vertical
                        neighbours.append([0, current[1], current[2] + dir, self.node_id(current)])
                    else:
                        neighbours.append([0, current[1] + dir, current[2], self.node_id(current)])
            # Calculate weights for all neighbours
            for neighbour in neighbours:
                # Check if already visited
                if self.node_id(neighbour) in close:
                    continue
                # Get coords in pixels for current node and neighbours
                current_coords = [self.xMCtoPx[current[1]], self.yMCtoPx[current[2]]]
                next_coords = [self.xMCtoPx[neighbour[1]], self.yMCtoPx[neighbour[2]]]
                # Get distances to pacman, ghost and moving cost
                d_pacman = self.manhattan_dist(pacman.pos, next_coords)
                cost = self.manhattan_dist(neighbour, current_coords)
                # Compute weight, avoiding going back and following the other ghost path
                if([self.node_id(neighbour), self.node_id(current)] == self.cur_edge):
                    neighbour[0] = 1e9
                elif([self.node_id(current), self.node_id(neighbour)] == ghost.cur_edge):
                    neighbour[0] = 1e8
                else:
                    neighbour[0] = cost + d_pacman
                heapq.heappush(open, neighbour)
        # Reconstruct path
        start = self.node_id(start)
        current = self.node_id(current)
        while parent.get(current) != start:
            current = parent[current]
        # Avoid going back
        self.cur_edge = [start, current]
        if current == start - 1:
            return 1
        if current == start + 10:
            return 2
        if current == start + 1:
            return 3
        return 4

    def manhattan_dist(self, obj1, obj2):
        return abs(obj1[0] - obj2[0]) + abs(obj1[1] - obj2[1])

    def node_id(self, node):
        return 10 * node[1] + node[2]

    # Determines if the pacman is in a tunnel adjacent to the node
    def adj(self, pacman, node):
        xMC, yMC = node[1], node[2]
        # Get neighbours
        neighbours = []
        for i in range(4):
            if self.MC[yMC][xMC] & 2 ** (i):
                neighbours.append(i + 1)
        # Check if pacman is between node and any neighbour
        for n in neighbours:
            dir = 1 if (n & 2) else -1
            if (n & 1):     # Vertical
                is_between = (self.yMCtoPx[yMC] - pacman[1]) * (self.yMCtoPx[yMC + dir] - pacman[1]) <= 0 and self.xMCtoPx[xMC] == pacman[0]
                if is_between:
                    return True
            else:           # Horizontal
                is_between = (self.xMCtoPx[xMC] - pacman[0]) * (self.xMCtoPx[xMC + dir] - pacman[0]) <= 0 and self.yMCtoPx[yMC] == pacman[1]
                if is_between:
                   return True
        return False

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
    def __init__(self, mc, xMCtoPX, yMCtoPX, xPXtoMC, yPXtoMC, type):
        self.xMCtoPX = xMCtoPX      # x-coords to pixels
        self.yMCtoPX = yMCtoPX      # y-coords to pixels
        self.xPXtoMC = xPXtoMC      # pixels to x-coords
        self.yPXtoMC = yPXtoMC      # pixels to y-coords
        self.pos = [180, 165]       # starting position
        self.alpha = 0.7            # aggressiveness
        self.type = type            # ghost type
        self.bounce = 1             # beginning idle
        self.size = 20              # draw size
        self.dir = 1                # moving direction
        self.MC = mc                # control matrix

#————————————————— FUNCTIONS ——————————————————#
    def loadTextures(self, textures):
        self.textures = textures

    def update(self, pacman, ghost1, ghost2):
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
        # Go of the box
        if(self.pos[0] == 180 and self.pos[1] == 130 and self.dir == 1):
            self.dir = choice([2, 4])
        # Get MC coords
        x = self.xPXtoMC[self.pos[0]]
        y = self.yPXtoMC[self.pos[1]]
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
        self.pos[(self.dir & 1)] += 1 if (self.dir & 2) else -1
        return

    def follow(self, pacmanXY):
        # Go out of the box
        if(self.pos[0] == 180 and self.pos[1] == 130 and self.dir == 1):
            self.dir = choice([2, 4])
        # Get MC coords
        x = self.xPXtoMC[self.pos[0]]
        y = self.yPXtoMC[self.pos[1]]

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
                px = self.xPXtoMC[fx]
                py = self.yPXtoMC[fy]
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


    def hunt(self, pacmanXY, ghostXY):
        # Go of the box
        if(self.pos[0] == 180 and self.pos[1] == 130 and self.dir == 1):
            self.dir = choice([2, 4])
        # Get MC coords
        x = self.xPXtoMC[self.pos[0]]
        y = self.yPXtoMC[self.pos[1]]
        # If intersection, choose with A*
        if(x >= 0 and y >= 0):
            self.dir = self.a_star([x, y], pacmanXY, ghostXY)
        # Move
        if not self.dir:
            return
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
        a = 0
        # Criteria: node is adjacent and is not the start
        while not self.adj(pacman, current) or current == start:
            current = heapq.heappop(open)
            close.append(self.node_id(current))
            parent[self.node_id(current)] = current[3]
            # Get neighbours
            neighbours = []
            for i in range(4):
                if self.MC[current[2]][current[1]] & 2 ** (i):
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
                current_coords = [self.xMCtoPX[current[1]], self.yMCtoPX[current[2]]]
                neighbour_coords = [self.xMCtoPX[neighbour[1]], self.yMCtoPX[neighbour[2]]]
                # Get distances to pacman, ghost and moving cost
                d_pacman = self.manhattan_dist(pacman, neighbour_coords)
                d_ghost = self.manhattan_dist(ghost, neighbour_coords)
                cost = self.manhattan_dist(neighbour, current_coords)
                # Compute weight
                neighbour[0] = cost + self.alpha * d_pacman - (1.0 - self.alpha) * d_ghost
                heapq.heappush(open, neighbour)

        # Reconstruct path
        start = self.node_id(start)
        current = self.node_id(current)
        while parent.get(current) != start:
            current = parent[current]

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
                is_between = (self.yMCtoPX[yMC] - pacman[1]) * (self.yMCtoPX[yMC + dir] - pacman[1]) <= 0 and self.xMCtoPX[xMC] == pacman[0]
                if is_between:
                    return True
            else:           # Horizontal
                is_between = (self.xMCtoPX[xMC] - pacman[0]) * (self.xMCtoPX[xMC + dir] - pacman[0]) <= 0 and self.yMCtoPX[yMC] == pacman[1]
                if is_between:
                   return True
        return False

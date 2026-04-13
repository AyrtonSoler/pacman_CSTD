#—————————————————— IMPORTS –——————————————————#
import pygame
from pygame.locals import *

# OpenGL libraries
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pandas as pd
import numpy as np
import math
import os

# Files
import sys
sys.path.append('..')
from Pacman import Pacman
#from Ghost import Ghost

#—————————————— GLOBAL VARIABLES ——————————————#
screen_height = 800
screen_width = 800

X_MIN = -500
X_MAX = 500
Y_MIN = -500
Y_MAX = 500

# Key stack
key_stack = []

# Plane dimensions
DimBoard = 400

# List for texture handling
textures = []

# File names
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
file_1 = os.path.join(BASE_PATH, 'mapa.bmp')
img_pacman = os.path.join(BASE_PATH, 'pacman.bmp')
img_ghost1 = os.path.join(BASE_PATH, 'fantasma1.bmp')
img_ghost2 = os.path.join(BASE_PATH, 'fantasma2.bmp')
img_ghost3 = os.path.join(BASE_PATH, 'fantasma3.bmp')
img_ghost4 = os.path.join(BASE_PATH, 'fantasma4.bmp')


file_csv = os.path.join(BASE_PATH, 'mapa.csv')
matrix = np.array(pd.io.parsers.read_csv(file_csv, header = None)).astype("int")

# Control matrix
MC = [
    [6, 10, 14, 10, 12, 6, 10, 14, 10, 12],
    [7, 10, 15, 14, 11, 11, 14, 15, 10, 13],
    [3, 10, 13, 3, 12, 6, 9, 7, 10, 9],
    [0, 0, 5, 6, 11, 11, 12, 5, 0, 0],
    [2, 10, 15, 13, 10, 10, 7, 15, 10, 8],
    [0, 0, 5, 7, 10, 10, 13, 5, 0, 0],
    [6, 10, 15, 11, 12, 6, 11, 15, 10, 12],
    [3, 12, 7, 14, 11, 11, 14, 13, 6, 9],
    [6, 11, 9, 3, 12, 6, 9, 3, 11, 12],
    [3, 10, 10, 10, 11, 11, 10, 10, 10, 9],
]

xMC = [0, 30, 71, 114, 156, 199, 242, 286, 328, 358]
yMC = [0, 51, 90, 130, 168, 208, 244, 282, 320, 360]
XPxToMC = np.full(361, -1, dtype=int)
YPxToMC = np.full(361, -1, dtype=int)

XPxToMC[0] = 0
XPxToMC[30] = 1
XPxToMC[71] = 2
XPxToMC[114] = 3
XPxToMC[156] = 4
XPxToMC[199] = 5
XPxToMC[242] = 6
XPxToMC[286] = 7
XPxToMC[328] = 8
XPxToMC[358] = 9

YPxToMC[0] = 0
YPxToMC[51] = 1
YPxToMC[90] = 2
YPxToMC[130] = 3
YPxToMC[168] = 4
YPxToMC[208] = 5
YPxToMC[244] = 6
YPxToMC[282] = 7
YPxToMC[320] = 8
YPxToMC[360] = 9

# Pathfinding variables
path = []
grid = []

# Pacman
pc = Pacman(matrix, MC, XPxToMC, YPxToMC)
#fantasmas
# ghosts = []

#————————————————— FUNCTIONS ——————————————————#
def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    glLineWidth(1.0)

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image,"RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)

def Init():
    screen = pygame.display.set_mode(
        (400, 400), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,400,400,0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0,0,0,0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    #textures[0]: plano
    Texturas(file_1)
    textures[1]: pacman
    Texturas(img_pacman)
    #textures[2]: fantasma1
    Texturas(img_ghost1)
    #textures[3]: fantasma2
    Texturas(img_ghost2)
    #textures[4]: fantasma3
    Texturas(img_ghost3)
    #textures[5]: fantasma4
    Texturas(img_ghost4)
    #se pasan las texturas a los objetos
    pc.loadTextures(textures,1)
    # ghosts[0].loadTextures(textures,2)
    # ghosts[1].loadTextures(textures,3)
    # ghosts[2].loadTextures(textures,4)
    # ghosts[3].loadTextures(textures,5)

def PlanoTexturizado():
    # Activate textures
    glColor3f(1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)
    # Front face
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2d(0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex2d(0, DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex2d(DimBoard, DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex2d(DimBoard, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def display(keys):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    PlanoTexturizado()
    dir = 0
    if(keys == pygame.K_UP):
        dir = 1
    if(keys == pygame.K_RIGHT):
        dir = 2
    if(keys == pygame.K_DOWN):
        dir = 3
    if(keys == pygame.K_LEFT):
        dir = 4
    pc.update(dir)
    pc.draw()
    #for g in ghosts:
    #    g.draw()
    #    g.update2(pc.position)

#———————————————————— MAIN ————————————————————#
last_key = None
pygame.init()
counter = 0
run = True
Init()

while run:
    # Keyboard input
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pressed = event.key
            key_stack.append(pressed)
            # Exit case
            if pressed == pygame.K_ESCAPE:
                run = False

    # Clean stack
    keys = pygame.key.get_pressed()
    while key_stack and not keys[key_stack[-1]]:
        key_stack.pop()
    # Update and display game
    if key_stack:
       last_key = key_stack[-1]
       counter = 0
    counter += 1
    display(key_stack[-1] if key_stack else last_key)
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()

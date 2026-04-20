#—————————————————— IMPORTS –——————————————————#
import pygame
from pygame.locals import *

# OpenGL libraries
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

# Other libraries
from math import sqrt
import numpy as np
import sys
import os

# Files
from Pacman import Pacman
from Ghost import Ghost
sys.path.append('..')

#—————————————— GLOBAL VARIABLES ——————————————#
dim_board = 400 # Plane dimensions
textures = []   # List for texture handling
offset = 0      # Timer for releasing ghosts

# Dictionary for binding keys to directions
directions = {
    pygame.K_UP:    1,
    pygame.K_RIGHT: 2,
    pygame.K_DOWN:  3,
    pygame.K_LEFT:  4,
}

# File names
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
img_ghost1 = os.path.join(BASE_PATH, 'fantasma1.bmp')
img_ghost2 = os.path.join(BASE_PATH, 'fantasma2.bmp')
img_ghost3 = os.path.join(BASE_PATH, 'fantasma3.bmp')
img_ghost4 = os.path.join(BASE_PATH, 'fantasma4.bmp')
img_pacman = os.path.join(BASE_PATH, 'pacman.bmp')
file_1 = os.path.join(BASE_PATH, 'mapa.bmp')

# Control matrix
MC = [
    [ 6, 10, 14, 10, 12,  6, 10, 14, 10, 12],
    [ 7, 10, 15, 14, 11, 11, 14, 15, 10, 13],
    [ 3, 10, 13,  3, 12,  6,  9,  7, 10,  9],
    [ 0,  0,  5,  6, 11, 11, 12,  5,  0,  0],
    [ 2, 10, 15, 13, 10, 10,  7, 15, 10,  8],
    [ 0,  0,  5,  7, 10, 10, 13,  5,  0,  0],
    [ 6, 10, 15, 11, 12,  6, 11, 15, 10, 12],
    [ 3, 12,  7, 14, 11, 11, 14, 13,  6,  9],
    [ 6, 11,  9,  3, 12,  6,  9,  3, 11, 12],
    [ 3, 10, 10, 10, 11, 11, 10, 10, 10,  9],
]

xMC = [0, 30, 71, 114, 156, 199, 242, 286, 328, 358]
yMC = [0, 51, 90, 130, 168, 208, 244, 282, 320, 360]

XPxToMC = np.full(361, -1, dtype = int)
for idx, coord in enumerate(xMC):
    XPxToMC[coord] = idx

YPxToMC = np.full(361, -1, dtype = int)
for idx, coord in enumerate(yMC):
    YPxToMC[coord] = idx

# Pacman
pacman = Pacman(MC, XPxToMC, YPxToMC)

# Ghosts
ghosts = []
for type in range(4):
    ghosts.append(Ghost(MC, xMC, yMC, XPxToMC, YPxToMC, type))

#————————————————— FUNCTIONS ——————————————————#
def Textures(filepath):
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
    screen = pygame.display.set_mode((400, 400), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,400,400,0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0,0,0,0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    Textures(file_1)        # textures[0]: plane
    Textures(img_pacman)    # textures[1]: pacman
    Textures(img_ghost1)    # textures[2]: ghost 1
    Textures(img_ghost2)    # textures[3]: ghost 2
    Textures(img_ghost3)    # textures[4]: ghost 3
    Textures(img_ghost4)    # textures[5]: ghost 4
    # Load textures to each object
    pacman.loadTextures(textures[1])
    for i in range(4):
        ghosts[i].loadTextures(textures[5 - i])

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
    glVertex2d(0, dim_board)
    glTexCoord2f(1.0, 1.0)
    glVertex2d(dim_board, dim_board)
    glTexCoord2f(1.0, 0.0)
    glVertex2d(dim_board, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def display(key):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    PlanoTexturizado()

    pacman.update(dir)
    pacman.draw()

    for i, g in enumerate(ghosts):
        if(offset >=
            20 * i):
            g.update(pacman.pos, ghosts[2].pos, ghosts[3].pos) if offset >= 320 * i else g.vibe()
        g.draw()

#———————————————————— MAIN ————————————————————#
pygame.init()
last_key = 0
run = True
Init()

while run:
    # Keyboard input
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            last_key = event.key
            # Exit case
            if last_key == pygame.K_ESCAPE:
                run = False
    # Display
    dir = directions.get(last_key, 0)
    display(dir)
    pygame.display.flip()
    pygame.time.wait(10)
    offset += 1
    # Collision
    for g in ghosts:
        if sqrt((pacman.pos[0] - g.pos[0])**2 + (pacman.pos[1] - g.pos[1])**2) < 18:
            print("\033[H\033[2JGame Over")
            run = False

pygame.quit()

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
    def __init__(self,mapa, mc, x_mc, y_mc):
        #Matriz de control que almacena los IDs de las intersecciones
        self.MC = mc
        #Vectores que almacenan las coordenadas 
        self.XPxToMC = x_mc
        self.YPxToMC = y_mc
        #se resplanda el mapa en terminos de pixeles
        self.mapa = mapa
 si el pacman se encuentra en estado inicial del juego
        self.start = 1      
        
    def loadTextures(self, texturas, id):
        self.texturas = texturas
        self.Id = id
        
    def update(self, dir):

                 
    def draw(self):
  

import pygame
from constants import *

def make_game_window():
    gwindow = pygame.display.set_mode((GRID_LENGTH*2, GRID_LENGTH))
    gwindow.fill(WHITE)
    pygame.display.update()
    pygame.display.set_caption("Assignment 1: FOG OF WAR PATHFINDER")
    return gwindow

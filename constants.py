import pygame
GREEN = (0, 255, 0) # EXPANDED
YELLOW = (255, 255, 0) # START
PATH = (0, 255, 255) # FINAL PATH 
RED = (255, 0, 0) # IN FRONTIER
BLUE = (0, 0, 255) #END
WHITE = (255, 255,255) #STANDARD
BLACK = (0,0,0) # BLOCKED
GREY = (127,127,127)#UNEXPANDED




ROWS = 101
NODE_LENGTH = 5

GRID_LENGTH = NODE_LENGTH*ROWS
WINDOW = pygame.display.set_mode((GRID_LENGTH*2+NODE_LENGTH, GRID_LENGTH))
WINDOW.fill(WHITE)

pygame.display.update()
pygame.display.set_caption("Assignment 1: FOG OF WAR PATHFINDER")

START_NODE = (0,0)
END_NODE = (ROWS-1,ROWS-1)
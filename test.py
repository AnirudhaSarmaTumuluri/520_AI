from math import inf
import pygame
import math
import random

from astar import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255,255)
BLACK = (0,0,0)


ROWS = 101
WIDTH = 808

WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Assignment 1: FOG OF WAR PATHFINDER")

class GridNode:
    def __init__(self, row, col, width, total_rows, blocked=False):
        self.row = row
        self.col = col
        self.blocked = blocked
        if blocked:
            self.color = BLACK
        else:
            self.color = WHITE
        self.x = row*(width)
        self.y = col*width
        
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return (self.row, self.col)

    def set_color(self, color):
        if color==BLACK:
            self.blocked = True
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


def make_grid(rows, width, start, end):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            
            if random.randint(0,10)%4==0:
                grid[i].append(GridNode(i,j,gap,rows,True))
            else:
                grid[i].append(GridNode(i, j, gap, rows))
    grid[start[0]][start[1]] = GridNode(i,j,gap, rows)
    grid[end[0]][end[1]] = GridNode(i,j,gap, rows)
    grid[end[0]][end[1]].set_color(GREEN)
    return grid

def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i*gap), (width, i*gap))

    for i in range(rows):
        pygame.draw.line(win, BLACK, (i*gap, 0), (i*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for gridnode in row:
            gridnode.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def main(win,width):
    grid = [[0 for _ in range(ROWS)] for x in range(ROWS)]
    start = [0,0]
    end = [20,20]
    window_grid = make_grid(ROWS, WIDTH,start,end)
    

    #window_grid[end[0]][end[1]].set_color = WHITE
    #window_grid[end[0]][end[1]].blocked = False

    openset = []
    openset.append(start)
    camefrom = grid

    gcost = [[inf for _ in range(ROWS)] for x in range(ROWS)]
    gcost[start[0]][start[1]] = 0

    fcost = [[inf for _ in range(ROWS)] for x in range(ROWS)]
    fcost[start[0]][start[1]] = h(start[0], start[1], end, grid)


    run = True
    started = True
    i = 0
    while run:

        if started:
            draw(win, window_grid, ROWS, width)
            while len(openset)!=0:
                current = findLowest(openset, fcost)
                if current == end:
                    print("REACHED")
                    window_grid[current[0]][current[1]].set_color(GREEN)
                    started = False
                    break
                #print()
                #print('Current:', current)
                #print('Openset:', openset)
                #print()
                openset.remove(current)
                
                for neighbor in give_neighbors(current, len(grid)):
                    if window_grid[neighbor[0]][neighbor[1]].blocked:
                        continue
                    G = gcost[current[0]][current[1]] + 1
                    if G<gcost[neighbor[0]][neighbor[1]]:
                        gcost[neighbor[0]][neighbor[1]] = G
                        fcost[neighbor[0]][neighbor[1]] = G + h(neighbor[0], neighbor[1], end, grid)
                        if neighbor not in openset:
                            openset.append(neighbor)
                            #print(neighbor[0], neighbor[1])
                            #print(window_grid[neighbor[0]][neighbor[1]])
                            window_grid[neighbor[0]][neighbor[1]].set_color(RED)
                            draw(win, window_grid, ROWS, width)

        draw(win, window_grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue
    pygame.quit()


main(WINDOW, WIDTH)
    

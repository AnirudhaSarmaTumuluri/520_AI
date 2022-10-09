from queue import PriorityQueue as PQ
import random
import pygame
from math import inf
import time
from constants import *
from maze_gen_test import make_maze

actual_grid = make_maze()
display_grid = actual_grid
agent_grid = [[GREY for _ in range(ROWS)] for x in range(ROWS)]
agent_grid[-1][-1] = BLUE

###def draw_lines_GLOBAL():
    #for i in range(ROWS):
        #pygame.draw.line(WINDOW, BLACK, (0, i*NODE_LENGTH), (GRID_LENGTH*2+NODE_LENGTH, i*NODE_LENGTH))   
    #for i in range(ROWS+1):
        #pygame.draw.line(WINDOW, BLACK, (i*NODE_LENGTH, 0), (i*NODE_LENGTH, GRID_LENGTH))
    #for i in range(ROWS):
        #pygame.draw.line(WINDOW, BLACK, (i*NODE_LENGTH+GRID_LENGTH+NODE_LENGTH, 0), (i*NODE_LENGTH+GRID_LENGTH+NODE_LENGTH, GRID_LENGTH))



#draw_lines_GLOBAL()

def draw_colors_GLOBAL():
    for i in range(ROWS):
        for j in range(ROWS):
            pygame.draw.rect(WINDOW, display_grid[i][j], (i*NODE_LENGTH+1, j*NODE_LENGTH+1, NODE_LENGTH, NODE_LENGTH))
            pygame.draw.rect(WINDOW, agent_grid[i][j], (i*NODE_LENGTH+GRID_LENGTH+NODE_LENGTH+1, j*NODE_LENGTH+1, NODE_LENGTH, NODE_LENGTH))

def update_frame():
    draw_colors_GLOBAL()
    pygame.display.update()

def give_neighbors_update(NODE):
    retval = []
    i,j = NODE[0], NODE[1]
    if j-1>=0:
        retval.append((i, j-1))
    if j+1<ROWS:
        retval.append((i, j+1))
    if i-1>=0:
        retval.append((i-1, j))
    if i+1<ROWS:
        retval.append((i+1, j))
    return retval

def init_agent_grid():
    global agent_grid
    agent_grid = [[GREY for _ in range(ROWS)] for x in range(ROWS)]
    agent_grid[START_NODE[0]][START_NODE[1]] = YELLOW
    agent_grid[END_NODE[0]][END_NODE[1]] = BLUE
    neighbors = give_neighbors_update(START_NODE)
    for neighbor in neighbors:
        agent_grid[neighbor[0]][neighbor[1]] = display_grid[neighbor[0]][neighbor[1]]
    update_frame()

def set_start(i,j):
    global START_NODE
    display_grid[START_NODE[0]][START_NODE[1]] = WHITE #Make old start white
    display_grid[i][j] = YELLOW #color the new start node
    agent_grid[START_NODE[0]][START_NODE[1]] = GREY
    agent_grid[i][j] = YELLOW
    START_NODE = (i,j)
    update_frame()
set_start(START_NODE[0], START_NODE[1])

def set_end(i,j):
    global END_NODE
    display_grid[END_NODE[0]][END_NODE[1]] = WHITE
    display_grid[i][j] = BLUE
    agent_grid[END_NODE[0]][END_NODE[1]] = GREY
    agent_grid[i][j] = BLUE
    END_NODE = (i,j)
    update_frame()
set_end(END_NODE[0], END_NODE[1])
init_agent_grid()

def set_blocked(i,j):
    if ((i,j)!=START_NODE) & ((i,j)!=END_NODE):
        display_grid[i][j] = BLACK
        update_frame()

def set_unblocked(i,j):
    if ((i,j)!=START_NODE) & ((i,j)!=END_NODE):
        display_grid[i][j] = WHITE
        update_frame()

def hcost(NODE):
    return abs(END_NODE[0]-NODE[0])+abs(END_NODE[1]-NODE[1])

def makepath(camefrom, current, start):
    total_path = []
    while current!=start:
        total_path.append(current)
        current = camefrom[current[0]][current[1]]
    
    total_path.append(START_NODE)
    return total_path

def give_neighbors_agent(NODE):
    retval = []
    i,j = NODE[0], NODE[1]
    if j-1>=0:
        if agent_grid[i][j-1]!=BLACK:
            retval.append((i, j-1))
    if j+1<ROWS:
        if agent_grid[i][j+1]!=BLACK:
            retval.append((i, j+1))
    if i-1>=0:
        if agent_grid[i-1][j]!=BLACK:
            retval.append((i-1, j))
    if i+1<ROWS:
        if agent_grid[i+1][j]!=BLACK:
            retval.append((i+1, j))
    return retval


gcost = [[inf for _ in range(ROWS)] for x in range(ROWS)]
fcost = [[inf for _ in range(ROWS)] for x in range(ROWS)]   
def astar_agent(start):
    openset = PQ()
    openset.put((hcost(start), start))
    gcost[start[0]][start[1]] = 0
    fcost[start[0]][start[1]] = hcost(start)
    camefrom = [[None for _ in range(ROWS)] for x in range(ROWS)]
    while not openset.empty():
        choice = openset.get()
        choice = choice[1]
        if choice==END_NODE:
            path = makepath(camefrom, END_NODE, start)
            updates = give_neighbors_update(path[-2])
            for node in updates:
                if agent_grid[node[0]][node[1]]!=PATH:
                    agent_grid[node[0]][node[1]] = actual_grid[node[0]][node[1]]
            update_frame()
            return True, path[-2]
        
        for neighbor in give_neighbors_agent(choice):
            G = gcost[choice[0]][choice[1]]+1
            if G<gcost[neighbor[0]][neighbor[1]]:
                camefrom[neighbor[0]][neighbor[1]] = (choice)
                gcost[neighbor[0]][neighbor[1]] = G
                fcost[neighbor[0]][neighbor[1]] = G+hcost(neighbor)
                if neighbor not in openset.queue:
                    openset.put((fcost[neighbor[0]][neighbor[1]], neighbor))

    return False, None

def repeated_astar(start, target):
    while start!=target:
        ans, next_step = astar_agent(start)
        if ans:
            display_grid[start[0]][start[1]] = WHITE
            agent_grid[start[0]][start[1]] = PATH
            start = next_step
            print('Current_location:', start)
            display_grid[start[0]][start[1]] = YELLOW
            agent_grid[start[0]][start[1]] = WHITE
            #time.sleep(0.1)
        else:
            return False
    return True
            
def SE_PHASE(active):
    se_phase = True
    while se_phase&active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                break
             
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]: #Tracks left click
                    position = pygame.mouse.get_pos()
                    i = (position[0]//NODE_LENGTH)
                    j = (position[1]//NODE_LENGTH)
                    if (i<ROWS)&(j<ROWS):
                        if not ((actual_grid[i][j]==BLACK)or(actual_grid[i][j]==BLUE)):
                            set_start(i,j)
                            init_agent_grid()

                if mouse_presses[2]: #Tracks Right click
                    position = pygame.mouse.get_pos()
                    i = (position[0]//NODE_LENGTH)
                    j = (position[1]//NODE_LENGTH)
                    if (i<ROWS)&(j<ROWS):
                        if not ((actual_grid[i][j]==BLACK)or(actual_grid[i][j]==YELLOW)):
                            set_end(i,j)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    position = pygame.mouse.get_pos()
                    i = (position[0]//NODE_LENGTH)
                    j = (position[1]//NODE_LENGTH)
                    set_start(i,j)
                    #print("Start point has been changed to:", (i,j))

                if event.key == pygame.K_e:
                    position = pygame.mouse.get_pos()
                    i = (position[0]//NODE_LENGTH)
                    j = (position[1]//NODE_LENGTH)
                    set_end(i,j)
                    #print("End point has been changed to:", (i,j))

                if event.key == pygame.K_c:
                    se_phase = False
                    break
    return active

def BLOCK_PHASE(active):
    h = [[abs(END_NODE[0]-i)+abs(END_NODE[1]-j) for j in range(ROWS)] for i in range(ROWS)]
    
    block_phase = True
    while block_phase&active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                break
             
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]: #Tracks left click
                    position = pygame.mouse.get_pos()
                    i = (position[0]//NODE_LENGTH)
                    j = (position[1]//NODE_LENGTH)
                    set_blocked(i,j)

                if mouse_presses[2]: #Tracks right click
                    position = pygame.mouse.get_pos()
                    i = (position[0]//NODE_LENGTH)
                    j = (position[1]//NODE_LENGTH)
                    set_unblocked(i,j)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    block_phase = False
                    break
    return active

def ASTAR_PHASE(active):
    astar_phase = True
    count = 0
    while astar_phase&active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    astar_phase = False
                    break
        if count<1:
            ans = repeated_astar(START_NODE, END_NODE)
            if ans:
                print("REACHED TARGET")
            else:
                print("CANT REACH DUDE")
            count+=1
    return active

def game_loop():
    update_frame()
    active = True
    active = SE_PHASE(active)
    active = BLOCK_PHASE(active)
    active = ASTAR_PHASE(active)

def main():
    game_loop()

main()
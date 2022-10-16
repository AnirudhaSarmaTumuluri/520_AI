from msilib import OpenDatabase
from queue import PriorityQueue as PQ
import random
from tkinter import END
from tkinter.filedialog import Open
import pygame
from math import inf
import time
from constants import *
from Origianl_maze_gen import make_maze
from Generator_maze import newmaze
from reader import readFile
fname = 'explanation_maze'
actual_grid = readFile(fname)
display_grid = actual_grid
agent_grid = [[GREY for _ in range(ROWS)] for x in range(ROWS)]
agent_grid[-1][-1] = BLUE
search = [[0 for _ in range(ROWS)] for x in range(ROWS)]
g = [[float('inf') for _ in range(ROWS)] for x in range(ROWS)]
f = [[float('inf') for _ in range(ROWS)] for x in range(ROWS)]
def calculate_hcost(ROWS, target):
    for i in range(ROWS):
        for j in range(ROWS):
            h[i][j] = abs(target[0]-i)+abs(target[1]-j)



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
    agent_grid[START_NODE[0]][START_NODE[1]] = RED
    agent_grid[END_NODE[0]][END_NODE[1]] = BLUE
    neighbors = give_neighbors_update(START_NODE)
    for neighbor in neighbors:
        agent_grid[neighbor[0]][neighbor[1]] = display_grid[neighbor[0]][neighbor[1]]
    update_frame()

def set_start(i,j):
    global START_NODE
    display_grid[START_NODE[0]][START_NODE[1]] = WHITE #Make old start white
    display_grid[i][j] = RED #color the new start node
    agent_grid[START_NODE[0]][START_NODE[1]] = GREY
    agent_grid[i][j] = RED
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



def makepath(camefrom, current, start):
    #print(camefrom)
    total_path = []
    while current!=start:
        total_path.append(current)
        current = camefrom[current]
    total_path.append(start)
    return total_path

def give_neighbors_agent(NODE):
    retval = []
    i,j = NODE[0], NODE[1]
    #print('Indices received:', i,j)
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



h = [[0 for j in range(ROWS)] for i in range(ROWS)]


from CustomPriorityQueue_minG import CustomPQ_minG as CQ
# from CustomPriorityQueue_maxG import CustomPQ_maxG as CQ
def astar_agent_backward(start, counter):
    target = start
    start = END_NODE
    #print(target)
    camefrom = dict()
    openset = CQ()
    openset.put((h[start[0]][start[1]], start))
    #print('AFTER PUT:', openset.queue)
    visited = set()


    #g[start[0]][start[1]] = 0
    #g[END_NODE[0]][END_NODE[1]] = float('inf')
    #search = [[0 for _ in range(ROWS)] for x in range(ROWS)]
    #f[start[0]][start[1]] = h[start[0]][start[1]]
    #print(openset)
    #print(openset.empty())
    while not openset.empty():
        choice = openset.get()
        if choice not in visited:
            visited.add(choice)
            #print('AFTER GET:', openset.queue)
            #print('Choice:', choice)
            choice = choice[1]
            if choice==target:
                path = makepath(camefrom, target, start)
                return True, path
            for neighbor in give_neighbors_agent(choice):
                if search[neighbor[0]][neighbor[1]] < counter:
                    g[neighbor[0]][neighbor[1]] = float('inf')
                    search[neighbor[0]][neighbor[1]] = counter
                test = g[choice[0]][choice[1]]+1
                if test<g[neighbor[0]][neighbor[1]]:
                    camefrom[neighbor] = choice
                    g[neighbor[0]][neighbor[1]] = test

                    f[neighbor[0]][neighbor[1]] = test+h[neighbor[0]][neighbor[1]]
                    if neighbor not in openset.queue:
                        openset.put((f[neighbor[0]][neighbor[1]], neighbor))
                    #print('AFTER PUT:', openset.queue)
    return False, None


def astar_agent(start, counter):
    print(start)
    camefrom = dict()
    openset = CQ()
    openset.put((h[start[0]][start[1]], start))
    #print('AFTER PUT:', openset.queue)
    visited = set()
    while not openset.empty():
        choice = openset.get()
        if choice not in visited:
            visited.add(choice)
            #print('AFTER GET:', openset.queue)
            #print('Choice:', choice)
            choice = choice[1]
            if choice==END_NODE:
                path = makepath(camefrom, END_NODE, start)
                return True, path[::-1]
            for neighbor in give_neighbors_agent(choice):
                if search[neighbor[0]][neighbor[1]] < counter:
                    g[neighbor[0]][neighbor[1]] = float('inf')
                    search[neighbor[0]][neighbor[1]] = counter
                test = g[choice[0]][choice[1]]+1
                if test<g[neighbor[0]][neighbor[1]]:
                    camefrom[neighbor] = choice
                    g[neighbor[0]][neighbor[1]] = test
                    f[neighbor[0]][neighbor[1]] = test+h[neighbor[0]][neighbor[1]]
                    if neighbor not in openset.queue:
                        openset.put((f[neighbor[0]][neighbor[1]], neighbor))
                    #print('AFTER PUT:', openset.queue)
    return False, None

def repeated_astar(start):
    Open_path = []
    counter = 0
    calculate_hcost(ROWS, END_NODE)
    current_location = start
    agent_grid[current_location[0]][current_location[1]] = RED
    Open_path.append(start)

    while current_location!=END_NODE:
        counter+=1
        #getpath from a star
        #print('---------------------------------')
        print('CALCULATING PATH FROM:', current_location)
        g[start[0]][start[1]] = 0
        search[start[0]][start[1]] = counter
        g[END_NODE[0]][END_NODE[1]] = float('inf')
        search[END_NODE[0]][END_NODE[1]] = counter
        ans, path = astar_agent(current_location, counter)
        #print(path)
        print('Path found:', ans)
        #print(path)
        #print('----------------------------------')
        #follow path until node in path is blocked
        #Assume that the first node in path would be start point and last would be end point
        i = 1
        if ans:
            next_step = path[1]
            steps_taken_without_path_update = 0
            while agent_grid[next_step[0]][next_step[1]]!=BLACK:
                steps_taken_without_path_update+=1
                i+=1
                print('Currently at:', current_location)
                agent_grid[current_location[0]][current_location[1]] = WHITE
                display_grid[current_location[0]][current_location[1]] = WHITE
                current_location = next_step #Move a step
                display_grid[current_location[0]][current_location[1]] = RED
                #time.sleep(0.2)
                Open_path.append(current_location)
                agent_grid[current_location[0]][current_location[1]] = RED
                if current_location==END_NODE:
                    print("Astar computed path", counter, 'times.')
                    return True
                #Update information about surroundings
                updates = give_neighbors_update(current_location)
                for node in updates:
                    if agent_grid[node[0]][node[1]]!=PATH:
                        agent_grid[node[0]][node[1]] = actual_grid[node[0]][node[1]]
                update_frame()
                next_step = path[i] #Get ready to take next step
                #update knowledge
        
        #repeat the loop when a block is found
        else:
            return False
    print("Astar computed path", counter, 'times.')
    return True
    pass

def astar_agent_adaptive(start, counter, gGOAL):
    #print(start)
    camefrom = dict()
    openset = CQ()
    openset.put((h[start[0]][start[1]], start))
    visited = set()
    while not openset.empty():
        choice = openset.get()
        if choice not in visited:
            visited.add(choice)
            choice = choice[1]
            if choice==END_NODE:
                path = makepath(camefrom, END_NODE, start)
                return True, path[::-1], g[END_NODE[0]][END_NODE[1]]
            for neighbor in give_neighbors_agent(choice):
                if search[neighbor[0]][neighbor[1]] < counter:
                    g[neighbor[0]][neighbor[1]] = float('inf')
                    search[neighbor[0]][neighbor[1]] = counter
                test = g[choice[0]][choice[1]]+1
                if test<g[neighbor[0]][neighbor[1]]:
                    camefrom[neighbor] = choice
                    g[neighbor[0]][neighbor[1]] = test
                    f[neighbor[0]][neighbor[1]] = test+h[neighbor[0]][neighbor[1]]
                    h[neighbor[0]][neighbor[1]] = gGOAL - test

                    if neighbor not in openset.queue:
                        openset.put((f[neighbor[0]][neighbor[1]], neighbor))

    return False, None, gGOAL

def repeated_astar_ADAPTIVE(start):
    counter = 0
    calculate_hcost(ROWS, END_NODE)
    current_location = start
    agent_grid[current_location[0]][current_location[1]] = RED
    g[start[0]][start[1]] = 0
    search[start[0]][start[1]] = counter
    g[END_NODE[0]][END_NODE[1]] - float('inf')
    search[END_NODE[0]][END_NODE[1]] = counter
    ans, path = astar_agent(current_location, counter)
    gGOAL = g[END_NODE[0]][END_NODE[1]]
    while current_location!=END_NODE:
        counter+=1
        #getpath from a star
        print('---------------------------------')
        print('CALCULATING PATH FROM:', current_location)
        h[start[0]][start[1]] = gGOAL - g[start[0]][start[1]]
        g[start[0]][start[1]] = 0
        search[start[0]][start[1]] = counter
        g[END_NODE[0]][END_NODE[1]] = float('inf')
        search[END_NODE[0]][END_NODE[1]] = counter
        ans, path, gGOAL = astar_agent_adaptive(current_location, counter, gGOAL)
        #print(path)
        print('Path found:', ans)
        #print(path)
        print('----------------------------------')
        #follow path until node in path is blocked
        #Assume that the first node in path would be start point and last would be end point
        i = 1
        if ans:
            next_step = path[1]
            while agent_grid[next_step[0]][next_step[1]]!=BLACK:
                i+=1
                print('Currently at:', current_location)
                agent_grid[current_location[0]][current_location[1]] = WHITE
                display_grid[current_location[0]][current_location[1]] = WHITE
                current_location = next_step #Move a step
                display_grid[current_location[0]][current_location[1]] = RED
                #time.sleep(0.2)
                agent_grid[current_location[0]][current_location[1]] = RED
                if current_location==END_NODE:
                    return True
                #Update information about surroundings
                updates = give_neighbors_update(current_location)
                for node in updates:
                    if agent_grid[node[0]][node[1]]!=PATH:
                        agent_grid[node[0]][node[1]] = actual_grid[node[0]][node[1]]
                update_frame()
                next_step = path[i] #Get ready to take next step
                #update knowledge
        
        #repeat the loop when a block is found
        else:
            return False
    print("Astar computed path", counter, 'times.')
    return True
    pass

def repeated_astar_backward(start):
    Open_path = []
    counter = 0
    calculate_hcost(ROWS, END_NODE)
    current_location = start
    agent_grid[current_location[0]][current_location[1]] = RED
    Open_path.append(start)

    while current_location!=END_NODE:
        counter+=1
        #getpath from a star
        #print('---------------------------------')
        #print('CALCULATING PATH FROM:', current_location)
        g[END_NODE[0]][END_NODE[1]] = 0
        
        search[start[0]][start[1]] = counter
        g[start[0]][start[1]] = float('inf')
        search[END_NODE[0]][END_NODE[1]] = counter
        ans, path = astar_agent_backward(current_location, counter)
        print(path)
        print('Path found:', ans)
        #print(path)
        #print('----------------------------------')
        #follow path until node in path is blocked
        #Assume that the first node in path would be start point and last would be end point
        i = 1
        if ans:
            next_step = path[1]
            steps_taken_without_path_update = 0
            while agent_grid[next_step[0]][next_step[1]]!=BLACK:
                steps_taken_without_path_update+=1
                i+=1
                print('Currently at:', current_location)
                agent_grid[current_location[0]][current_location[1]] = WHITE
                display_grid[current_location[0]][current_location[1]] = WHITE
                current_location = next_step #Move a step
                display_grid[current_location[0]][current_location[1]] = RED
                #time.sleep(0.2)
                Open_path.append(current_location)
                agent_grid[current_location[0]][current_location[1]] = RED
                if current_location==END_NODE:
                    return True
                #Update information about surroundings
                updates = give_neighbors_update(current_location)
                for node in updates:
                    if agent_grid[node[0]][node[1]]!=PATH:
                        agent_grid[node[0]][node[1]] = actual_grid[node[0]][node[1]]
                update_frame()
                next_step = path[i] #Get ready to take next step
                #update knowledge
        
        #repeat the loop when a block is found
        else:
            return False



    return True
    pass

            
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
                        if not ((actual_grid[i][j]==BLACK)or(actual_grid[i][j]==RED)):
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
    calculate_hcost(ROWS, END_NODE)
    g = [[float('inf') for _ in range(ROWS)] for x in range(ROWS)]
    f = [[float('inf') for _ in range(ROWS)] for x in range(ROWS)]
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
            #ans = repeated_astar_backward(START_NODE)
            ans = repeated_astar_ADAPTIVE(START_NODE)
            #ans = repeated_astar(START_NODE)
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

def stat_loop():
    calculate_hcost(ROWS, END_NODE)
    actual_grid = newmaze()
    agent_grid = [[GREY for _ in range(ROWS)] for x in range(ROWS)]
    agent_grid[-1][-1] = BLUE
    search = [[0 for _ in range(ROWS)] for x in range(ROWS)]
    g = [[float('inf') for _ in range(ROWS)] for x in range(ROWS)]
    f = [[float('inf') for _ in range(ROWS)] for x in range(ROWS)]
    #ans = repeated_astar_backward(START_NODE)
    ans = repeated_astar_ADAPTIVE(START_NODE)
    #ans = repeated_astar(START_NODE)
    if ans:
        print("REACHED TARGET")
    else:
        print("CANT REACH DUDE")
    pass

def main():
    game_loop()

main()

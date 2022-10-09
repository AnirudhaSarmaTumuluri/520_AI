

from queue import PriorityQueue as PQ
import random
from turtle import update
import pygame
from math import inf
from constants import *
from get_neighbors import *
from initialization import *
# PROGRAM GLOBAL VARS


WINDOW = make_game_window()


actual_grid = [[WHITE for _ in range(ROWS)] for x in range(ROWS)]
display_grid = actual_grid
agent_grid = [[GREY for _ in range(ROWS)] for x in range(ROWS)]
choice = WHITE
for i in range(ROWS):
    for j in range(ROWS):
        if random.randint(1,10)%9==0:
            choice = BLACK
        else:
            choice = WHITE
        
        display_grid[i][j] = choice
        
START_NODE = (0,0)
END_NODE = (ROWS-1,ROWS-1)

# GLOBAL VARS ENDS



#pygame.draw.rect(WINDOW, display_grid[3][7], (3*NODE_LENGTH, 7*NODE_LENGTH, NODE_LENGTH, NODE_LENGTH))




def init_agent_grid():
    global agent_grid
    agent_grid = [[GREY for _ in range(ROWS)] for x in range(ROWS)]
    agent_grid[START_NODE[0]][START_NODE[1]] = YELLOW
    agent_grid[END_NODE[0]][END_NODE[1]] = BLUE
    neighbors = give_neighbors_update(START_NODE)
    for neighbor in neighbors:
        agent_grid[neighbor[0]][neighbor[1]] = display_grid[neighbor[0]][neighbor[1]]

    update_frame(WINDOW, display_grid)
    


def draw_lines_GLOBAL(WINDOW):
    for i in range(ROWS):
        pygame.draw.line(WINDOW, BLACK, (0, i*NODE_LENGTH), (GRID_LENGTH*2+NODE_LENGTH, i*NODE_LENGTH))
        

    for i in range(ROWS+1):
        pygame.draw.line(WINDOW, BLACK, (i*NODE_LENGTH, 0), (i*NODE_LENGTH, GRID_LENGTH))
        
    
    for i in range(ROWS):
        pygame.draw.line(WINDOW, BLACK, (i*NODE_LENGTH+GRID_LENGTH+NODE_LENGTH, 0), (i*NODE_LENGTH+GRID_LENGTH+NODE_LENGTH, GRID_LENGTH))


  
def draw_colors_GLOBAL(WINDOW, display_grid):
    for i in range(ROWS):
        for j in range(ROWS):
            pygame.draw.rect(WINDOW, display_grid[i][j], (i*NODE_LENGTH, j*NODE_LENGTH, NODE_LENGTH, NODE_LENGTH))
            pygame.draw.rect(WINDOW, agent_grid[i][j], (i*NODE_LENGTH+GRID_LENGTH+NODE_LENGTH, j*NODE_LENGTH, NODE_LENGTH, NODE_LENGTH))



def update_frame(WINDOW, display_grid):
    draw_colors_GLOBAL(WINDOW, display_grid)
    draw_lines_GLOBAL(WINDOW)
    pygame.display.update()

    
def set_start(i,j):
    global START_NODE
    display_grid[START_NODE[0]][START_NODE[1]] = WHITE #Make old start white
    display_grid[i][j] = YELLOW #color the new start node
    agent_grid[START_NODE[0]][START_NODE[1]] = GREY
    agent_grid[i][j] = YELLOW
    START_NODE = (i,j)
    update_frame(WINDOW, display_grid)

set_start(START_NODE[0], START_NODE[1])

def set_end(i,j):
    global END_NODE
    display_grid[END_NODE[0]][END_NODE[1]] = WHITE
    display_grid[i][j] = BLUE
    agent_grid[END_NODE[0]][END_NODE[1]] = GREY
    agent_grid[i][j] = BLUE
    END_NODE = (i,j)
    update_frame(WINDOW, display_grid)

set_end(END_NODE[0], END_NODE[1])
#init_agent_grid()
def set_infrontier(NODE):
    if (NODE!=START_NODE)&(NODE!=END_NODE):
        display_grid[NODE[0]][NODE[1]] = RED
        update_frame(WINDOW, display_grid)

def set_expanded(NODE):
    if (NODE!=START_NODE)&(NODE!=END_NODE):
        display_grid[NODE[0]][NODE[1]] = GREEN
        update_frame(WINDOW, display_grid)

def set_blocked(i,j):
    if ((i,j)!=START_NODE) & ((i,j)!=END_NODE):
        display_grid[i][j] = BLACK
        update_frame(WINDOW, display_grid)

def set_unblocked(i,j):
    if ((i,j)!=START_NODE) & ((i,j)!=END_NODE):
        display_grid[i][j] = WHITE
        update_frame(WINDOW, display_grid)





def hcost(NODE):
    return abs(END_NODE[0]-NODE[0])+abs(END_NODE[1]-NODE[1])



def makepath(camefrom, current, start):
    total_path = []
    while current!=start:
        total_path.append(current)
        current = camefrom[current[0]][current[1]]
    
    total_path.append(START_NODE)
    return total_path




def astar(start):

    openset = PQ()
    openset.put((hcost(start), start))
    gcost = [[inf for _ in range(ROWS)] for x in range(ROWS)]
    gcost[start[0]][start[1]] = 0

    fcost = [[inf for _ in range(ROWS)] for x in range(ROWS)]
    fcost[start[0]][start[1]] = hcost(start)
    
    camefrom = [[None for _ in range(ROWS)] for x in range(ROWS)]

    while not openset.empty():

        choice = openset.get()
        #print(choice)
        choice = choice[1]
        #set_expanded(choice)
        #print(choice, fcost[choice[0]][choice[1]], gcost[choice[0]][choice[1]])
        if choice==END_NODE:
            #print("REACHED:", END_NODE)
            """for x in gcost:
                print(x)

            print('-----------------------')
            print('----------------------')
            for x in fcost:
                print(x)"""

            path = makepath(camefrom, END_NODE, start)
            for i in range(1,len(path)-1):
                x = path[i]
                display_grid[x[0]][x[1]] = PATH
            #display_grid[path[-1][0]][path[-1][1]] = WHITE
            #display_grid[path[-2][0]][path[-2][1]] = YELLOW
            update_frame(WINDOW, display_grid)


            return True, path[-2]
        
        for neighbor in give_neighbors(choice):
            G = gcost[choice[0]][choice[1]]+1
            if G<gcost[neighbor[0]][neighbor[1]]:
                camefrom[neighbor[0]][neighbor[1]] = (choice)
                gcost[neighbor[0]][neighbor[1]] = G
                print('G=', G, 'HCOST:', hcost(neighbor))
                fcost[neighbor[0]][neighbor[1]] = G+hcost(neighbor)
                if neighbor not in openset.queue:
                    openset.put((fcost[neighbor[0]][neighbor[1]], neighbor))
                    #set_infrontier(neighbor)
                    #update_frame(WINDOW, display_grid)

    return False, None


def astar_agent(start):

    openset = PQ()
    openset.put((hcost(start), start))
    gcost = [[inf for _ in range(ROWS)] for x in range(ROWS)]
    gcost[start[0]][start[1]] = 0

    fcost = [[inf for _ in range(ROWS)] for x in range(ROWS)]
    fcost[start[0]][start[1]] = hcost(start)
    
    camefrom = [[None for _ in range(ROWS)] for x in range(ROWS)]

    while not openset.empty():

        choice = openset.get()
        #print(choice)
        choice = choice[1]
        #set_expanded(choice)
        #print(choice, fcost[choice[0]][choice[1]], gcost[choice[0]][choice[1]])
        if choice==END_NODE:
            #print("REACHED:", END_NODE)
            """for x in gcost:
                print(x)

            print('-----------------------')
            print('----------------------')
            for x in fcost:
                print(x)"""

            path = makepath(camefrom, END_NODE, start)
            #for i in range(1,len(path)-1):
                #x = path[i]
                #agent_grid[x[0]][x[1]] = PATH

            updates = give_neighbors_update(path[-2])
            for node in updates:
                if agent_grid[node[0]][node[1]]!=PATH:
                    agent_grid[node[0]][node[1]] = actual_grid[node[0]][node[1]]
            #agent_grid[path[-1][0]][path[-1][1]] = WHITE
            #agent_grid[path[-2][0]][path[-2][1]] = YELLOW
            update_frame(WINDOW, display_grid)


            return True, path[-2]
        
        for neighbor in give_neighbors_agent(choice):
            G = gcost[choice[0]][choice[1]]+1
            if G<gcost[neighbor[0]][neighbor[1]]:
                camefrom[neighbor[0]][neighbor[1]] = (choice)
                gcost[neighbor[0]][neighbor[1]] = G
                #print('G=', G, 'HCOST:', hcost(neighbor))
                fcost[neighbor[0]][neighbor[1]] = G+hcost(neighbor)
                if neighbor not in openset.queue:
                    openset.put((fcost[neighbor[0]][neighbor[1]], neighbor))
                    #set_infrontier(neighbor)
                    #update_frame(WINDOW, display_grid)

    return False, None

def repeated_astar(start, target):
    #prev = start
    while start!=target:
        ans, next_step = astar_agent(start)
        if ans:
            display_grid[start[0]][start[1]] = WHITE

            agent_grid[start[0]][start[1]] = PATH
            start = next_step
            display_grid[start[0]][start[1]] = YELLOW
            agent_grid[start[0]][start[1]] = WHITE

            #time.sleep(0.1)
        else:
            return False
    return True
            








def game_loop():
    update_frame(WINDOW, display_grid)

    active = True
    se_phase = True

    while se_phase&active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                break
             
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]: #Tracks left click
                    #print('Left click pressed')
                    position = pygame.mouse.get_pos()
                    i = (position[0]//NODE_LENGTH)
                    j = (position[1]//NODE_LENGTH)
                    set_start(i,j)
                    init_agent_grid()
                    #pygame.draw.rect(WINDOW, display_grid[i][j], (i*NODE_LENGTH, j*NODE_LENGTH, NODE_LENGTH, NODE_LENGTH))
                    #pygame.display.update()
                    #print(pygame.mouse.get_pos())
                    #WINDOW.fill(GREEN)
                    #pygame.display.update()

                if mouse_presses[2]: #Tracks Right click
                    #print('Right click pressed')
                    position = pygame.mouse.get_pos()
                    i = (position[0]//NODE_LENGTH)
                    j = (position[1]//NODE_LENGTH)
                    set_end(i,j)
                    #WINDOW.fill(RED)
                    #pygame.display.update()
            
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
                    #print('Left click pressed')
                    position = pygame.mouse.get_pos()
                    i = (position[0]//NODE_LENGTH)
                    j = (position[1]//NODE_LENGTH)
                    set_blocked(i,j)

                if mouse_presses[2]: #Tracks right click
                    #print('Right click pressed')
                    position = pygame.mouse.get_pos()
                    i = (position[0]//NODE_LENGTH)
                    j = (position[1]//NODE_LENGTH)
                    set_unblocked(i,j)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    block_phase = False
                    break
    
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

        #astar_phase = False

        

        pass





    

        

def main():
    game_loop()
"""    if astar():
        print("REACHED TARGET")
    else:
        print("CANNOT REACH TARGET")
    """
main()
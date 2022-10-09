from constants import *


def give_neighbors_update(NODE):
    retval = []
    i,j = NODE[0], NODE[1]

    if j-1>=0:
        retval.append((i, j-1))
    
    if j+1<ROWS:
        retval.append((i, j+1))

    if i-1>=0:
        #print(i, j, ROWS)
        #print(NODE)
        #print(display_grid[i-1][j])
        retval.append((i-1, j))

    if i+1<ROWS:
        retval.append((i+1, j))
    

    #print('NODE:',retval)
    return retval

def give_neighbors(NODE):
    retval = []
    i,j = NODE[0], NODE[1]

    if j-1>=0:
        if display_grid[i][j-1]!=BLACK:
            retval.append((i, j-1))
    
    if j+1<ROWS:
        if display_grid[i][j+1]!=BLACK:
            retval.append((i, j+1))
    if i-1>=0:
        #print(i, j, ROWS)
        #print(NODE)
        #print(display_grid[i-1][j])
        if display_grid[i-1][j]!=BLACK:
            retval.append((i-1, j))
    
    if i+1<ROWS:
        if display_grid[i+1][j]!=BLACK:
            retval.append((i+1, j))
    

    #print('NODE:',retval)
    return retval


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
        #print(i, j, ROWS)
        #print(NODE)
        #print(display_grid[i-1][j])
        if agent_grid[i-1][j]!=BLACK:
            retval.append((i-1, j))
    
    if i+1<ROWS:
        if agent_grid[i+1][j]!=BLACK:
            retval.append((i+1, j))
    

    #print('NODE:',retval)
    return retval
import random
from venv import create
from xml.etree.ElementTree import XML
from constants import ROWS, BLACK, WHITE
visited = [[False for _ in range(ROWS)] for x in range(ROWS)]

def markVisited(vertex):
    visited[vertex[0]][vertex[1]] = True

def give_neighbors_agent(NODE):
    retval = []
    i,j = NODE[0], NODE[1]
    #print('Indices received:', i,j)
    if j-1>=0:
        if not visited[i][j-1]:
            retval.append((i, j-1))
    if j+1<ROWS:
        if not visited[i][j+1]:
            retval.append((i, j+1))
    if i-1>=0:
        if not visited[i-1][j]:
            retval.append((i-1, j))
    if i+1<ROWS:
        if not visited[i+1][j]:
            retval.append((i+1, j))
    return retval

def block(vertex, maze):
    choice = random.randint(1,10)
    if choice%3==0:
        #print('Blocked:', vertex)
        maze[vertex[0]][vertex[1]] = 1
    return maze

def randomUnvisitedVertex(vertex):
    choices = give_neighbors_agent(vertex)
    if len(choices)!=0:
        return random.choice(choices)

def createMaze():
    maze = [[0 for _ in range(ROWS)] for x in range(ROWS)]
    start = (random.randint(0,ROWS-1),random.randint(0,ROWS-1))
    stack = []
    stack.append(start)
    while len(stack)!=0:
        current = stack.pop()
        maze = block(current, maze)
        neighbors = give_neighbors_agent(current)
        while len(neighbors)!=0:
            index = random.randint(0,len(neighbors)-1)
            neighbor = neighbors.pop(index)
            if neighbor not in visited:
                visited[neighbor[0]][neighbor[1]] = True
                stack.append(neighbor)
    return maze
import sys
fname = "attach2\Random_Maze " + str(7)
x = createMaze()
# for row in x:
#     print(row)
fp = open(fname, 'a')
for i in range(ROWS):
    for j in range(ROWS):
        fp.write(str(x[i][j]) + ' ')
    fp.write('\n')
fp.close()

    


'''
for i in range(50):
    fname = 'Maze_'+str(i)+'.txt'
    fp = open(fname, 'a')
    maze = createMaze()
    for i in range(ROWS):
        for j in range(ROWS):
            fp.write(str(maze[i][j]) + ' ')
        fp.write('\n')
    fp.close()'''




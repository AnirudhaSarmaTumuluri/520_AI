
from Generator_maze import createMaze
from constants import ROWS
for i in range(5):
    fname = 'x_Maze_'+str(i)+'.txt'
    fp = open(fname, 'a')
    maze = createMaze()
    for i in range(ROWS):
        for j in range(ROWS):
            fp.write(str(maze[i][j]) + ' ')
        fp.write('\n')
    fp.close()
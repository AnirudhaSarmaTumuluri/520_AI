from constants import BLACK, WHITE

def readFile(fname):
    fp = open(fname, 'r')
    maze = []
    for line in fp:
        row = []
        for block in line.split():
            if block.strip()=='1':
                row.append(BLACK)
            else:
                row.append(WHITE)
        maze.append(row)
    return maze



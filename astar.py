from math import inf
def give_neighbors(curr, size):
    retval = []
    i,j = curr[0], curr[1]
    if i-1>=0:
        retval.append([i-1, j])
    
    if i+1<size:
        retval.append([i+1, j])
    
    if j-1>=0:
        retval.append([i, j-1])
    
    if j+1<size:
        retval.append([i, j+1])

    return retval

def h(i,j, end, grid):
    return abs(i-end[0])+abs(j-end[1])

def findLowest(Oset, fcost):
    ans =  inf
    ansnode = None
    for node in Oset:
        if fcost[node[0]][node[1]]<ans:
            ans = fcost[node[0]][node[1]]
            ansnode = node
    return ansnode
def main():
    grid = [[0 for _ in range(5)] for x in range(5)]
    start = [1,1]
    end = [4,4]

    openset = []
    openset.append(start)
    camefrom = grid

    gcost = [[inf for _ in range(5)] for x in range(5)]
    gcost[start[0]][start[1]] = 0

    fcost = [[inf for _ in range(5)] for x in range(5)]
    fcost[start[0]][start[1]] = h(start[0], start[1], end, grid)

    #print(give_neighbors([1,1], 5))
    while len(openset)!=0:
        current = findLowest(openset, fcost)
        if current == end:
            print("REACHED")
            break
        print()
        print('Current:', current)
        print('Openset:', openset)
        print()
        openset.remove(current)
        
        for neighbor in give_neighbors(current, len(grid)):
            G = gcost[current[0]][current[1]] + 1
            if G<gcost[neighbor[0]][neighbor[1]]:
                gcost[neighbor[0]][neighbor[1]] = G
                fcost[neighbor[0]][neighbor[1]] = G + h(neighbor[0], neighbor[1], end, grid)
                if neighbor not in openset:
                    openset.append(neighbor)

main()





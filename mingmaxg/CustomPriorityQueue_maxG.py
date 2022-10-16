class CustomPQ_maxG():
    def __init__(self):
        self.queue = [(0, (0, 0), 0)]
        self.size = 0
        self.max_g = -1

    def empty(self):
        return len(self.queue) == 1
    
    def put(self, heuristic_tuple):
        self.max_g = max(self.max_g, heuristic_tuple[2])
        self.queue.append(heuristic_tuple)
        self.size = len(self.queue) - 1 
        swap_index = self.size
        while swap_index >= 2 and self.queue[swap_index//2][0] > self.queue[swap_index][0]:
            tmp = self.queue[swap_index]
            self.queue[swap_index] = self.queue[swap_index//2]
            self.queue[swap_index//2] = tmp
            swap_index = swap_index//2
        while swap_index >= 2 and self.queue[swap_index//2][0] == self.queue[swap_index][0]:
            f1 = self.queue[swap_index//2][0]
            c = self.max_g + 1
            g1 = self.queue[swap_index//2][2]
            f2 = self.queue[swap_index][0]
            g2 = self.queue[swap_index][2]
            if (f1*c - g1) > (f2*c-g2):
                tmp = self.queue[swap_index]
                self.queue[swap_index] = self.queue[swap_index//2]
                self.queue[swap_index//2] = tmp
                swap_index = swap_index//2
            else:
                break  
    def get(self):
        max_heuristic_tuple = self.queue[1]
        self.queue[1] = self.queue[self.size]
        self.queue.pop()
        self.size -= 1
        swap_index = 1
        while swap_index*2 <= self.size:
            child_index = 2*swap_index
            if child_index < self.size and self.queue[child_index][0] > self.queue[child_index+1][0]:
                child_index += 1
            if self.queue[swap_index] > self.queue[child_index]:
                tmp = self.queue[swap_index]
                self.queue[swap_index] = self.queue[child_index]
                self.queue[child_index] = tmp 
                swap_index = child_index
            else:
                break
        return max_heuristic_tuple
 
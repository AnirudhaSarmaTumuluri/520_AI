class CustomPQ():
    def __init__(self):
        self.tuple_entries = [(int('inf'),int('inf'))]
        self.size = 0

    def empty(self):
        return len(self.tuple_entries) == 0
    
    def put(self, heuristic_tuple):
        self.tuple_entries.append(heuristic_tuple)
        self.size += 1
        swap_index = self.size
        while swap_index >= 2 and self.tuple_entries[swap_index//2][0] > self.tuple_entries[swap_index][0]:
            tmp = self.tuple_entries[swap_index]
            self.tuple_entries[swap_index] = self.tuple_entries[swap_index//2]
            self.tuple_entries[swap_index//2] = tmp
            swap_index = swap_index//2

    def get(self):
        max_heuristic_tuple = self.tuple_entries[1]
        self.tuple_entries[1] = self.tuple_entries[self.size]
        self.size -= 1
        swap_index = 1
        while swap_index*2 <= self.size:
            exchange_index = 2*swap_index
            if exchange_index < self.size and self.tuple_entries[2*exchange_index][0] > self.tuple_entries[2*exchange_index+1]:
                exchange_index += 1
            if self.tuple_entries[swap_index] > self.tuple_entries[exchange_index]:
                tmp = self.tuple_entries[swap_index]
                self.tuple_entries[swap_index] = self.tuple_entries[exchange_index]
                self.tuple_entries[exchange_index] = tmp 
                swap_index = exchange_index
        return max_heuristic_tuple
 
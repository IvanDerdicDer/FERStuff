import sys
from random import randint, random
from time import  sleep

class Memory:

    def __init__(self, size1 = 50, holes1 = False):
        self.withHoles = holes1
        self.memorySize = size1
        self.memory = [randint(0, 9) for _ in range(size1)]
        self.allocatedMemory = ['-'] * size1
        self.holesIndexing = [(0, size1)]

    def freeSpace(self):
        freeSpaceIndex = []
        i = 0
        while i < len(self.allocatedMemory):
            if self.allocatedMemory[i] == '-':
                for j in range(i, len(self.allocatedMemory)):
                    if self.allocatedMemory[j] != '-' or (j == len(self.allocatedMemory) - 1 and self.allocatedMemory[j] == '-'):
                        freeSpaceIndex.append((i, j-i))
                        i = j
                        break
            i += 1
        return freeSpaceIndex

    def allocateMemory(self, num, s):
        for i in self.holesIndexing:
            if i[1] >= s:
                for j in range(s):
                    self.allocatedMemory[i[0]+j] = num
                self.holesIndexing = self.freeSpace()
                break
        else:
            sys.exit(f"Nema dovoljno memorije za alokaciju")

    def releaseMemory(self, num):
        if num not in self.allocatedMemory:
            return

        for i in range(self.memorySize):
            if self.allocatedMemory[i] == num:
                for j in range(i, self.memorySize):
                    if self.allocatedMemory[j] != num:
                        if not self.withHoles:
                            self.mergeMemory(i, j - i)
                        self.holesIndexing = self.freeSpace()
                        break
                    self.allocatedMemory[j] = '-'

    def mergeMemory(self, startIndex, size):
        while startIndex + size < self.memorySize and self.allocatedMemory[startIndex + size] != '-':
            self.allocatedMemory[startIndex] = self.allocatedMemory[startIndex + size]
            self.allocatedMemory[startIndex + size] = '-'
            startIndex += 1

if __name__ == '__main__':
    memorySize = 50
    holes = 1
    id = 0
    if len(sys.argv) >= 3:
        memorySize = sys.argv[1]
        try:
            holes = int(sys.argv[2])
        except Exception:
            pass
    mem: Memory = Memory(int(memorySize), holes)
    print(f"{mem.memory}\n{mem.allocatedMemory}")
    print(mem.holesIndexing)
    while True:
        size = randint(1, 10)
        if random() >= 0.24:
            mem.allocateMemory(id, size)
            print(f"Alokacija za {id} veličine {size}")
            print(f"{mem.memory}\n{mem.allocatedMemory}")
            id += 1
        else:
            toRemove = int(input("ID za maknut: "))
            mem.releaseMemory(toRemove)
            print(f"{mem.memory}\n{mem.allocatedMemory}")
        print(mem.holesIndexing)
        sleep(1)
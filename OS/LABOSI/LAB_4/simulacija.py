import sys
from random import randint, random
from time import  sleep

class holeIndex:

    def __init__(self, startIndex, size):
        self.startIndex = startIndex
        self.size = size

    def __gt__(self, other):
        return self.startIndex > other.startIndex

    def __lt__(self, other):
        return self.startIndex < other.startIndex

    def __eq__(self, other):
        return self.startIndex == other.startIndex and self.size == other.size

    def __str__(self):
        return f"({self.startIndex}, {self.size})"

    def __repr__(self):
        return f"({self.startIndex}, {self.size})"

class Memory:

    def __init__(self, size1 = 50, holes1 = False):
        self.withHoles = holes1
        self.memorySize = size1
        self.memory = [randint(0, 9) for _ in range(size1)]
        self.allocatedMemory = ['-'] * size1
        self.holesIndexing = [holeIndex(0, size1)]

    def freeSpace(self):
        freeSpaceIndex = []
        i = 0
        while i < len(self.allocatedMemory):
            if self.allocatedMemory[i] == '-':
                for j in range(i, len(self.allocatedMemory)):
                    if self.allocatedMemory[j] != '-' or (j == len(self.allocatedMemory) - 1 and self.allocatedMemory[j] == '-'):
                        freeSpaceIndex.append(holeIndex(i, j-i))
                        i = j
                        break
            i += 1
        return freeSpaceIndex

    def allocateMemory(self, num, s):
        for i in self.holesIndexing:
            if i.size >= s:
                for j in range(s):
                    self.allocatedMemory[i.startIndex+j] = num
                ind = self.holesIndexing.index(i)
                if not (self.holesIndexing[ind].size - s):
                    self.holesIndexing.pop(ind)
                else:
                    self.holesIndexing[ind] = holeIndex(self.holesIndexing[ind].startIndex+s, self.holesIndexing[ind].size - s)
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
                            self.holesIndexing[0].startIndex -= j - i
                            self.holesIndexing[0].size += j - i
                            self.mergeMemory(i, j - i)
                        else:
                            toAppend = holeIndex(i, j-i)
                            if toAppend not in self.holesIndexing:
                                self.holesIndexing.append(toAppend)
                                self.holesIndexing.sort()
                        break
                    self.allocatedMemory[j] = '-'

    def mergeMemory(self, startIndex, size):
        while startIndex + size < self.memorySize and self.allocatedMemory[startIndex + size] != '-':
            self.allocatedMemory[startIndex] = self.allocatedMemory[startIndex + size]
            self.allocatedMemory[startIndex + size] = '-'
            startIndex += 1

    def defragment(self):
        for i in range(self.memorySize):
            tmpSize = 0
            if self.allocatedMemory[i] == '-':
                for j in range(i, self.memorySize):
                    if self.allocatedMemory[j] != '-':
                        tmpSize = j - i
                        break
                for j in range(i, i + tmpSize):
                    try:
                        self.allocatedMemory[j] = self.allocatedMemory[j + tmpSize]
                        self.allocatedMemory[j + tmpSize] = '-'
                    except IndexError:
                        break
                self.holesIndexing = self.freeSpace()

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
        if random() >= 0.5:
            mem.allocateMemory(id, size)
            print(f"Alokacija za {id} veličine {size}")
            print(f"{mem.memory}\n{mem.allocatedMemory}")
            id += 1
        else:
            toRemove = input("ID za maknut ili 'd' za defragmentaciju: ")
            if toRemove == 'd':
                mem.defragment()
            else:
                mem.releaseMemory(int(toRemove))
            print(f"{mem.memory}\n{mem.allocatedMemory}")
        print(mem.holesIndexing)
        sleep(1)
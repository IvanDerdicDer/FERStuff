import multiprocessing as mp
import sys
import ctypes


def incrementNTimes(a, n, id, z, pravo):
    for i in range(n):
        z[id] = 1
        while z[1-id] != 0:
            if pravo.value == 1-id:
                z[id] = 0
                while pravo.value == 1-id:
                    pass
                z[id] = 1
        a.value += 1
        pravo.value = 1 - id
        z[id] = 0

if __name__ == '__main__':
    common = mp.Value('i', 0)
    processNumber = int(sys.argv[1])
    incrementNumber = int(sys.argv[2])
    while processNumber - 2 >= 0:
        z = mp.Manager().list((0, 0))
        pravo = mp.Value('i', 0)
        processes = [mp.Process(target=incrementNTimes, args=[common, incrementNumber, 0, z, pravo]),
                     mp.Process(target=incrementNTimes, args=[common, incrementNumber, 1, z, pravo])]
        processes[0].start()
        processes[1].start()
        processes[0].join()
        processes[1].join()
        processNumber -= 2

    if processNumber > 0:
        z = mp.Manager().list((0, 0))
        pravo = mp.Value('i', 0)
        p = mp.Process(target=incrementNTimes, args=[common, incrementNumber, 0, z, pravo])
        p.start()
        p.join()

    print(common.value)

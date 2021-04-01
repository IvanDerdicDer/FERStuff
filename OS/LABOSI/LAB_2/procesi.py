import multiprocessing as mp
import sys


def incrementNTimes(a, n):
    for i in range(n):
        a.value += 1

if __name__ == '__main__':
    common = mp.Value('i', 0)
    processNumber = int(sys.argv[1])
    incrementNumber = int(sys.argv[2])
    processes = []
    for i in range(processNumber):
        processes.append(mp.Process(target=incrementNTimes, args=[common, incrementNumber]))
        processes[-1].start()
    for p in processes:
        p.join()

    print(common.value)
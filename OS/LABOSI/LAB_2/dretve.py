import threading as td
import sys

def incrementNTimes(n, id):
    global common
    for i in range(n):
        common = common + 1

if __name__ == '__main__':
    common = 0
    threadNumber = int(sys.argv[1])
    incrementNumber = int(sys.argv[2])
    threads = []
    for i in range(threadNumber):
        threads.append(td.Thread(target=incrementNTimes, args=[incrementNumber, i]))
        threads[-1].start()
    for t in threads:
        t.join()

    print(common)
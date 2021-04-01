import signal
import sys
import os

pauseProgram = False
lastPrime = None

def printLastPrime(a, b):
    global lastPrime
    print(lastPrime)

def isPrime(n):
    for i in range(3, n, 2):
        if n % i == 0 or n == 1 or n == 2:
            return False
    return True

def pause(a, b):
    global pauseProgram
    pauseProgram = not pauseProgram

def killSelf(a, b):
    printLastPrime(None, None)
    sys.exit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, pause)
    signal.signal(signal.SIGTERM, killSelf)
    signal.signal(signal.SIGQUIT, killSelf)
    signal.setitimer(signal.ITIMER_REAL, 5, 5)
    signal.signal(signal.SIGALRM, printLastPrime)
    print(f"My PID: {os.getpid()}")
    i = 2
    while True:
        if not pauseProgram:
            if isPrime(i):
                lastPrime = i
            i += 1



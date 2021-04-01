import signal
import sys
import os
import random
import time

def killSelfAndOther(sigNumber, frame):
    os.kill(pidToMess, signal.SIGQUIT)
    sys.exit("Killed")

def killSelf(sigNumber, frame):
    sys.exit("Killed")

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, killSelf)
    signal.signal(signal.SIGQUIT, killSelf)
    signal.signal(signal.SIGINT, killSelfAndOther)
    pidToMess = int(sys.argv[1])
    signals = [signal.SIGUSR1, signal.SIGUSR2, signal.SIGALRM, signal.SIGCONT]
    while True:
        sigSelect = random.randint(0, 3)
        os.kill(pidToMess, signals[sigSelect])
        print(f"Poslan: {signals[sigSelect]}")

        time.sleep(random.randint(3, 5))
        #time.sleep(6)
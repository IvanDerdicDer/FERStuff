import threading as thrd
import time

def philosopher(id):
    while True:
        leftChopstick = id
        rightChopstick = (id + 1) % 5
        leftPhilosopher = (id - 1) % 5
        rightPhilosopher = rightChopstick
        #Think
        time.sleep(2)
        #pickup chopsticks
        with lock:
            while not (chopsticks[leftChopstick] and chopsticks[rightChopstick]):
                pEvents[id].clear()
                philosopherState[id] = 'o'
                lock.release()
                pEvents[id].wait()
                lock.acquire()
            chopsticks[leftChopstick] = False
            chopsticks[rightChopstick] = False
        #Eat
        philosopherState[id] = 'X'
        time.sleep(2)
        philosopherState[id] = 'O'
        #Set down chopsticks
        with lock:
            chopsticks[leftChopstick] = True
            chopsticks[rightChopstick] = True
            pEvents[leftPhilosopher].set()
            pEvents[rightPhilosopher].set()

if __name__ == '__main__':
    lock = thrd.Lock()
    chopsticks = [True] * 5
    philosophers = []
    philosopherState = ['O'] * 5
    pEvents = [thrd.Event()] * 5
    for p in pEvents:
        p.set()
    for i in range(5):
        philosophers.append(thrd.Thread(target=philosopher, args=(i,)))
        philosophers[-1].start()
    while True:
        time.sleep(1)
        numberEating = 0
        for i in philosopherState:
            if i == 'X':
                numberEating += 1
        print(f"{philosopherState} {numberEating}")
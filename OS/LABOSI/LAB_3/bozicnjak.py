import multiprocessing as mp
from multiprocessing.sharedctypes import Value
from time import sleep
from random import randint

def santa(eNum, rNum, bsemP, bsemD, osemR, osemK):
    while True:
        bsemD.acquire()
        with bsemP:
            if rNum.value == 10 and eNum.value:
                bsemP.release()
                print("Ukrcaj poklone i raznosi")
                sleep(2)
                bsemP.acquire()

                for _ in range(10):
                    osemR.release()
                rNum.value = 0
                print("Poslao sobove na godišnji")
            if rNum.value == 10:
                bsemP.release()
                print("Nahrani sobove")
                sleep(2)
                bsemP.acquire()
            while eNum.value >= 3:
                bsemP.release()
                print("Riješi probleme")
                sleep(2)
                bsemP.acquire()

                print("Pošalji ih natrag")
                for _ in range(3):
                    osemK.release()
                eNum.value -= 3

def elf(eNum, bsemP, bsemD, osemK):
    with bsemP:
        eNum.value += 1
        if eNum.value == 3:
            print("Postavio djeda")
            bsemD.release()
    osemK.acquire()

def reindeer(rNum, bsemP, osemR):
    with bsemP:
        rNum.value += 1
    osemR.acquire()

def northPole():
    s = mp.Process(target=santa, args=(elfNumber, reindeerNumber, sem['P'], sem['D'], sem['R'], sem['K']))
    s.start()
    while True:
        sleep(randint(1, 3))
        if randint(1, 100) > 50 and reindeerNumber.value < 10:
            print("Stvorio soba")
            reindeers.append(mp.Process(target=reindeer, args=(reindeerNumber, sem['P'], sem['R'],)))
            reindeers[-1].start()
        if randint(1, 100) > 50:
            print("Stvorio patuljka")
            elfs.append(mp.Process(target=elf, args=(elfNumber, sem['P'], sem['D'], sem['K'])))
            elfs[-1].start()


if __name__ == '__main__':
    elfNumber = Value('i', 0)
    reindeerNumber = Value('i', 0)
    elfs = []
    reindeers = []
    sem = {}
    sem['P'] = mp.Manager().BoundedSemaphore(1)
    sem['D'] = mp.BoundedSemaphore(1)
    sem['D'].acquire()
    sem['R'] = mp.Manager().Semaphore(10)
    sem['K'] = mp.Manager().Semaphore(3)

    northPole()
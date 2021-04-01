import signal
import time
import sys
import os
import ctypes
libcsignal = ctypes.cdll.LoadLibrary("libc.so.6")

irqEnable = True
waitList = [0]*5
priorities = [0]*6
currentPriority = 0


signals = [signal.SIGUSR1, signal.SIGUSR2, signal.SIGALRM, signal.SIGCONT, signal.SIGINT]

def printSymbol(n, symbol):
    global waitList
    global priorities
    global currentPriority
    toPrint = ''
    for i in range(6):
        if i == n:
            toPrint += f'{symbol} '
        else:
            toPrint += '- '
    print(f"{toPrint[:-1]} {waitList} {currentPriority} {priorities}")

def holdSignals(signals):
    for i in signals:
        libcsignal.sighold(i)

def releaseSignals(signals):
    for i in signals:
        libcsignal.sigrelse(i)

def killSelf(sigNumber, frame):
    sys.exit("Killed")

def doSignal(n):
    printSymbol(n, 'P')
    for i in range(5):
        printSymbol(n, i + 1)
        time.sleep(1)
    printSymbol(n, 'K')

def getMostImportant(waitList):
    tmpList = waitList.copy()
    toReturn = 0
    for i in range(len(tmpList) - 1, -1, -1):
        if tmpList[i]:
            toReturn = i + 1
            break
    return toReturn

def signalHandler(sigNumber, frame):
    global irqEnable
    global currentPriority
    global waitList
    global priorities
    holdSignals(signals)
    printSymbol(signals.index(sigNumber) + 1, 'X')
    waitList[signals.index(sigNumber)] += 1
    time.sleep(0.5)
    #print(f"Frame: {frame}")
    #print(f"waitList: {waitList}")

    signalToDo = getMostImportant(waitList)
    #print(f"signaltoDo: {signalToDo} currentProprity: {currentPriority}")
    while signalToDo > currentPriority:
        #print(f"u petlji: {signalToDo} {currentPriority}")
        #print(f"signalToDo: {signalToDo}")
        if signalToDo:
            waitList[signalToDo - 1] -= 1
            priorities[signalToDo] = currentPriority
            currentPriority = signalToDo
            releaseSignals(signals)
            doSignal(signalToDo)
            holdSignals(signals)
            currentPriority = priorities[signalToDo]
            priorities[signalToDo] = 0
        signalToDo = getMostImportant(waitList)
    releaseSignals(signals)




if __name__ == '__main__':
    for i in signals:
        signal.signal(i, signalHandler)
    signal.signal(signal.SIGTERM, killSelf)
    signal.signal(signal.SIGQUIT, killSelf)
    print(f"Obrada prekida, PID = {os.getpid()}")
    secs = 1
    while True:
        time.sleep(1)
        printSymbol(0, secs)
        secs += 1
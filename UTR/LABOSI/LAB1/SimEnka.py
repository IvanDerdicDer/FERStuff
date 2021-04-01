# Ulazni nizovi - [["a", "b", "c", ...], ["a", "t", "r", ...], ...]
tmpList = input().split("|")
inputLists = [i.split(",") for i in tmpList]

#Skup stanja - ["s1", "s2", "s3", "s4", ...]
allowedStates:list = input().split(",")

#Simboli abecede - ["a", "b", "c", "d", ...]
allowedSymbols:list = input().split(",")

#Prihvatljiva stanja - ["s1", "s2", "s3", "s4", ...]
finalStates:list = input().split(",")

#Početno stanje - "s1,s2,s3,..."
startingState:str = input()

#s1,a->s1,s2,...
#Funkcije prijelaza - {s1: {a: s1,s2,...}}
transitionFunctions = {}
try:
    tmpFunc = input()
    while tmpFunc:
        if tmpFunc.split(",", 1)[0] == '^EXIT':
            break

        currState:str = tmpFunc.split(",", 1)[0]
        transitionInput:str = tmpFunc.split(",", 1)[1].split("->")[0]
        nextStates:list = tmpFunc.split("->")[1].split(",")
        if currState not in transitionFunctions.keys():
            transitionFunctions[currState] = {}
        if not (nextStates[0] == "#" or (transitionInput == "$" and nextStates[0] == currState and len(nextStates) == 1)):
            transitionFunctions[currState][transitionInput] = nextStates

        tmpFunc = input()
except:
    pass

def epsilonClosure(currentStates:list):
    i = 0
    while i < len(currentStates):
        state = currentStates[i]
        try:
            currentStates += transitionFunctions[state]["$"]
            currentStates = list(dict.fromkeys(currentStates))
        except:
            pass
        i += 1
    return currentStates



for inputList in inputLists:
    currentStates = [startingState]
    for inputSymbol in inputList:
        currentStates = epsilonClosure(currentStates)
        currentStates.sort()
        print(f"{','.join(currentStates) if currentStates else '#'}|", end="")
        nextStates = []
        for currState in currentStates:
            try:
                nextStates += transitionFunctions[currState][inputSymbol]
            except:
                pass
        nextStates = list(dict.fromkeys(nextStates))

        currentStates = nextStates

    currentStates = epsilonClosure(currentStates)
    currentStates.sort()
    print(",".join(currentStates) if currentStates else '#')

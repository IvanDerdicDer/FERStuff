import ctypes

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
startingStates:str = input()

#Funkcije prijelaza - func --> ["s1", ["a", "s2,s3,..."]]
#                   - [func1, func2, ...]
transitionFunctions = []
try:
    tmpFunc = input().split(",", 1)
    while tmpFunc:
        if tmpFunc[0] == '^EXIT':
            break
        tmpFunc[-1] = tmpFunc[-1].split("->")
        transitionFunctions.append(tmpFunc)
        tmpFunc = input().split(",", 1)
except:
    pass

def removeDuplicates(string: str):
    uniqueList = []
    stringList = string.split(",")
    for i in stringList:
        if i not in uniqueList:
            uniqueList.append(i)
    uniqueList.sort()
    return convertStateListToStateString(uniqueList)

def removeEmptyStates(stateList: list):
    onlyEmptyStates = True
    for i in stateList:
        if i != "#":
            onlyEmptyStates = False
    if onlyEmptyStates:
        return "#"
    while "#" in stateList:
        stateList.remove("#")

    return convertStateListToStateString(stateList)

def canTransitionState(currState, inputSymbol):
    for func in transitionFunctions:
        if currState == func[0] and inputSymbol == func[1][0]:
            return True
    return False

def doStateTransition(currState, inputSymbol):
    if (currState not in allowedStates or inputSymbol not in allowedSymbols) and inputSymbol != "$":
        return False
    for func in transitionFunctions:
        if currState == func[0] and inputSymbol == func[1][0]:
            return func[1][1]
    return False

def convertStateListToStateString(stateList):
    tmpStateList = stateList.copy()
    tmpStateList.sort()
    if not stateList:
        return False
    stateStr = ''
    for i in tmpStateList:
        stateStr += f",{i}"
    return stateStr[1:]


def epsilonClosure(currState, outputStateListPointer: ctypes.pointer):
    if not currState:
        return
    currStateList: list = currState.split(",")
    outputStateListPointer.contents.value += currStateList
    outputStateListPointer.contents.value.sort()
    for state in currStateList:
        nextusStatus = doStateTransition(state, "$")
        if nextusStatus == currState:
            return
        epsilonClosure(nextusStatus, outputStateListPointer)

#Petlja za liste ulaze
for inputList in inputLists:
    currentStates: str = startingStates
    someTmpList = currentStates.split(",")
    for i in someTmpList:
        outputStateList = []
        outputStateListPointer = ctypes.pointer(ctypes.py_object([]))
        epsilonClosure(i, outputStateListPointer)
        outputStateList = outputStateListPointer.contents.value.copy()
        nextState = convertStateListToStateString(outputStateList)
        nextState = removeDuplicates(nextState)
        nextState = removeEmptyStates(nextState.split(","))
        currentStates = currentStates.replace(i, nextState if outputStateList else i)

    outputStates: str = currentStates

    #Petlja za ulaze
    for inputSymbol in inputList:
        tmpCurrentStates = currentStates.split(",")
        #Petlja za trenutna stanja
        nextState = ''
        for currState in tmpCurrentStates:
            #print(f"\t\tCurrState: {currState}")

            outputStateList = []
            outputStateListPointer = ctypes.pointer(ctypes.py_object([]))
            epsilonClosure(i, outputStateListPointer)
            outputStateList = outputStateListPointer.contents.value.copy()
            nextState = convertStateListToStateString(outputStateList)
            nextState = removeDuplicates(nextState)
            nextState = removeEmptyStates(nextState.split(","))
            currentStates = currentStates.replace(currState, nextState if outputStateList else currState)

            nextState = doStateTransition(currState, inputSymbol)

            currentStates = currentStates.replace(currState, nextState if nextState else "#", 1)

        currentStates = currentStates.split(",")
        currentStates = convertStateListToStateString(currentStates)
        currentStates = removeDuplicates(currentStates)
        currentStates = removeEmptyStates(currentStates.split(","))
        outputStates += f"|{currentStates}"

    #Na kraju petlje za liste ulaza
    print(outputStates)
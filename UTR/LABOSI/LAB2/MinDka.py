#Skup stanja - ["s1", "s2", "s3", "s4", ...]
allowedStates:list = input().split(",")

#Simboli abecede - ["a", "b", "c", "d", ...]
allowedSymbols:list = input().split(",")

#Konačna stanja - ["s1", "s2", "s3", "s4", ...]
finalStates:list = input().split(",")

#Početno stanje - "s1"
startingState:str = input()

#s1,a->s1
#Funkcije prijelaza - {s1: {a: s1}}
transitionFunctions = {}
try:
    tmpFunc = input()
    while tmpFunc:
        if tmpFunc.split(",", 1)[0] == '^EXIT':
            break

        currState:str = tmpFunc.split(",", 1)[0]
        transitionInput:str = tmpFunc.split(",", 1)[1].split("->")[0]
        nextStates:list = tmpFunc.split("->")[1]
        if currState not in transitionFunctions.keys():
            transitionFunctions[currState] = {}
        if not (nextStates[0] == "#" or (transitionInput == "$" and nextStates[0] == currState and len(nextStates) == 1)):
            transitionFunctions[currState][transitionInput] = nextStates

        tmpFunc = input()
except Exception:
    pass

def findReachableStates(transitionFunctions: dict):
    global startingState
    reachableStates = []
    queue = [startingState]
    while queue:
        reachableStates += queue
        for i in transitionFunctions[queue.pop(0)].values():
            if i not in reachableStates:
                queue.append(i)
        queue = list(dict.fromkeys(queue))
    return list(dict.fromkeys(reachableStates))

def removeUnreachable(reachableStates: list):
    global transitionFunctions
    global allowedStates
    global finalStates
    for state in allowedStates:
        if state not in reachableStates:
            transitionFunctions.pop(state)
    allowedStates = reachableStates.copy()
    for i in finalStates.copy():
        if i not in reachableStates:
            finalStates.remove(i)

def equivalenceUsingMatrix():
    equivalenceMatrix = [[True] * i for i in range(1, len(allowedStates), 1)]

    columns = allowedStates[:-1]
    rows = allowedStates[1:]

    retroactiveStatesList = {}

    for row in range(len(allowedStates)-1):
        for column in range(row + 1):
            for symbol in allowedSymbols:
                tupleKey = (transitionFunctions[rows[row]][symbol], transitionFunctions[columns[column]][symbol])
                if not((tupleKey[0] in finalStates) ^ (tupleKey[1] in finalStates)):
                    if tupleKey[0] != tupleKey[1]:
                        try:
                            if equivalenceMatrix[rows.index(tupleKey[0])][columns.index(tupleKey[1])]:
                                if tupleKey not in retroactiveStatesList:
                                    retroactiveStatesList[tupleKey] = []
                                retroactiveStatesList[tupleKey].append((rows[row], columns[column]) if not((rows[row] in finalStates) ^ (columns[column] in finalStates)) else None)
                                if not retroactiveStatesList[tupleKey][-1]:
                                    retroactiveStatesList[tupleKey].pop(-1)
                        except Exception:
                            pass
                else:
                    equivalenceMatrix[row][column] = False
                    break

    for key in retroactiveStatesList.keys():
        if not equivalenceMatrix[rows.index(key[0])][columns.index(key[1])]:
            for states in retroactiveStatesList[key]:
                equivalenceMatrix[rows.index(states[0])][columns.index(states[1])] = False

    return equivalenceMatrix


if __name__ == '__main__':
    reachableStates = findReachableStates(transitionFunctions)
    reachableStates.sort()

    removeUnreachable(reachableStates)

    equivalenceMatrix = equivalenceUsingMatrix()

    columns = allowedStates[:-1]
    rows = allowedStates[1:]
    equivalentStatesList = []
    for row in range(len(allowedStates) - 1):
        for column in range(row + 1):
            if equivalenceMatrix[row][column]:
                equivalentStatesList.append([rows[row], columns[column]] if not((rows[row] in finalStates) ^ (columns[column] in finalStates)) else None)
                if not equivalentStatesList[-1]:
                    equivalentStatesList.pop(-1)
                equivalentStatesList[-1].sort()

    statesToReplace = {i: i for i in transitionFunctions.keys()}
    for key in statesToReplace.keys():
        for equivalentStates in equivalentStatesList:
            if key in equivalentStates:
                statesToReplace[key] = equivalentStates[0]
                break

    transitionFunctionsOut = {statesToReplace[i]: {j: statesToReplace[transitionFunctions[i][j]]
                                                   for j in transitionFunctions[i].keys()}
                              for i in transitionFunctions.keys()}

    allowedStatesOut = [i for i in transitionFunctionsOut.keys()]
    allowedStatesOut.sort()
    allowedSymbolsOut = allowedSymbols.copy()
    allowedSymbolsOut.sort()
    finalStatesOut = list(set([statesToReplace[i] for i in finalStates]))
    finalStatesOut.sort()
    startingStateOut = statesToReplace[startingState]

    print(",".join(allowedStatesOut))
    print(",".join(allowedSymbolsOut))
    print(",".join(finalStatesOut))
    print(startingStateOut)
    for key in transitionFunctionsOut.keys():
        for symbol in transitionFunctionsOut[key].keys():
            print(f"{key},{symbol}->{transitionFunctionsOut[key][symbol]}")

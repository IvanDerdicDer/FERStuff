# Ulazni nizovi - [["a", "b", "c", ...], ["a", "t", "r", ...], ...]
tmpList = input().split("|")
inputLists = [i.split(",") for i in tmpList]

#Skup stanja - ["s1", "s2", "s3", "s4", ...]
allowedStates:list = input().split(",")

#Simboli abecede - ["a", "b", "c", "d", ...]
allowedSymbols:list = input().split(",")

#Simboli stoga - ["A", "B", "C", "D", ...]
stackSymbols:list = input().split(",")

#Prihvatljiva stanja - ["s1", "s2", "s3", "s4", ...]
finalStates:list = input().split(",")

#Početno stanje - "s1"
startingState:str = input()

#Početno stanje stoga - "K"
startingStackState:str = input()

#{["s1", "a", "K"]: ["s2", "NK"]}
transitionFunctions = {}
try:
    tmpFunc = input()
    while tmpFunc:
        if tmpFunc == '^EXIT':
            break

        key = tmpFunc.split('->')[0]
        data = tmpFunc.split('->')[1]
        transitionFunctions[tuple(key.split(","))] = data.split(",")

        tmpFunc = input()
except:
    pass

for inputList in inputLists:
    print(f"{startingState}#{startingStackState}|", end="")
    stack = [startingStackState]
    currentState = startingState
    hasFailed = False

    for symbol in inputList:
        key = (currentState, "$", stack.pop() if stack else "$")
        while key in transitionFunctions.keys():
            # stack.append(transitionFunctions[key][1])
            for i in reversed(transitionFunctions[key][1]):
                if i != "$":
                    stack.append(i)
            currentState = transitionFunctions[key][0]
            print(f"{currentState}#{''.join(reversed(stack)) if stack else '$'}|", end="")
            key = (currentState, "$", stack.pop() if stack else "$")
        else:
            stack.append(key[2])

        key = (currentState, symbol, stack.pop() if stack else "$")

        if key not in transitionFunctions.keys():
            print(f"fail|", end="")
            hasFailed = True
            break
        for i in reversed(transitionFunctions[key][1]):
            if i != "$":
                stack.append(i)
        currentState = transitionFunctions[key][0]
        print(f"{currentState}#{''.join(reversed(stack)) if stack else '$'}|", end="")

    key = tuple([currentState, "$", stack.pop() if stack else "$"])
    while key in transitionFunctions.keys() and currentState not in finalStates and not hasFailed:
        # stack.append(transitionFunctions[key][1])
        for i in reversed(transitionFunctions[key][1]):
            if i != "$":
                stack.append(i)
        currentState = transitionFunctions[key][0]
        print(f"{currentState}#{''.join(reversed(stack)) if stack else '$'}|", end="")
        key = (currentState, "$", stack.pop() if stack else "$")
    else:
        stack.append(key[2])

    if not hasFailed:
        if currentState in finalStates:
            print("1")
        else:
            print("0")
    else:
        print("0")
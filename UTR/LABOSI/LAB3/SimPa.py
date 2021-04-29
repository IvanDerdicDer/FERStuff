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

stack = [startingStackState]

#s1,a->s1,s2,...
#Funkcije prijelaza - {s1: {a: s1,s2,...}}
transitionFunctions = {}
try:
    tmpFunc = input()
    while tmpFunc:
        if tmpFunc == '^EXIT':
            break

        key = tmpFunc.split('->')[0]
        data = tmpFunc.split('->')[1]
        transitionFunctions[key.split(',')] = data.split(',')

        tmpFunc = input()
except:
    pass

from sys import exit

def S():
    global inputString
    global isPartOf
    global nonFinal
    nonFinal += 'S'
    if inputString[0] == 'a':
        inputString = inputString[1:]
        A()
        B()
    elif inputString[0] == 'b':
        inputString = inputString[1:]
        B()
        A()
    else:
        isPartOf = False
        exit(f"{nonFinal}\n{'DA' if isPartOf else 'NE'}")

    return

def A():
    global inputString
    global isPartOf
    global nonFinal
    nonFinal += 'A'
    if inputString[0] == 'b':
        inputString = inputString[1:]
        C()
    elif inputString[0] == 'a':
        inputString = inputString[1:]
    else:
        isPartOf = False
        exit(f"{nonFinal}\n{'DA' if isPartOf else 'NE'}")

    return

def B():
    global inputString
    global isPartOf
    global nonFinal
    nonFinal += 'B'
    if inputString[0] == 'c':
        inputString = inputString[1:]
        if inputString[0] == 'c':
            inputString = inputString[1:]
            S()
            if inputString[0] == 'b':
                inputString = inputString[1:]
                if inputString[0] == 'c':
                    inputString = inputString[1:]
                else:
                    isPartOf = False
                    exit(f"{nonFinal}\n{'DA' if isPartOf else 'NE'}")
            else:
                isPartOf = False
                exit(f"{nonFinal}\n{'DA' if isPartOf else 'NE'}")
        else:
            isPartOf = False
            exit(f"{nonFinal}\n{'DA' if isPartOf else 'NE'}")
    else:
        return

def C():
    global nonFinal
    nonFinal += 'C'
    A()
    A()

    return

if __name__ == '__main__':
    inputString = input()
    isPartOf = True
    nonFinal = ""
    S()
    print(f"{nonFinal}\n{'DA' if isPartOf else 'NE'}")
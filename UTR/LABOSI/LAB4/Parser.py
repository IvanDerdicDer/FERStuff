from sys import exit

def S():
    global inputString
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
        print(f"{nonFinal}\n{'NE'}")
        exit(0)

    return

def A():
    global inputString
    global nonFinal
    nonFinal += 'A'
    if inputString and inputString[0] == 'b':
        inputString = inputString[1:]
        C()
    elif inputString and inputString[0] == 'a':
        inputString = inputString[1:]
    else:
        print(f"{nonFinal}\n{'NE'}")
        exit(0)

    return

def B():
    global inputString
    global nonFinal
    nonFinal += 'B'
    if inputString and inputString[0] == 'c':
        inputString = inputString[1:]
        if inputString and inputString[0] == 'c':
            inputString = inputString[1:]
            S()
            if inputString and inputString[0] == 'b':
                inputString = inputString[1:]
                if inputString and inputString[0] == 'c':
                    inputString = inputString[1:]
                else:
                    print(f"{nonFinal}\n{'NE'}")
                    exit(0)
            else:
                print(f"{nonFinal}\n{'NE'}")
                exit(0)
        else:
            print(f"{nonFinal}\n{'NE'}")
            exit(0)
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
    nonFinal = ""
    S()
    print(f"{nonFinal}\n{'DA' if not inputString else 'NE'}")
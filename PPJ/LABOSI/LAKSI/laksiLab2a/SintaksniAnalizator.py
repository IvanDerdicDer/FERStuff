def loadFile() -> list:
    lexicallyAnalyzed = []
    try:
        while True:
            lexicallyAnalyzed.append(input().split(" "))

    except Exception:
        pass

    return lexicallyAnalyzed

def createDict() -> dict:
    rules = ['<program> ::= <lista_naredbi> = {IDN KR_ZA ⏊}\n',
             '<lista_naredbi> ::= <naredba> <lista_naredbi> = {IDN KR_ZA}\n',
             '<lista_naredbi> ::= $ = {KR_AZ ⏊}\n',
             '<naredba> ::= <naredba_pridruzivanja> = {IDN}\n',
             '<naredba> ::= <za_petlja> = {KR_ZA}\n',
             '<naredba_pridruzivanja> ::= IDN OP_PRIDRUZI <E> = {IDN}\n',
             '<za_petlja> ::= KR_ZA IDN KR_OD <E> KR_DO <E> <lista_naredbi> KR_AZ = {KR_ZA}\n',
             '<E> ::= <T> <E_lista> = {IDN BROJ OP_PLUS OP_MINUS L_ZAGRADA}\n',
             '<E_lista> ::= OP_PLUS <E> = {OP_PLUS}\n',
             '<E_lista> ::= OP_MINUS <E> = {OP_MINUS}\n',
             '<E_lista> ::= $ = {IDN KR_ZA KR_DO KR_AZ D_ZAGRADA ⏊}\n',
             '<T> ::= <P> <T_lista> = {IDN BROJ OP_PLUS OP_MINUS L_ZAGRADA}\n',
             '<T_lista> ::= OP_PUTA <T> = {OP_PUTA}\n',
             '<T_lista> ::= OP_DIJELI <T> = {OP_DIJELI}\n',
             '<T_lista> ::= $ = {IDN KR_ZA KR_DO KR_AZ OP_PLUS OP_MINUS D_ZAGRADA ⏊}\n',
             '<P> ::= OP_PLUS <P> = {OP_PLUS}\n',
             '<P> ::= OP_MINUS <P> = {OP_MINUS}\n',
             '<P> ::= L_ZAGRADA <E> D_ZAGRADA = {L_ZAGRADA}\n',
             '<P> ::= IDN = {IDN}\n',
             '<P> ::= BROJ = {BROJ}']

    rules = [i.replace("{", "") for i in rules]
    rules = [i.replace("}", "") for i in rules]
    rules = [i.strip() for i in rules]

    rules = [line.split(" ::= ") for line in rules]

    transitionDict = {}
    for line in rules:
        transitionDict[(line[0], tuple(line[1].split(" = ")[1].split(" ")))] = line[1].split(" = ")[0].split(" ")

    return transitionDict

def createStuffSet(transitionDict: dict) -> set:
    stuffSet = set()

    for i in transitionDict.values():
        for j in i:
            if j[0] != '<':
                stuffSet.add(j)

    return stuffSet

def main():
    lexicallyAnalyzed = loadFile()
    lexicallyAnalyzed.append('⏊')
    transitionDict = createDict()

    stuffSet = createStuffSet(transitionDict)

    output = []

    if not len(lexicallyAnalyzed):
        print("\n".join(["<program>", " <lista_naredbi>", "  $"]))
        return

    stack = [('<program>', 0)]
    line = 0
    while stack:
        stackTop = stack.pop()
        if stackTop[0] in stuffSet:
            if stackTop[0] == '$':
                output.append(" " * stackTop[1] + "$")
                continue

            output.append(" " * stackTop[1] + " ".join(lexicallyAnalyzed[line]))
            line += 1
            continue

        for key in transitionDict.keys():
            if stackTop[0] == key[0] and lexicallyAnalyzed[line][0] in key[1]:
                for i in reversed(transitionDict[key]):
                    if i == "$":
                        stack.append((i, stackTop[1] + 1))
                        break
                    else:
                        if stackTop[0] != '<P>':
                            stack.append((i, stackTop[1] + 1))

                        if key == ('<P>', ('L_ZAGRADA',)) and i != 'L_ZAGRADA':
                            stack.append((i, stackTop[1] + 1))

                        if key == ('<P>', ('OP_PLUS',)) and i != 'OP_PLUS':
                            stack.append((i, stackTop[1] + 1))

                        if key == ('<P>', ('OP_MINUS',)) and i != 'OP_MINUS':
                            stack.append((i, stackTop[1] + 1))
                else:
                    if stackTop in stuffSet:
                        line += 1

                break
        else:
            print("err " + " ".join(lexicallyAnalyzed[line] if lexicallyAnalyzed[line] != '⏊' else ['kraj']))
            return

        output.append(" " * stackTop[1] + stackTop[0])
        if stackTop[0] == '<P>':
            output.append(" " * (stackTop[1] + 1) + " ".join(lexicallyAnalyzed[line]))
            line += 1
        """print("!!!<<<---DEBUG--->>>!!!")
        for i in output:
            print(i)
        print('')"""

    print("\n".join(output))

if __name__ == '__main__':
    main()
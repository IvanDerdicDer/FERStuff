def loadFile() -> list:
    lexicallyAnalyzed = []
    try:
        while True:
            lexicallyAnalyzed.append(input().split(" "))

    except Exception:
        pass

    return lexicallyAnalyzed

def createTransitionDict() -> dict:
    rules = ['<program> ::= <lista_naredbi>\n',
             '<lista_naredbi> ::= <naredba> <lista_naredbi>\n',
             '<lista_naredbi> ::= $\n',
             '<naredba> ::= <naredba_pridruzivanja>\n',
             '<naredba> ::= <za_petlja>\n',
             '<naredba_pridruzivanja> ::= IDN OP_PRIDRUZI <E>\n',
             '<za_petlja> ::= KR_ZA IDN KR_OD <E> KR_DO <E> <lista_naredbi> KR_AZ\n',
             '<E> ::= <T> <E_lista>\n',
             '<E_lista> ::= OP_PLUS <E>\n',
             '<E_lista> ::= OP_MINUS <E>\n',
             '<E_lista> ::= $\n', '<T> ::= <P> <T_lista>\n',
             '<T_lista> ::= OP_PUTA <T>\n',
             '<T_lista> ::= OP_DIJELI <T>\n',
             '<T_lista> ::= $\n',
             '<P> ::= OP_PLUS <P>\n',
             '<P> ::= OP_MINUS <P>\n',
             '<P> ::= L_ZAGRADA <E> D_ZAGRADA\n',
             '<P> ::= IDN\n',
             '<P> ::= BROJ']

    rules = [line.split("::=") for line in rules]
    returnDict = {}
    for line in rules:
        if line[0].strip() not in returnDict.keys():
            returnDict[line[0].strip()] = []
        returnDict[line[0].strip()].append(line[1].strip().split(" "))

    return returnDict

def main():
    lexicallyAnalyzed = loadFile()
    transitionDict = createTransitionDict()
    print(transitionDict)

if __name__ == '__main__':
    main()
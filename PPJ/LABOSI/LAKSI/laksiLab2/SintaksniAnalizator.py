def loadFile() -> list:
    lexicallyAnalyzed = []
    try:
        while True:
            lexicallyAnalyzed.append(input().split(" "))

    except Exception:
        pass

    return lexicallyAnalyzed

def createDicts() -> tuple:
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

    rules = [line.split("::=") for line in rules]

    rules1 = []
    rules2 = []

    for line in rules:
        rules1.append([line[0].strip(), line[1].strip().split("=")[0].strip().split(" ")])
        rules2.append([line[0].strip(), line[1].strip().split("=")[1].strip().split(" ")])

    transitionDict = {}
    syntaxDict = {}

    for lineDict, lineSyntax in zip(rules1, rules2):
        if lineDict[0] not in transitionDict.keys():
            transitionDict[lineDict[0]] = []
        transitionDict[lineDict[0]].append(lineDict[1])

        if lineSyntax[0] not in syntaxDict.keys():
            syntaxDict[lineSyntax[0]] = []
        syntaxDict[lineSyntax[0]].append(lineSyntax[1])

    return transitionDict, syntaxDict

def main():
    lexicallyAnalyzed = loadFile()
    transitionDict, syntaxDict = createDicts()

    output = ["<program>"]

    if not len(lexicallyAnalyzed):
        print("\n".join(lexicallyAnalyzed + ["$"]))
        return

    stack = ['<program>']
    line = 0
    while stack:
        stackTop = stack.pop()
        if lexicallyAnalyzed[line][0] in syntaxDict[stackTop]:
            line += 1
            for i in transitionDict[stackTop]:
                if i == '$':
                    line -= 1
                else:
                    stack.append(i)

if __name__ == '__main__':
    main()
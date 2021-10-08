englishAlphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
keywordDict = {'za': 'KR_ZA', 'od': 'KR_OD', 'do': 'KR_DO', 'az': 'KR_AZ'}
operatorDict = {'=': 'OP_PRIDRUZI', '+': 'OP_PLUS', '-': 'OP_MINUS', '*': 'OP_PUTA', '/': 'OP_DIJELI', '(': 'L_ZAGRADA',
                ')': 'D_ZAGRADA'}

fullDict = keywordDict | operatorDict

def removeMultipleSpaces(code: str) -> str:
    """
    Removes extra whitespaces after the first whitespace
    :param code:
    :return:
    """
    workCode = [i for i in code]

    for i in range(len(workCode)):
        if workCode[i] == ' ':
            if i + 1 < len(workCode) and workCode[i + 1] == ' ':
                j = i + 1
                while workCode[j] == ' ':
                    workCode[j] = ''

    return ''.join(workCode)


def preprocessor(code: str) -> list[str]:
    """
    Makes sure that before and after every operator exists a whitespace
    :param code:
    :return:
    """

    workWithCode = [i.strip() for i in removeMultipleSpaces(code).strip().split('\n')]

    toReturn = []
    for line in workWithCode:
        line.replace('\t', ' ')
        i = 0
        while i < len(line):
            if line[i] in operatorDict.keys():
                if i - 1 > 0 and line[i - 1] != ' ' and line[i - 1] != '/':
                    line = line[:i] + ' ' + line[i:]
                    i += 1

                if i + 1 < len(line) and line[i + 1] != ' ' and line[i + 1] != '/':
                    line = line[:i + 1] + ' ' + line[i + 1:]
                    i += 1

            i += 1
        toReturn.append(line.split(' '))

    return toReturn


def isVar(var: str) -> bool:
    """
    Checks if the given string is a valid variable
    :param var:
    :return:
    """
    if var[0] in englishAlphabet:
        return True

    return False


def isComment(var: str) -> bool:
    """
    Checks if the given string is a start of a line comment
    :param var:
    :return:
    """
    if var[0] == '/' and len(var) >= 2:
        if var[1] == '/':
            return True

    return False


def isInt(num: str) -> bool:
    """
    Checks if the given string is an integer
    :param num:
    :return:
    """
    try:
        int(num)
    except ValueError:
        return False

    return True


def inputCode() -> str:
    toReturn = ''
    try:
        while True:
            toReturn += input() + '\n'
    except Exception:
        pass

    return toReturn


def main():
    workCode = preprocessor(inputCode())

    output = []

    for line in range(len(workCode)):
        for part in workCode[line]:
            if isComment(part):
                break

            if part in fullDict.keys():
                output.append(f"{fullDict[part]} {line + 1} {part}")
                continue

            if isVar(part):
                output.append(f"IDN {line + 1} {part}")
                continue

            if isInt(part):
                output.append(f"BROJ {line + 1} {part}")
                continue

    print("\n".join(output))


if __name__ == '__main__':
    main()

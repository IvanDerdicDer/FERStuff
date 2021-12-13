from sys import exit
from enum import Enum

class InitType(Enum):
    EQ = 0
    ZA = 1
    NAN = 2

class TreeNode:
    def __init__(self, initValue: tuple[str, int], parentNode = None) -> None:
        self.value = initValue[0]
        self.depth = initValue[1]
        self.parentNode: TreeNode = parentNode
        self.children = []

    def addChild(self, child) -> None:
        self.children.append(child)

    def getChildren(self) -> list:
        return self.children

    def __str__(self):
        return f"{self.value}, {self.depth}"

    def __repr__(self):
        return f"{self.value}, {self.depth}"

def inputFile() -> list[tuple[str, int]]:
    toReturn = []
    inputLine = None
    while True:
        try:
            inputLine = input()
            toReturn.append((inputLine.strip(), len(inputLine) - len(inputLine.lstrip(" "))))
        except Exception:
            break

    return toReturn

def generateTree(notATree: list[tuple[str, int]], root: TreeNode, previousDepth: int) -> None:
    notATree.pop(0)

    if not len(notATree):
        return

    if previousDepth == notATree[0][1]:
        return

    while len(notATree) and notATree[0][1] > previousDepth:
        child = TreeNode(notATree[0], root)
        generateTree(notATree, child, notATree[0][1])
        root.addChild(child)

def printTree(root: TreeNode) -> None:
    print(" " * root.depth + root.value)
    for child in root.getChildren():
        printTree(child)

def checkInitType(child: TreeNode):
    children: list[TreeNode] = child.parentNode.getChildren()
    childIndex = children.index(child)

    if childIndex < len(children) - 1 and children[childIndex + 1].value.startswith("OP_PRIDRUZI"):
        return InitType.EQ

    if 0 < childIndex and children[childIndex - 1].value.startswith("KR_ZA"):
        return InitType.ZA

    return InitType.NAN

def getAllIDN(root: TreeNode, returnDict: dict[str, list[tuple[int, InitType]]]) -> None:
    if root.value.startswith("IDN"):
        if root.value.split(" ")[2] not in returnDict:
            returnDict[root.value.split(" ")[2]] = []
        initType = checkInitType(root)
        returnDict[root.value.split(" ")[2]].append((int(root.value.split(" ")[1]), initType))

    for child in root.getChildren():
        getAllIDN(child, returnDict)

def wasZAInit(depth: int, depths: list[tuple[int, InitType]]):
    useList = [i for i in depths if i[0] < depth]
    for depth1 in reversed(useList):
        if depth1[1] == InitType.ZA:
            return depth1

    return False

def wasEQInit(depth: int, depths: list[tuple[int, InitType]]):
    useList = [i for i in depths if i[0] < depth]
    for depth1 in useList:
        if depth1[1] == InitType.EQ:
            return depth1

    return False

def semanticallyAnalyze(root: TreeNode, idnDict: dict[str, list[tuple[int, InitType]]]):
    if root.value.startswith("IDN"):
        if checkInitType(root) == InitType.NAN:
            zaInit = wasZAInit(int(root.value.split(' ')[1]), idnDict[root.value.split(" ")[2]])
            eqInit = wasEQInit(int(root.value.split(' ')[1]), idnDict[root.value.split(" ")[2]])
            if zaInit:
                print(f"{root.value.split(' ')[1]} {zaInit[0]} {root.value.split(' ')[2]}")
            elif eqInit:
                print(f"{root.value.split(' ')[1]} {eqInit[0]} {root.value.split(' ')[2]}")
            elif not(zaInit or eqInit):
                print(f"err {root.value.split(' ')[1]} {root.value.split(' ')[2]}")
                exit(0)

    for child in root.getChildren():
        semanticallyAnalyze(child, idnDict)

def main():
    notATree = inputFile()

    treeRoot = TreeNode(("<program>", 0))
    generateTree(notATree, treeRoot, 0)
    idnDict = {}
    getAllIDN(treeRoot, idnDict)

    semanticallyAnalyze(treeRoot, idnDict)

if __name__ == '__main__':
    main()
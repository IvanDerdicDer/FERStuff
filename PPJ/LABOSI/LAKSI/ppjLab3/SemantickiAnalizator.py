from sys import exit
from enum import Enum

class InitType(Enum):
    EQ = 0
    ZA = 1
    NAN = 2
    NOT = 3

class TreeNode:
    def __init__(self, initValue: tuple, parentNode = None) -> None:
        self.value: str = initValue[0]
        self.depth: int = initValue[1]
        self.parentNode: TreeNode = parentNode
        self.children = []

    def addChild(self, child) -> None:
        self.children.append(child)

    def getChildren(self) -> list:
        return self.children

    def __str__(self):
        return f"[{self.value}, {self.depth}]"

    def __repr__(self):
        return f"[{self.value}, {self.depth}]"

def inputFile() -> list:
    toReturn = []
    inputLine = None
    while True:
        try:
            inputLine = input()
            toReturn.append((inputLine.strip(), len(inputLine) - len(inputLine.lstrip(" "))))
        except Exception:
            break

    return toReturn

def generateTree(notATree: list, root: TreeNode, previousDepth: int) -> None:
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
    print(" " * root.depth + root.value + f" | {root.depth}")
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


def isChildOf(parent: TreeNode, child: TreeNode) -> bool:
    if child is parent:
        return True

    if child.parentNode is None:
        return False

    return isChildOf(parent, child.parentNode)

def getParentZaLoop(child: TreeNode):
    if child.parentNode is None:
        return child

    if child.value == "<za_petlja>":
        return child

    return getParentZaLoop(child.parentNode)

def getLastZaLoop(root: TreeNode, node: TreeNode):
    if root.value.startswith("KR_ZA"):
        if isChildOf(root.parentNode, node):
            return root

    for child in root.getChildren():
        checkVar = getLastZaLoop(child, node)
        if checkVar:
            return checkVar

    return None


def checkIdnDef(root: TreeNode, node: TreeNode) -> TreeNode:
    if root.value.startswith("IDN"):
        if checkInitType(root) == InitType.EQ:
            if root.value.split(" ")[2] == node.value.split(" ")[2]:
                zaNode = getParentZaLoop(root)
                if isChildOf(zaNode, node):
                    return root

    for child in root.getChildren():
        checkVar = checkIdnDef(child, node)
        if checkVar:
            return checkVar

    return None

def checkZaDef(root: TreeNode, node: TreeNode) -> TreeNode:
    if root.value.startswith("IDN"):
        if checkInitType(root) == InitType.ZA:
            if root.value.split(" ")[2] == node.value.split(" ")[2]:
                return root

    for child in root.getChildren():
        zaVar = checkZaDef(child, node)
        if zaVar:
            return zaVar

    return None

def getTreeRoot(node: TreeNode) -> TreeNode:
    if node.parentNode is None:
        return node

    return getTreeRoot(node.parentNode)

def semanticallyAnalyze2(root: TreeNode):
    while root.value.startswith("IDN"):
        if checkInitType(root) == InitType.NAN:
            lastZa = getLastZaLoop(getTreeRoot(root), root)
            zaVar = checkZaDef(lastZa.parentNode, root) if lastZa else None
            eqVar = checkIdnDef(getTreeRoot(root), root)

            if zaVar and eqVar:
                if isChildOf(zaVar.parentNode, root):
                    if zaVar.value.split(" ")[1] == root.value.split(' ')[1]:
                        print(f"err {root.value.split(' ')[1]} {root.value.split(' ')[2]}")
                        exit(0)

                    print(f"{root.value.split(' ')[1]} {zaVar.value.split(' ')[1]} {root.value.split(' ')[2]}")
                    break

                if eqVar.value.split(" ")[1] == root.value.split(' ')[1]:
                    print(f"err {root.value.split(' ')[1]} {root.value.split(' ')[2]}")
                    exit(0)

                print(f"{root.value.split(' ')[1]} {eqVar.value.split(' ')[1]} {root.value.split(' ')[2]}")
                break


            if zaVar:
                if zaVar.value.split(" ")[1] == root.value.split(' ')[1]:
                    print(f"err {root.value.split(' ')[1]} {root.value.split(' ')[2]}")
                    exit(0)

                print(f"{root.value.split(' ')[1]} {zaVar.value.split(' ')[1]} {root.value.split(' ')[2]}")
                break

            if eqVar:
                if eqVar.value.split(" ")[1] == root.value.split(' ')[1]:
                    print(f"err {root.value.split(' ')[1]} {root.value.split(' ')[2]}")
                    exit(0)

                print(f"{root.value.split(' ')[1]} {eqVar.value.split(' ')[1]} {root.value.split(' ')[2]}")
                break

            print(f"err {root.value.split(' ')[1]} {root.value.split(' ')[2]}")
            exit(0)
        break

    for child in root.getChildren():
        semanticallyAnalyze2(child)

def main():
    notATree = inputFile()

    treeRoot = TreeNode(("<program>", 0))
    generateTree(notATree, treeRoot, 0)

    semanticallyAnalyze2(treeRoot)

if __name__ == '__main__':
    main()
import argparse
import queue
from typing import Tuple, List, Dict
from time import time

GRAPH = Dict[str, List[Dict]]
HEURISTIC = Dict[str, int]


class TreeNode:
    def __init__(self,
                 label: str = '',
                 weight: int = 0,
                 heuristic: int = 0,
                 depth: int = None,
                 parent=None,
                 children=None):
        """
        Init function
        :param label: Node label
        :param weight: Node weight
        :param heuristic: Node heuristic
        :param depth: Node depth
        :param parent: Nodes parent
        :param children: Nodes children
        """
        if children is None:
            children = []

        self.label = label
        self.weight = weight
        self.heuristic = heuristic
        self.depth = depth
        self.parent = parent
        self.children = children

    def __repr__(self):
        return f'({self.label}, {self.weight}, {self.heuristic}, {self.depth})'


class UCSNode(TreeNode):
    def __eq__(self, other):
        return self.weight == other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __lt__(self, other):
        return self.weight < other.weight


class AstarNode(TreeNode):
    def __eq__(self, other):
        return self.heuristic == other.heuristic

    def __gt__(self, other):
        return self.heuristic > other.heuristic

    def __lt__(self, other):
        return self.heuristic < other.heuristic


def parse_arguments() -> argparse.Namespace:
    """
    Function that parses command line arguments
    :return:
    """
    parser = argparse.ArgumentParser(description="A script that tests different space search algorithms")

    parser.add_argument('--alg',
                        type=str,
                        help='Algorithm to be used. One of the following: bfs, ucs, astar')
    parser.add_argument('--ss',
                        type=str,
                        help='Path to the file containing the states')
    parser.add_argument('--h',
                        type=str,
                        help='Path to the file containing the heuristic')
    parser.add_argument('--check-optimistic',
                        action='store_true',
                        default=False,
                        help='Flag to be set if you want to check how optimistic is the heuristic')
    parser.add_argument('--check-consistent',
                        action='store_true',
                        default=False,
                        help='Flag to be set if you want to check how consistent is the heuristic')

    return parser.parse_args()


def load_file(filepath: str) -> List[str]:
    """
    Function that loads a given file to memory as a list of file lines
    :param filepath:
    :return:
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        file: List[str] = f.readlines()

    file = [line.strip() for line in file if not line.startswith('#')]

    return file


def check_child_exists_in_path(parent: TreeNode, child: TreeNode):
    """
    Checks if child exists in the current path
    :param parent:
    :param child:
    :return:
    """
    while parent.parent:
        if parent.parent.label == child.label:
            return True

        parent = parent.parent

    return False


def space_search(start: str, destination: str, graph: GRAPH, sorting: bool = False, node_type=TreeNode) -> Tuple:
    """
    Function that searches for the path from the start to the destination for the given graph
    :param node_type: Type of the node that is used
    :param start: Label of the start node
    :param destination: Label of the destination node
    :param graph: Graph that gets searched
    :param sorting: Key for the sort algorith
    :return:
    """
    kwargs = {
        'label': start,
        'depth': 0
    }

    tree: node_type = node_type(**kwargs)
    q: queue.LifoQueue = queue.LifoQueue()
    q.put(tree)
    if sorting:
        q: queue.PriorityQueue = queue.PriorityQueue()
        q.put(tree)

    while q.qsize() != 0:
        first: node_type = q.get()

        if first.parent:
            first.parent.children.append(first)

        if first.label == destination:
            return tree, first

        if first.depth + 1 < len(graph):
            to_append = []
            for i in graph[first.label]:
                i['weight'] += first.weight
                i['depth'] = first.depth + 1
                i['parent'] = first
                node = node_type(**i)

                # Ensures no infinite loops happen
                if not check_child_exists_in_path(first, node):
                    to_append.append(node)

            for i in to_append:
                q.put(i)

    return None, None


def proces_bare_graph(g: List[str]) -> Tuple[str, str, GRAPH]:
    """
    Turns the raw input from loading the file into a data structure
    :param g: Raw input
    :return:
    """
    start = g.pop(0)
    destination = g.pop(0)

    graph = {i.split(': ')[0]: i.split(': ')[1] for i in g}

    for key in graph:
        kwarg_list = []
        for value in graph[key].split(' '):
            kwarg_list.append({
                'label': value.split(',')[0],
                'weight': int(value.split(',')[1])
            })

        graph[key] = kwarg_list

    return start, destination, graph


def proces_bare_heuristic(h: List[str]) -> HEURISTIC:
    """
    Turns the raw input from loading the file into a data structure
    :param h: Raw input
    :return:
    """
    heuristic = {i.split(': ')[0]: int(i.split(': ')[1]) for i in h}

    return heuristic


def add_heuristic_to_graph(graph: GRAPH, heuristic: HEURISTIC) -> GRAPH:
    """
    Adds the heuristic to graph nodes
    :param graph: Graph to be searched
    :param heuristic: Heuristic dict
    :return:
    """
    for key in graph:
        for node in graph[key]:
            node['heuristic'] = heuristic[node['label']]

    return graph


def get_path(destination: TreeNode):
    path_list = [destination.label]
    while destination.parent:
        path_list.append(destination.parent.label)
        destination = destination.parent

    return list(reversed(path_list))


def main():
    args = parse_arguments()

    if args.alg == 'bfs':
        start, destination, graph = proces_bare_graph(load_file(args.ss))
        tree, destination = space_search(start, destination, graph)
        path = get_path(destination)
        print(path)
        print(len(path))
        return

    if args.alg == 'ucs':
        start, destination, graph = proces_bare_graph(load_file(args.ss))
        tree, destination = space_search(start, destination, graph, True, UCSNode)
        path = get_path(destination)
        print(path)
        print(len(path))
        return

    if args.alg == 'astar':
        start, destination, graph = proces_bare_graph(load_file(args.ss))
        heuristic = proces_bare_heuristic(load_file(args.h))
        graph = add_heuristic_to_graph(graph, heuristic)
        tree, destination = space_search(start, destination, graph, True, AstarNode)
        path = get_path(destination)
        print(path)
        print(len(path))
        return


if __name__ == '__main__':
    start_time = time()
    main()
    print(F"Time taken > {time() - start_time}")

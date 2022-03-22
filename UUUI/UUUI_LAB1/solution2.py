import argparse
import os
from collections import deque
from time import time
from typing import Tuple, List, Dict

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

    def __eq__(self, other):
        return all([
            self.label == other.label,
            (self.weight + self.heuristic) == (other.weight + other.heuristic)
        ])


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


def check_was_visited(states: List[TreeNode], child: TreeNode):
    """

    :param states:
    :param child:
    :return:
    """
    for state in states:
        if state.label == child.label:
            return state

    return None


def proces_bare_graph(g: List[str]) -> Tuple[str, List[str], GRAPH]:
    """
    Turns the raw input from loading the file into a data structure
    :param g: Raw input
    :return:
    """
    start = g.pop(0)
    destination: List[str] = g.pop(0).split(' ')

    graph = {i.split(':')[0]: i.split(':')[1].strip() for i in g}

    for key in graph:
        kwarg_list = []
        for value in graph[key].split(' '):
            kwarg_list.append({
                                  'label': value.split(',')[0],
                                  'weight': int(value.split(',')[1])
                              } if value else {
                'label': '',
                'weight': 0
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
    """
    Function that gets the full path
    :param destination: Target state
    :return:
    """
    path_list = [destination.label]
    while destination.parent:
        path_list.append(destination.parent.label)
        destination = destination.parent

    return list(reversed(path_list))


def get_number_of_nodes(tree: TreeNode):
    count = 0

    stack = [tree]

    while stack:
        top = stack.pop()

        count += 1

        for child in reversed(top.children):
            stack.append(child)

    return count


def print_solution(alg: str, heuristic_file: str, tree: TreeNode, destination: TreeNode):
    """
    Function that prints the solution is the correct format
    :param alg: Algorithm used
    :param heuristic_file: Name of the file
    :param tree: Complete tree
    :param destination: Found solution
    :return:
    """

    if alg == 'astar':
        print(f'# A-STAR {heuristic_file}')
    else:
        print(f'# {alg.upper()}')

    print(f'[FOUND_SOLUTION]: {"yes" if destination else "no"}')

    print(f"[STATES_VISITED]: {get_number_of_nodes(tree)}")

    path = get_path(destination) if destination else []

    print(f"[PATH_LENGTH]: {len(path)}")

    print(f"[TOTAL_COST]: {destination.weight:.1f}")

    print(f'[PATH]: {" => ".join(path)}')


def bfs(start: str, destination: List[str], graph: GRAPH):
    kwargs = {
        'label': start,
        'depth': 0
    }

    tree: TreeNode = TreeNode(**kwargs)
    q: deque = deque()
    q.append(tree)

    visited = []

    while q:
        first = q.popleft()

        if first.label in destination:
            return tree, first




def main():
    args = parse_arguments()

    if args.alg == 'bfs':
        start, destination, graph = proces_bare_graph(load_file(args.ss))
        tree, destination = None, None
        print_solution(args.alg, None, tree, destination)
        return

    if args.alg == 'ucs':
        start, destination, graph = proces_bare_graph(load_file(args.ss))
        tree, destination = None, None
        print_solution(args.alg, None, tree, destination)
        return

    if args.alg == 'astar':
        start, destination, graph = proces_bare_graph(load_file(args.ss))
        heuristic = proces_bare_heuristic(load_file(args.h))
        graph = add_heuristic_to_graph(graph, heuristic)
        tree, destination = None, None
        print_solution(args.alg, os.path.basename(args.h), tree, destination)
        return


if __name__ == '__main__':
    start_time = time()
    main()
    print(F"Time taken > {time() - start_time}")

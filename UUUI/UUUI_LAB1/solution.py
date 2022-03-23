import argparse
from collections import deque
from queue import PriorityQueue
from typing import Tuple, List, Dict

GRAPH = Dict[str, List[Dict[str, int]]]
HEURISTIC = Dict[str, int]


class Node:
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
        return f'({self.label}, {self.weight + self.heuristic})'


class UCSNode(Node):
    def __lt__(self, other):
        if self.weight == other.weight:
            return self.label < other.label
        return self.weight < other.weight


class AstarNode(Node):
    def __lt__(self, other):
        if (self.weight + self.heuristic) == (other.weight + other.heuristic):
            return self.label < other.label
        return (self.weight + self.heuristic) < (other.weight + other.heuristic)


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


def bfs(start: str, destination: List[str], graph: GRAPH):
    """
    Executes the BFS algorithm to find the path from start to one of the destinations for a given graph
    :param start:
    :param destination:
    :param graph:
    :return:
    """
    kwargs = {
        'label': start,
        'depth': 0
    }

    tree: Node = Node(**kwargs)
    q: deque = deque()
    q.append(tree)

    visited = {tree.label}

    node_count = len(graph)

    while q:
        first: Node = q.popleft()

        if first.parent:
            first.parent.children.append(first)

        if first.label in destination:
            return tree, first

        if first.depth + 1 < node_count:
            to_append = []

            for i in graph[first.label]:
                i['depth'] = first.depth + 1
                i['parent'] = first
                node = Node(**i)

                node.weight += first.weight

                if node.label not in visited:
                    visited.add(node.label)
                    to_append.append(node)

            to_append.sort(key=lambda x: x.label)

            for i in to_append:
                q.append(i)

    return tree, None


def ucs(start: str, destination: List[str], graph: GRAPH):
    """
    Executes the UCS algorithm to find the path from start to one of the destinations for a given graph
    :param start:
    :param destination:
    :param graph:
    :return:
    """
    kwargs = {
        'label': start,
        'depth': 0
    }

    tree: UCSNode = UCSNode(**kwargs)
    q: PriorityQueue = PriorityQueue()
    q.put(tree)

    visited = {tree.label}

    node_count = len(graph)

    while q:
        first: UCSNode = q.get()

        visited.add(first.label)

        if first.parent:
            first.parent.children.append(first)

        if first.label in destination:
            return tree, first

        if first.depth + 1 < node_count:
            for i in graph[first.label]:
                i['depth'] = first.depth + 1
                i['parent'] = first
                node = UCSNode(**i)

                node.weight += first.weight

                if node.label not in visited:
                    q.put(node)

    return tree, None


def astar(start: str, destination: List[str], graph: GRAPH):
    """
    Executes the A* algorithm to find the path from start to one of the destinations for a given graph with heuristic
    :param start:
    :param destination:
    :param graph:
    :return:
    """
    kwargs = {
        'label': start,
        'depth': 0
    }

    tree: AstarNode = AstarNode(**kwargs)
    q: PriorityQueue = PriorityQueue()
    q.put(tree)

    visited = {tree.label: tree.weight}

    node_count = len(graph)

    while q:
        first: AstarNode = q.get()

        if first.parent:
            first.parent.children.append(first)

        if first.label in destination:
            return tree, first

        visited[first.label] = first.weight

        if first.depth + 1 < node_count:
            for i in graph[first.label]:
                i['depth'] = first.depth + 1
                i['parent'] = first
                node = AstarNode(**i)

                node.weight += first.weight

                if node.label in visited and visited[node.label] < node.weight:
                    continue

                if node.label in visited and visited[node.label] > node.weight:
                    visited[node.label] = node.weight

                q.put(node)

    return tree, None


def check_is_optimistic(destination: List[str], graph: GRAPH, heuristic: HEURISTIC):
    """
    Function that checks if the given heuristic is optimistic
    :param destination:
    :param graph:
    :param heuristic:
    :return:
    """
    s = {}

    size = 0

    for key in graph:
        s[key] = size
        size += 1

    distance = [[0 for i in range(size)] for j in range(size)]

    for i in range(size):
        for j in range(size):
            distance[i][j] = 0 if i == j else float('inf')

    for state, next_states in graph.items():
        for next_state in next_states:
            if next_state['label']:
                distance[s[state]][s[next_state['label']]] = next_state['weight']

    for k in range(size):
        for i in range(size):
            for j in range(size):
                if distance[i][j] > (distance[i][k] + distance[k][j]):
                    distance[i][j] = distance[i][k] + distance[k][j]

    bl = True
    optimistic_heuristic: Dict[str, Dict] = {i: {'bl': True} for i in heuristic}
    for state in graph:
        min_distance = distance[s[state]][s[destination[0]]]
        for i in range(len(destination)):
            min_distance = min(min_distance, distance[s[state]][s[destination[i]]])

        is_optimistic = heuristic[state] <= min_distance
        bl &= is_optimistic
        optimistic_heuristic[state]['bl'] &= is_optimistic
        optimistic_heuristic[state]['b'] = is_optimistic
        optimistic_heuristic[state]['min_distance'] = min_distance

    return optimistic_heuristic, bl


def print_is_optimistic(optimistic_heuristic: Dict[str, Dict], heuristic: HEURISTIC, h_path: str, bl):
    print(f"# HEURISTIC-OPTIMISTIC {h_path}")

    for state in optimistic_heuristic:
        print(f"[CONDITION]: {'[OK]' if optimistic_heuristic[state]['b'] else '[ERR]'} h({state}) <= h*: {heuristic[state]:.1f} <= {optimistic_heuristic[state]['min_distance']:.1f}")

    print(f"[CONCLUSION]: Heuristic {'is' if bl else 'is not'} optimistic.")


def check_is_consistent(graph: GRAPH, heuristic: HEURISTIC):
    consistent_heuristic = []

    bl = True
    for state, next_states in graph.items():
        for next_state in next_states:
            if next_state['label']:
                b = heuristic[state] <= heuristic[next_state['label']] + next_state['weight']
                bl &= b
                consistent_heuristic.append({
                    'b': b,
                    'state': state,
                    'next_state': next_state
                })

    return consistent_heuristic, bl


def print_is_consistent(consistent_heuristic, heuristic: HEURISTIC, bl, h_path):
    print(f"# HEURISTIC-OPTIMISTIC {h_path}")

    for i in consistent_heuristic:
        print(f"[CONDITION]: {'[OK]' if i['b'] else '[ERR]'} h({i['state']}) <= h({i['next_state']['label']}) + c: {heuristic[i['state']]:.1f} <= {heuristic[i['next_state']['label']]:.1f} + {i['next_state']['weight']:.1f}")

    print(f"[CONCLUSION]: Heuristic {'is' if bl else 'is not'} consistent.")


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
            if node['label']:
                node['heuristic'] = heuristic[node['label']]

    return graph


def get_path(destination: Node):
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


def get_number_of_nodes(tree: Node):
    count = 0

    stack = [tree]

    while stack:
        top = stack.pop()

        count += 1

        for child in reversed(top.children):
            stack.append(child)

    return count


def print_solution(alg: str, heuristic_file: str, tree: Node, destination: Node):
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

    if not destination:
        return

    print(f"[STATES_VISITED]: {get_number_of_nodes(tree)}")

    path = get_path(destination) if destination else []

    print(f"[PATH_LENGTH]: {len(path)}")

    print(f"[TOTAL_COST]: {destination.weight:.1f}")

    print(f'[PATH]: {" => ".join(path)}')


def main():
    args = parse_arguments()

    if args.check_optimistic:
        _, destination, graph = proces_bare_graph(load_file(args.ss))
        heuristic = proces_bare_heuristic(load_file(args.h))
        optimistic_heuristic, bl = check_is_optimistic(destination, graph, heuristic)
        print_is_optimistic(optimistic_heuristic, heuristic, args.h, bl)
        return

    if args.check_consistent:
        _, _, graph = proces_bare_graph(load_file(args.ss))
        heuristic = proces_bare_heuristic(load_file(args.h))
        consistent_heuristic, bl = check_is_consistent(graph, heuristic)
        print_is_consistent(consistent_heuristic, heuristic, bl, args.h)
        return

    if args.alg == 'bfs':
        start, destination, graph = proces_bare_graph(load_file(args.ss))
        tree, destination = bfs(start, destination, graph)
        print_solution(args.alg, None, tree, destination)
        return

    if args.alg == 'ucs':
        start, destination, graph = proces_bare_graph(load_file(args.ss))
        tree, destination = ucs(start, destination, graph)
        print_solution(args.alg, None, tree, destination)
        return

    if args.alg == 'astar':
        start, destination, graph = proces_bare_graph(load_file(args.ss))
        heuristic = proces_bare_heuristic(load_file(args.h))
        graph = add_heuristic_to_graph(graph, heuristic)
        tree, destination = astar(start, destination, graph)
        print_solution(args.alg, args.h, tree, destination)
        return


if __name__ == '__main__':
    main()

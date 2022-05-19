from typing import List, Dict, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
import math
from copy import deepcopy
import argparse

DATASET = Dict[str, List[str]]
GOAL_COUNT = Dict[str, Dict[str, Dict[str, int]]]
GOAL_DICT = Dict[str, Dict[str, int]]
ENTROPY_DICT = Dict[str, float]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        'dataset',
        type=str
    )

    p.add_argument(
        'test_dataset',
        type=str
    )

    p.add_argument(
        'depth',
        type=int,
        nargs='?'
    )

    return p.parse_args()


@dataclass(frozen=True)
class Dataset:
    header: List[str]
    goals: Set[str]
    data: DATASET

    def __contains__(self, item):
        return item in self.header

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value
        if key not in self.header:
            self.header.append(key)

    def __delitem__(self, key):
        del self.data[key]
        self.header.pop(self.header.index(key))

    def __iter__(self):
        return iter(self.header)

    def __copy__(self):
        return Dataset(self.header.copy(), self.goals.copy(), deepcopy(self.data))

    def copy(self):
        return self.__copy__()


def csv_parser(filepath: str) -> Dataset:
    with open(filepath, 'r') as f:
        values = [i.strip().split(',') for i in f.readlines()]

    header = values.pop(0)
    header_mapping = {header.index(i): i for i in header}

    to_return = {i: [] for i in header}

    for i in values:
        for j, index in zip(i, range(len(i))):
            to_return[header_mapping[index]].append(j)

    return Dataset(header, set(to_return[header[-1]]), to_return)


def dataset_subset(dataset: Dataset, column: str, value: str):
    new_dataset: Dataset = Dataset(
        [i for i in dataset if i != column],
        dataset.goals.copy(),
        {i: [] for i in dataset if i != column}
    )

    for value_d, index in zip(dataset[column], range(len(dataset[column]))):
        if value_d == value:
            for key in new_dataset:
                new_dataset[key].append(dataset[key][index])

    return new_dataset


@dataclass(frozen=True)
class Node:
    dataset: Dataset
    depth: int
    goals: Optional[Dict[str, int]]
    entropy: Optional[float]
    attribute: str
    children: Dict[str, Optional[Any]] = field(default_factory=dict)
    parent: Optional[Any] = None
    connection: Optional[str] = None


STACK_ENTRY = Tuple[Node, Optional[Dataset]]
STACK = List[STACK_ENTRY]


class ID3:
    def __init__(self, depth_limit: Optional[int] = None):
        self.root: Optional[Node] = None
        self.depth_limit: Optional[int] = depth_limit

    @staticmethod
    def count_goal(dataset: Dataset) -> Tuple[GOAL_COUNT, int]:
        to_return = {i: {} for i in list(dataset)[:-1]}
        goal_column = list(dataset)[-1]

        base = len(dataset.goals)

        for key in list(dataset)[:-1]:
            for value, goal in zip(dataset[key], dataset[goal_column]):
                if value not in to_return[key]:
                    to_return[key][value] = {i: 0 for i in dataset.goals}

                to_return[key][value][goal] += 1

        return to_return, base

    @staticmethod
    def calculate_entropy(data: Dict[str, int], base: int) -> float:
        all_goals_count = 0
        for key in data:
            all_goals_count += data[key]

        to_return = sum(
            -(data[i] / all_goals_count) * math.log(data[i] / all_goals_count, base) if data[i] != 0 else 0 for i in
            data)

        return to_return

    def ig(self, data: Dict[str, int], x: Dict[str, Dict[str, int]], base: int) -> float:
        all_goals_count = 0
        for key in data:
            all_goals_count += data[key]

        to_return = self.calculate_entropy(data, base) + sum(
            -(sum(x[i][j] for j in x[i]) / all_goals_count) * self.calculate_entropy(x[i], base) for i in x)
        return to_return

    @staticmethod
    def get_goal_dict(goal_count: GOAL_COUNT) -> GOAL_DICT:
        goal_dict = dict.fromkeys(goal_count)
        for key in goal_count:
            for value in goal_count[key]:
                if not goal_dict[key]:
                    goal_dict[key] = {i: 0 for i in goal_count[key][value]}
                for goal in goal_count[key][value]:
                    goal_dict[key][goal] += goal_count[key][value][goal]

        return goal_dict

    def get_entropy_dict(self, goal_dict: GOAL_DICT, goal_count: GOAL_COUNT, base: int) -> ENTROPY_DICT:
        entropy_dict = dict.fromkeys(goal_count)
        for key in goal_count:
            entropy_dict[key] = self.ig(goal_dict[key], goal_count[key], base)

        return entropy_dict

    def all_entropy(self, goal_count: GOAL_COUNT, base: int) -> Tuple[ENTROPY_DICT, GOAL_DICT]:
        goal_dict = self.get_goal_dict(goal_count)

        entropy_dict = self.get_entropy_dict(goal_dict, goal_count, base)

        if entropy_dict:
            for i in entropy_dict:
                print(f"IG({i}) = {entropy_dict[i]:.5f} ", end='')
            print()

        return entropy_dict, goal_dict

    def get_next_node(self, dataset: Dataset, connection: Optional[str], parent: Optional[Node] = None) -> Optional[Node]:
        goal_count, base = self.count_goal(dataset)

        this_goals = None
        if parent is not None:
            this_goals = {i: 0 for i in parent.goals}
            for i in dataset[dataset.header[-1]]:
                this_goals[i] += 1

        if parent is not None and parent.depth + 1 == self.depth_limit:
            return Node(
                dataset,
                parent.depth + 1,
                None,
                None,
                max(sorted(this_goals), key=lambda x: {i: this_goals[i] for i in sorted(this_goals)}[x]),
                parent=parent,
                connection=connection
            )

        entropy_dict, goal_dict = self.all_entropy(goal_count, base)

        if not entropy_dict:
            if len(dataset) == 1:
                return Node(
                    dataset,
                    parent.depth + 1 if parent else 0,
                    None,
                    None,
                    dataset[dataset.header[-1]][-1],
                    {},
                    parent,
                    connection
                )

            return Node(
                dataset,
                parent.depth + 1 if parent else 0,
                None,
                None,
                max(sorted(parent.goals), key=lambda x: {i: parent.goals[i] for i in sorted(parent.goals)}[x]),
                {},
                parent,
                connection
            )

        next_node = max(entropy_dict, key=lambda x: entropy_dict[x])

        return Node(
            dataset,
            parent.depth + 1 if parent else 0,
            goal_dict[next_node],
            entropy_dict[next_node],
            next_node,
            dict.fromkeys(goal_count[next_node]),
            parent,
            connection
        )

    def build_tree(self, dataset: Dataset) -> None:
        to_root = self.get_next_node(dataset, None)

        self.root = to_root

        stack: STACK = [(self.root, dataset.copy())]

        while stack:
            top: STACK_ENTRY = stack.pop()

            for child in top[0].children:
                sub_dataset = dataset_subset(top[1], top[0].attribute, child)
                new_node = self.get_next_node(sub_dataset, child, top[0])

                if new_node.entropy == 0.0:
                    new_node = Node(
                        new_node.dataset,
                        new_node.depth,
                        new_node.goals,
                        new_node.entropy,
                        max(sorted(new_node.goals), key=lambda x: {i: new_node.goals[i] for i in sorted(new_node.goals)}[x]),
                        {},
                        new_node.parent,
                        new_node.connection
                    )

                top[0].children[child] = new_node
                stack.append((top[0].children[child], sub_dataset.copy()))

    def fit(self, dataset: Dataset):
        self.build_tree(dataset)

        pass

    def print_branches(self):
        print('[BRANCHES]:')
        stack: List[Node] = [self.root]

        while stack:
            top = stack.pop()

            if not top.children:
                print_stack: List[str] = [top.attribute]
                connection: str = top.connection
                parent: Node = top.parent
                while parent:
                    print_stack.append(f"{parent.depth + 1}:{parent.attribute}={connection}")
                    connection = parent.connection
                    parent = parent.parent

                print(' '.join(reversed(print_stack)))

            for child in reversed(list(top.children)):
                stack.append(top.children[child])

    def predict(self, dataset: Dataset):
        count_correct: int = 0
        n = len(dataset.goals)
        goals = list(dataset.goals)
        goals.sort()
        matrix = [[0 for j in range(n)] for i in range(n)]
        self.print_branches()
        print('[PREDICTIONS]:', end='')
        for index in range(len(dataset[list(dataset)[-1]])):
            stack: List[Node] = [self.root]

            while stack:
                top = stack.pop()

                if not top.children:
                    if top.attribute == dataset[dataset.header[-1]][index]:
                        count_correct += 1
                    matrix[goals.index(dataset[dataset.header[-1]][index])][goals.index(top.attribute)] += 1

                    print('', top.attribute, end='')
                    break

                if dataset[top.attribute][index] not in top.children:
                    d = {i: 0 for i in set(top.dataset[top.dataset.header[-1]])}
                    for i in top.dataset[top.dataset.header[-1]]:
                        d[i] += 1

                    sol = max(sorted(d), key=lambda x: {i: d[i] for i in sorted(d)}[x])
                    stack.append(
                        Node(
                            dataset,
                            top.depth + 1,
                            None,
                            None,
                            sol,
                            {},
                            top,
                            dataset[top.attribute][index]
                        )
                    )
                    continue

                stack.append(top.children[dataset[top.attribute][index]])

        print()
        print(f"[ACCURACY]: {count_correct / len(dataset[dataset.header[-1]]):.5f}")
        print('[CONFUSION_MATRIX]:')
        for i in matrix:
            print(" ".join(str(j) for j in i))


def main():
    args = parse_args()

    a = None
    if args.depth:
        a = ID3(args.depth)
    else:
        a = ID3()

    dataset = csv_parser(args.dataset)
    a.fit(dataset)

    test_dataset = csv_parser(args.test_dataset)
    a.predict(test_dataset)


if __name__ == '__main__':
    main()

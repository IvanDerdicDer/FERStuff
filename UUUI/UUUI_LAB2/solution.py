import argparse
from typing import List, Tuple, Generator, Any
from dataclasses import dataclass
from itertools import combinations

CLAUSE = Tuple


@dataclass
class Clause:
    clause: CLAUSE
    parent1: Any = None
    parent2: Any = None

    def __contains__(self, item):
        return item in self.clause

    def __iter__(self):
        return self.clause.__iter__()

    def __len__(self):
        return len(self.clause)

    def __add__(self, other):
        return Clause(self.clause + other.clause)

    def __eq__(self, other):
        return self.clause == other.clause


CLAUSES = List[Clause]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('operation',
                        type=str,
                        help='Type of ai operation')

    parser.add_argument('clause_path',
                        type=str,
                        help='Path to the clause file')

    parser.add_argument('user_input',
                        type=str,
                        nargs='?',
                        default=None,
                        help='Path to the user input file')

    return parser.parse_args()


def load_file(filepath: str) -> List[str]:
    with open(filepath, 'r') as f:
        to_return = [i.strip().lower() for i in f.readlines() if not i.startswith('#')]

    return to_return


def conjugate(a: str):
    a = '~' + a

    if a.startswith('~~'):
        a = a[2:]

    return a


def negate_clause(clause: Clause) -> CLAUSES:
    to_return = [Clause((conjugate(i),), clause.parent1, clause.parent2) for i in clause]

    return to_return


def remove_duplicates_in_clause(clause: Clause) -> Clause:
    to_return = []
    for c in clause:
        if c not in to_return:
            to_return.append(c)

    return Clause(tuple(to_return), clause.parent1, clause.parent2)


def remove_duplicates_in_clause_list(clause: CLAUSES) -> CLAUSES:
    to_return = []
    for c in clause:
        if c not in to_return:
            to_return.append(c)

    return to_return


def remove_redundant_in_clauses_list(clauses: CLAUSES) -> CLAUSES:
    to_return = clauses.copy()

    for clause in clauses:
        to_remove = []
        if is_sub_clause_in_set(to_return, clause):
            to_remove.append(clause)

        for c in to_remove:
            if c in to_return:
                to_return.remove(c)

    return to_return


def remove_redundant_between(new: CLAUSES, clauses: CLAUSES) -> Tuple[CLAUSES, CLAUSES]:
    to_return_new = new.copy()
    to_return_clauses = clauses.copy()

    to_remove_new = []
    to_remove_clauses = []

    for n in new:
        if is_sub_clause_in_set(clauses, n):
            to_remove_new.append(n)

    for c in clauses:
        if is_sub_clause_in_set(new, c):
            to_remove_clauses.append(c)

    for n in to_remove_new:
        if n in to_return_new:
            to_return_new.remove(n)

    for c in to_remove_clauses:
        if c in to_return_clauses:
            to_return_clauses.remove(c)

    return to_return_new, to_return_clauses


def remove_parents_in_clauses_list(clauses: CLAUSES) -> CLAUSES:
    to_return = clauses.copy()
    to_remove = []

    for clause in clauses:
        if clause.parent1:
            to_remove.append(clause.parent1)

        if clause.parent2:
            to_remove.append(clause.parent2)

    for clause in to_remove:
        if clause in to_return:
            to_return.remove(clause)

    return to_return


def proces_clauses(clauses_raw: List[str]) -> CLAUSES:
    clauses_work: CLAUSES = [remove_duplicates_in_clause(Clause(tuple(i.split(' v ')))) for i in clauses_raw]

    to_process = clauses_work.pop()

    to_return = clauses_work + negate_clause(to_process)

    return to_return


def are_opposite(a: str, b: str) -> bool:
    if not a.startswith('~') and b.startswith('~'):
        return a == b[1:]

    if not b.startswith('~') and a.startswith('~'):
        return b == a[1:]

    return False


def has_opposite(clause: Clause) -> bool:
    for i in clause.clause:
        for j in clause.clause:
            if conjugate(i) == j:
                return True

    return False


def is_sub_clause_in_set(set1: CLAUSES, clause: Clause) -> bool:
    for c in set1:
        if all(i in clause for i in c) and len(clause) > len(c):
            return True

    return False


def put_in_set(set1: CLAUSES, clause: Clause) -> None:
    if not is_sub_clause_in_set(set1, clause):
        set1.append(clause)


def merge2(c1: Clause, c2: Clause, left_on: str) -> Clause:
    if left_on not in c1 or conjugate(left_on) not in c2:
        raise ValueError('Cannot merge on the given key')

    c1_tmp = list(c1)
    c2_tmp = list(c2)

    c1_tmp.remove(left_on)
    c2_tmp.remove(conjugate(left_on))

    return remove_duplicates_in_clause(Clause(tuple(c1_tmp + c2_tmp), c1, c2))


def resolve_all(c1: Clause, c2: Clause) -> CLAUSES:
    to_return = []

    for i in c1:
        if conjugate(i) in c2:
            to_return.append(merge2(c1, c2, i))

    return to_return


def print_solution(solution_clause: Clause):
    stack = [solution_clause]
    stack2 = []

    while stack:
        top = stack.pop()

        if not top.parent1 and not top.parent2:
            continue

        stack2.append(f"{' v '.join(top.parent1)}, {' v '.join(top.parent2)} -> {' v '.join(top)}")

        if top.parent1:
            stack.append(top.parent1)

        if top.parent2:
            stack.append(top.parent2)

    while stack2:
        print(stack2.pop())

    print('----------------------')


def resolver4(clauses: CLAUSES) -> bool:
    clauses_work = clauses.copy()

    new = []

    while True:

        for c1, c2 in combinations(clauses_work.copy(), 2):
            resolvents = resolve_all(c1, c2)

            resolvents = [remove_duplicates_in_clause(i) for i in resolvents if not has_opposite(i)]

            if any(not i for i in resolvents):
                for i in resolvents:
                    if not i:
                        print_solution(i)

                return True

            for i in resolvents:
                put_in_set(new, i)

        if all(i in clauses_work for i in new):
            print_solution(clauses_work[-1])
            return False

        new = remove_redundant_in_clauses_list(new)
        new = remove_duplicates_in_clause_list(new)

        for i in new:
            put_in_set(clauses_work, i)

        clauses_work = remove_redundant_in_clauses_list(clauses_work)
        clauses_work = remove_duplicates_in_clause_list(clauses_work)

        new, clauses_work = remove_redundant_between(new, clauses_work)


def main():
    args = parse_args()

    if args.operation == 'resolution':
        a = load_file(args.clause_path)
        target = a[-1]
        clauses = proces_clauses(a)

        print('\n'.join(' v '.join(i) for i in clauses))

        print('----------------------')

        print(f"[CONCLUSION]: {target} {'is true' if resolver4(clauses) else 'is unknown'}")

    if args.operation == 'cooking':
        clauses = load_file(args.clause_path)
        user_input = load_file(args.user_input)

        for ui in user_input:
            print(f'User command: {ui}')
            if ui.endswith('?'):
                b = clauses + [ui[:-2]]
                b = proces_clauses(b)
                print(f"[CONCLUSION]: {ui[:-2]} {'is true' if resolver4(b) else 'is unknown'}")

            if ui.endswith('-'):
                if ui[:-2] in clauses:
                    clauses.remove(ui[:-2])
                    print(f'Removed {ui[:-2]}')
                else:
                    print(f'Clause {ui[:-2]} does not exist')

            if ui.endswith('+'):
                clauses = [ui[:-2]] + clauses
                print(f'Added {ui[:-2]}')


if __name__ == '__main__':
    main()

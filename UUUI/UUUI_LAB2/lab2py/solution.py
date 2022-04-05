import argparse
from typing import List

CLAUSE = List[str]
CLAUSES = List[CLAUSE]


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


def load_file(filepath: str) -> CLAUSES:
    with open(filepath, 'r') as f:
        to_return = [list(set(i.strip().split(' v ' if ' v ' in i else ' V '))) for i in f.readlines() if
                     not i.startswith('#')]

    return to_return


def conjugate(a: str):
    a = '~' + a

    if a.startswith('~~'):
        a = a[2:]

    return a


def negate_clause(clause: CLAUSE) -> CLAUSES:
    to_return = [[conjugate(i)] for i in clause]

    return to_return


def proces_clauses(clauses_raw: CLAUSES) -> CLAUSES:
    clauses_work = clauses_raw.copy()

    to_process = clauses_work.pop()

    to_return = clauses_work + negate_clause(to_process)

    return to_return


def remove_redundant(clauses: CLAUSES) -> CLAUSES:
    to_return: CLAUSES = clauses.copy()
    redundant: CLAUSES = []

    for i in clauses:
        for j in clauses:
            if len(j) < len(i) and all(k in i for k in j):
                redundant.append(i)

    redundant = list(set(tuple(i) for i in redundant))
    redundant = [list(i) for i in redundant]

    for i in redundant:
        to_return.remove(i)

    return to_return


def are_opposite(a: str, b: str) -> bool:
    if not a.startswith('~') and b.startswith('~'):
        return a == b[1:]

    if not b.startswith('~') and a.startswith('~'):
        return b == a[1:]

    return False


def merge(a: CLAUSE, b: CLAUSE) -> CLAUSE:
    a_work = a.copy()
    b_work = b.copy()

    for i in a_work:
        for j in b_work:
            if are_opposite(i, j):
                a_work.remove(i)
                b_work.remove(j)
                return a_work + b_work

    return []


def has_opposite(clause: CLAUSE) -> bool:
    for i in clause:
        for j in clause:
            if conjugate(i) == j:
                return True

    return False


def resolver(clauses: CLAUSES) -> bool:
    clauses_work = clauses.copy()

    index = 0

    last = list(set(clauses[index]))

    clauses_work.remove(clauses[index])

    previous_last = None

    extra_print = False

    while last:
        if not clauses_work:
            clauses_work += clauses.copy()

        if previous_last == last:
            index += 1
            if index >= len(clauses):
                return False
            last = clauses[index]
            if last in clauses_work:
                clauses_work.remove(last)

        previous_last = last

        stack = []
        for element in last:
            for clause in clauses_work:
                if conjugate(element) in clause:
                    stack.append(clause)
                    break

        while stack:
            top = stack.pop()
            pp_last = last.copy()
            print(f"{' v '.join(last)}, {' v '.join(top)} -> ", end='')
            last = list(set(merge(last, top)))
            if has_opposite(last):
                last = pp_last.copy()
                extra_print = True
                continue

            print(' v '.join(last))
            if top in clauses_work:
                clauses_work.remove(top)

        if extra_print:
            print('')
            extra_print = False

        if not last:
            return True
    else:
        return False


def main():
    args = parse_args()

    if args.operation == 'resolution':
        a = load_file(args.clause_path)
        target = a[-1]
        clauses = remove_redundant(proces_clauses(a))

        for clause in clauses:
            print(' v '.join(clause))

        print(f"[CONCLUSION]: {' v '.join(target)} {'is true' if resolver(clauses) else 'is unknown'}")


if __name__ == '__main__':
    main()

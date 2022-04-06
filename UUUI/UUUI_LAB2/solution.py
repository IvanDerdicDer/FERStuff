import argparse
from typing import List, Tuple, Generator
from collections import deque

CLAUSE = Tuple
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


def load_file(filepath: str) -> List[str]:
    with open(filepath, 'r') as f:
        to_return = [i.strip().lower() for i in f.readlines() if not i.startswith('#')]

    return to_return


def conjugate(a: str):
    a = '~' + a

    if a.startswith('~~'):
        a = a[2:]

    return a


def round_robin_clause(start_index: int, clauses: CLAUSES) -> Generator:
    if start_index not in range(len(clauses)):
        raise IndexError('Index out of range')

    starting_clause = clauses[start_index]

    yield clauses[start_index]
    start_index = (start_index + 1) % len(clauses)

    while starting_clause != clauses[start_index]:
        yield clauses[start_index]
        start_index = (start_index + 1) % len(clauses)


def negate_clause(clause: CLAUSE) -> CLAUSES:
    to_return = [(conjugate(i), ) for i in clause]

    return to_return


def remove_duplicates_in_clause(clause: CLAUSE) -> CLAUSE:
    to_return = []
    for c in clause:
        if c not in to_return:
            to_return.append(c)

    return tuple(to_return)


def remove_duplicates_in_clause_list(clause: CLAUSES) -> CLAUSES:
    to_return = []
    for c in clause:
        if c not in to_return:
            to_return.append(c)

    return to_return


def proces_clauses(clauses_raw: List[str]) -> CLAUSES:
    clauses_work: CLAUSES = [remove_duplicates_in_clause(tuple(i.split(' v '))) for i in clauses_raw]

    to_process = clauses_work.pop()

    to_return = clauses_work + negate_clause(to_process)

    return to_return


def remove_redundant(clauses: CLAUSES) -> CLAUSES:
    to_return: CLAUSES = clauses.copy()
    redundant: CLAUSES = []

    for i in clauses:
        for j in clauses:
            if len(j) < len(i) and all(k in i for k in j):
                if i not in redundant:
                    redundant.append(i)

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
    a_work = list(a)
    b_work = list(b)

    for i in a_work:
        for j in b_work:
            if are_opposite(i, j):
                a_work.remove(i)
                b_work.remove(j)
                return tuple(a_work + b_work)

    return tuple()


def has_opposite(clause: CLAUSE) -> bool:
    for i in clause:
        for j in clause:
            if conjugate(i) == j:
                return True

    return False


def is_sub_clause_in_set(set: List[CLAUSE], clause: CLAUSE) -> bool:
    for c in set:
        if all(i in clause for i in c):
            return True

    return False


def put_in_set(set: List[CLAUSE], clause: CLAUSE) -> None:
    if not is_sub_clause_in_set(set, clause):
        set.append(clause)


def resolver(clauses: CLAUSES, targets: CLAUSES) -> bool:
    # for target in targets:
    clauses_work = clauses.copy()

    index = 0

    clause_sets = [[]]

    to_print = [[]]

    last = remove_duplicates_in_clause(clauses[index])

    clauses_work.remove(clauses[index])

    previous_last = None

    were_used = []

    while last:
        if previous_last == last or not clauses_work:
            were_used = []
            clause_sets.append([])
            to_print.append([])
            clauses_work += clauses.copy()
            clauses_work = remove_duplicates_in_clause_list(list(tuple(i) for i in clauses_work))
            index += 1
            if index >= len(clauses):
                print('\n'.join(to_print[-2]))
                print('----------------------')
                print(f'index {index}, clauses {len(clauses)}')
                return False
            last = clauses[index]
            if last in clauses_work:
                if last not in were_used:
                    were_used.append(last)

        previous_last = last

        stack = deque()
        for element in last:
            for clause in round_robin_clause(index, clauses_work):
                if clause not in were_used:
                    if conjugate(element) in clause:
                        stack.append(clause)
                        break

        while stack:
            top = stack.popleft()
            stack = deque()
            tmp_last = remove_duplicates_in_clause(merge(last, top))
            if top in clauses_work:
                if top not in were_used:
                    were_used.append(top)

            if not has_opposite(tmp_last) and not is_sub_clause_in_set(clause_sets[-1], tmp_last):
                put_in_set(clause_sets[-1], tmp_last)
            else:
                continue

            if tmp_last == clause_sets[-1][-1]:
                to_print[-1].append(f"{' v '.join(last)}, {' v '.join(top)} -> {' v '.join(clause_sets[-1][-1])}")

            last = tmp_last

        if not last:
            print('\n'.join(to_print[-1]))
            print('----------------------')
            print(f'index {index}, clauses {len(clauses)}')
            return True

        print('\n'.join(to_print[-1]))
        print('----------------------')
        print(f'index {index}, clauses {len(clauses)}')
    else:
        print('\n'.join(to_print[-1]))
        print('----------------------')
        print(f'index {index}, clauses {len(clauses)}')
        return False


def resolver2(clauses: CLAUSES):
    clauses_work = clauses.copy()
    clauses_queue = deque(clauses)
    clause_sets = [[]]
    to_print = [[]]
    previous = None

    first = clauses_queue.popleft()
    clauses_work.remove(first)

    while first:
        if previous == first:
            clauses_work = clauses.copy()
            clause_sets.append([])
            to_print.append([])
            if not clauses_queue:
                print('\n'.join(to_print[-2]))
                print('----------------------')
                return False
            first = clauses_queue.popleft()
            clauses_work.remove(first)

        for element in first:
            to_break = False
            for clause in reversed(clauses_work):
                if conjugate(element) in clause:
                    to_break = True
                    tmp_first = remove_duplicates_in_clause(merge(first, clause))

                    clauses_work.remove(clause)

                    if has_opposite(tmp_first):
                        continue

                    put_in_set(clause_sets[-1], tmp_first)

                    if tmp_first == clause_sets[-1][-1]:
                        to_print[-1].append(
                            f"{' v '.join(first)}, {' v '.join(clause)} -> {' v '.join(clause_sets[-1][-1])}")

                    previous = tuple(first)
                    first = tuple(tmp_first)

                    if not first:
                        print('\n'.join(to_print[-1]))
                        print('----------------------')
                        return True

                    break
            if to_break:
                break
        else:
            clauses_work = clauses.copy()
            clause_sets.append([])
            to_print.append([])
            if not clauses_queue:
                print('\n'.join(to_print[-2]))
                print('----------------------')
                return False
            first = clauses_queue.popleft()
            clauses_work.remove(first)

    else:
        print('\n'.join(to_print[-1]))
        print('----------------------')
        return False


def clause_pair_generator(clauses: CLAUSES) -> Generator:
    sent_pairs = []

    for i in clauses:
        for j in clauses:
            if i != j:
                sent = list(i + j)
                sent.sort()
                sent = tuple(sent)

                if sent not in sent_pairs:
                    sent_pairs.append(sent)
                    yield i, j


def merge2(c1: CLAUSE, c2: CLAUSES, left_on: str) -> CLAUSE:
    if left_on not in c1 or conjugate(left_on) not in c2:
        raise ValueError('Cannot merge on the given key')

    c1_tmp = list(c1)
    c2_tmp = list(c2)

    c1_tmp.remove(left_on)
    c2_tmp.remove(conjugate(left_on))

    return remove_duplicates_in_clause(tuple(c1_tmp + c2_tmp))


def resolve_all(c1: CLAUSE, c2: CLAUSES) -> CLAUSES:
    to_return = []

    for i in c1:
        if conjugate(i) in c2:
            to_return.append(merge2(c1, c2, i))

    return to_return


def resolver3(clauses: CLAUSES) -> bool:
    clauses_work = clauses.copy()

    clauses_sets = [[]]
    to_print = [[]]

    while True:
        new = []
        for c1, c2 in clause_pair_generator(clauses_work.copy()):
            resolvents = resolve_all(c1, c2)

            to_remove = []

            for i in resolvents:
                i = remove_duplicates_in_clause(i)
                if has_opposite(i):
                    to_remove.append(i)

            for i in to_remove:
                resolvents.remove(i)

            if resolvents:
                if c2 in clauses_work:
                    clauses_work.remove(c2)

            if any(not i for i in resolvents):
                return True

            for i in resolvents:
                put_in_set(new, i)

        if all(i in clauses_work for i in new):
            return False

        for i in new:
            put_in_set(clauses_work, i)


def main():
    args = parse_args()

    if args.operation == 'resolution':
        a = load_file(args.clause_path)
        target = a[-1]
        clauses = remove_redundant(proces_clauses(a))

        print('\n'.join(a))

        print('----------------------')

        print(f"[CONCLUSION]: {target} {'is true' if resolver3(clauses) else 'is unknown'}")

    if args.operation == 'cooking':
        clauses = load_file(args.clause_path)
        user_input = load_file(args.user_input)

        for ui in user_input:
            print(f'User command: {ui}')
            if ui.endswith('?'):
                b = clauses + [ui[:-2]]
                b = remove_redundant(proces_clauses(b))
                print(f"[CONCLUSION]: {ui[:-2]} {'is true' if resolver3(b) else 'is unknown'}")

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

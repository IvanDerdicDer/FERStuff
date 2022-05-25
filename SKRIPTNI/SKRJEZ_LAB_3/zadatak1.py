from dataclasses import dataclass, field
import argparse
from typing import Tuple

FILE_LINES = list[list[str]]


class MatrixDimensionMissmatch(Exception):
    pass


@dataclass(slots=True)
class Matrix:
    rows: int
    columns: int
    matrix: dict[tuple[int, int], float] = field(default_factory=dict)

    def print(self) -> str:
        to_return = ''

        for i in range(self.rows):
            for j in range(self.columns):
                to_return += f"{self.matrix[(i, j)] if (i, j) in self.matrix else 0:.2f} "
            to_return += '\n'

        return to_return

    def write(self) -> str:
        to_return = f'{self.rows} {self.columns}\n'
        for i in self.matrix:
            to_return += f'{i[0]} {i[1]} {self.matrix[i]}\n'

        return to_return


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()

    p.add_argument('in_file', type=str)
    p.add_argument('out_file', type=str)

    return p.parse_args()


def load_file(filepath: str) -> FILE_LINES:
    with open(filepath, 'r') as f:
        return [i.strip().split() for i in f.readlines()]


def extract_matrices(file_lines: FILE_LINES) -> tuple[Matrix, ...]:
    to_return = []
    for i in file_lines:
        if len(i) == 2:
            to_return.append(Matrix(int(i[0]), int(i[1])))

        if len(i) == 3:
            to_return[-1].matrix[(int(i[0]), int(i[1]))] = float(i[2])

    return tuple(to_return)


def multiply_matrices(m1: Matrix, m2: Matrix) -> Matrix:
    if m1.columns != m2.rows:
        raise MatrixDimensionMissmatch(f"Matrix {m1} has {m1.columns} columns while matrix {m2} has {m2.rows} rows")

    to_return = Matrix(m1.rows, m2.columns)

    for i in range(to_return.rows):
        for j in range(to_return.columns):
            s = 0
            for k in range(m2.rows):
                a = m1.matrix[(i, k)] if (i, k) in m1.matrix else 0
                b = m2.matrix[(k, j)] if (k, j) in m2.matrix else 0
                s += a * b

            if s:
                to_return.matrix[(i, j)] = s

    return to_return


def write_file(filepath: str, content: str) -> None:
    with open(filepath, 'w') as f:
        f.write(content)


def main():
    args = parse_args()

    file = load_file(args.in_file)

    a, b = extract_matrices(file)

    print(f'A:\n{a.print()}')
    print(f'B:\n{b.print()}')

    c = multiply_matrices(a, b)

    print(f'A*B:\n{c.print()}')

    write_file(args.out_file, c.write())


if __name__ == '__main__':
    main()

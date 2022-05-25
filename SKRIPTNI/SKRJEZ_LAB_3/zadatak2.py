import argparse
from decimal import Decimal

FILE_LINES = list[list[str]]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()

    p.add_argument('in_file', type=str)

    return p.parse_args()


def load_file(filepath: str) -> FILE_LINES:
    with open(filepath, 'r') as f:
        return [i.strip().split() for i in f.readlines()]


def process_file(file: FILE_LINES) -> None:
    print('Hyp#Q10#Q20#Q30#Q40#Q50#Q60#Q70#Q80#Q90')
    for line, n in zip(file, range(1, len(file) + 1)):
        line.sort()
        index = Decimal(0.1)

        print(f"{n:3d}#", end='')
        while index < Decimal(0.8):
            print(f"{line[int(len(line) * index) - 1]}#", end='')
            index += Decimal(0.1)
        else:
            index += Decimal(0.1)
            print(f"{line[int(len(line) * index) - 1]}\n", end='')


def main():
    args = parse_args()

    file = load_file(args.in_file)

    process_file(file)


if __name__ == '__main__':
    main()

import argparse
import os
from copy import deepcopy
from dataclasses import dataclass, field

FILE = list[list[str]]


class DuplicateStudentException(Exception):
    pass


def empty_index():
    return [0]


@dataclass
class DataFrame:
    header: list = field(default_factory=list)
    data: dict[str, list] = field(default_factory=dict)

    index: list[int] = field(default_factory=empty_index, init=False)

    def add_row(self, row):
        for i in self.header:
            self.data[i].append(None)

        for i, value in zip(self.header, row):
            self.data[i][-1] = value

        self.index.append(self.index[-1] + 1)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()

    p.add_argument('folder_path', type=str)

    return p.parse_args()


def load_files(folder_path: str) -> tuple[FILE, list[tuple[str, FILE]]]:
    files = os.listdir(folder_path)

    students = []
    labs = []

    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='UTF-8') as f:
                tempfile = [i.strip().split(' ') for i in f.readlines()]

                if file == 'studenti.txt':
                    students = deepcopy(tempfile)
                else:
                    labs.append((file, deepcopy(tempfile)))

    return students, labs


def main():
    args = parse_args()

    students, labs = load_files(args.folder_path)

    grades = DataFrame()
    grades.header = ['JMBAG', 'Ime', 'Prezime', 'L1', 'L2', 'L3']
    grades.data = {i: [] for i in grades.header}

    for student in students:
        grades.add_row(student)

    for lab in labs:
        for s in lab[1]:
            if s[0] in grades.data['JMBAG']:
                index = grades.data['JMBAG'].index(s[0])

                lab_number = 'L' + str(int(lab[0].split('_')[1]))

                if grades.data[lab_number][index]:
                    raise DuplicateStudentException()

                if not grades.data[lab_number][index]:
                    grades.data[lab_number][index] = 0

                grades.data[lab_number][index] += float(s[1])

    print(*grades.header, sep='    ')
    for entry in zip(*grades.data.values()):
        print(*(i if i else "-" for i in entry), sep='    ')


if __name__ == '__main__':
    main()

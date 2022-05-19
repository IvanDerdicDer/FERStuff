import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Union, List, Dict
from copy import deepcopy

NP_ARRAY = np.ndarray
DATASET = Dict[str, List[str]]


@dataclass(frozen=True)
class Dataset:
    header: List[str]
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
        return Dataset(self.header.copy(), deepcopy(self.data))

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

    return Dataset(header, to_return)


class Sigmoid:
    @staticmethod
    def apply(x: NP_ARRAY) -> NP_ARRAY:
        return 1 / (1 + np.exp(x))


class RElU:
    @staticmethod
    def apply(x: NP_ARRAY) -> NP_ARRAY:
        return x * (x > 0)


class NoFunc:
    @staticmethod
    def apply(x: NP_ARRAY) -> NP_ARRAY:
        return x


OUTPUT_FUNCTION = Union[Sigmoid, RElU, NoFunc]


@dataclass
class Layer:
    input_size: int
    number_of_nodes: int
    output_function: OUTPUT_FUNCTION = field(default_factory=Sigmoid)
    weight: Optional[NP_ARRAY] = None
    bias: Optional[NP_ARRAY] = None
    _is_output: bool = False

    def __post_init__(self) -> None:
        if self._is_output:
            self.set_as_output()
            return

        self.weight = np.array(
            [[np.random.normal(scale=0.01) for _ in range(self.input_size)] for _ in range(self.number_of_nodes)]
        )
        self.bias = np.array([np.random.normal(scale=0.01) for _ in range(self.number_of_nodes)])

    def run(self, layer_input: NP_ARRAY) -> NP_ARRAY:
        return self.output_function.apply(np.matmul(self.weight, layer_input) + self.bias)

    def set_as_output(self) -> None:
        self.output_function = NoFunc()

        self._is_output = True

    def mutate(self, std_dev: float, mutation_probability: float) -> None:
        self.weight += np.array(
            [
                [
                    np.random.normal(scale=std_dev) if np.random.random() > mutation_probability else 0 for _ in
                    np.arange(self.input_size)
                ] for _ in np.arange(self.number_of_nodes)
            ]
        )

        self.bias += [
            np.random.normal(scale=std_dev) if np.random.random() > mutation_probability else 0 for _ in
            np.arange(self.number_of_nodes)
        ]


@dataclass
class NeuralNetwork:
    layers: Optional[List[Layer]] = field(default_factory=list)

    def add_layer(self, layer: Layer) -> None:
        self.layers.append(layer)

    def run(self, input_layer: NP_ARRAY) -> NP_ARRAY:
        run_layers = np.array(self.layers)

        tmp_result = input_layer

        for layer in run_layers:
            tmp_result = layer.run(tmp_result)

        return tmp_result[0]

    def mutate(self, std_dev: float, mutation_probability: float) -> None:
        for layer in self.layers:
            layer.mutate(std_dev, mutation_probability)

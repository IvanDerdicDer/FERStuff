import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Union, List, Dict, Tuple, Any
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
import random

NP_ARRAY = np.ndarray
DATASET = Dict[str, List[str]]
LAYER_PARAMETERS = List[Tuple[Tuple[int, int], Dict[str, Any]]]


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
            to_return[header_mapping[index]].append(float(j))

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

        if all((self.weight is None, self.bias is None)):
            self.weight = np.array(
                [[np.random.normal(scale=0.01) for _ in range(self.input_size)] for _ in range(self.number_of_nodes)]
            )

            self.bias = np.array([np.random.normal(scale=0.01) for _ in range(self.number_of_nodes)])

    def run(self, layer_input: NP_ARRAY) -> NP_ARRAY:
        return self.output_function.apply(np.matmul(self.weight, layer_input) + self.bias)

    def set_as_output(self) -> None:
        self.output_function = NoFunc()

        self._is_output = True

    def mutate(self, std_dev: float, mutation_probability: float):
        self.weight *= np.array(
            [
                [
                    1 - (np.random.normal(scale=std_dev) * mutation_probability) for _ in
                    np.arange(self.input_size)
                ] for _ in np.arange(self.number_of_nodes)
            ]
        )

        self.bias += [
            1 - (np.random.normal(scale=std_dev) * mutation_probability) for _ in
            np.arange(self.number_of_nodes)
        ]

        return self


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

    def __copy__(self):
        return NeuralNetwork(self.layers)

    def copy(self):
        return self.__copy__()


GENERATION_RESULTS = List[Tuple[NeuralNetwork, float]]
GENERATION = List[NeuralNetwork]


def calculate_error(output: np.ndarray, expected_output: np.ndarray) -> float:
    return np.sum(np.power((expected_output - output), 2)) / len(output)


def run_network_over_dataset(args: Tuple[NeuralNetwork, Dataset]) -> Tuple[NeuralNetwork, float]:
    network: NeuralNetwork = args[0]
    dataset: Dataset = args[1]
    output = []
    for row in zip(*(dataset[i] for i in dataset.header)):
        output.append(network.run(np.array(row[:-1])))

    return network, calculate_error(np.array(output), np.array(dataset[dataset.header[-1]]))


def run_generation(
        generation: GENERATION,
        datasets: List[Dataset]
) -> GENERATION_RESULTS:
    with ThreadPoolExecutor() as executor:
        results = executor.map(run_network_over_dataset, (i for i in zip(generation, datasets)))

    return [i for i in results]


def breed(network1: NeuralNetwork, network2: NeuralNetwork) -> GENERATION:
    work1 = network1.copy()
    work2 = network2.copy()

    new_layers = []

    l1: Layer
    l2: Layer
    for l1, l2 in zip(work1.layers, work2.layers):
        new_weight = (l1.weight + l2.weight) / 2
        new_bias = (l1.bias + l2.bias) / 2

        new_layers.append(Layer(l1.input_size, l1.number_of_nodes, weight=new_weight, bias=new_bias))

    return [NeuralNetwork(new_layers.copy()), NeuralNetwork(new_layers.copy())]


def construct_new_generation(
        generation: GENERATION_RESULTS,
        elite_number: int,
        std_dev: float,
        mutation_probability: float
) -> GENERATION:
    sorted_generation: GENERATION_RESULTS = [i for i in sorted(generation, key=lambda x: x[1])]

    elites: GENERATION = [i[0] for i in sorted_generation[:elite_number]]
    """rest: GENERATION_RESULTS = sorted_generation[elite_number:]

    rest: GENERATION = [i[0] for i in random.sample(rest, int(len(rest) * 0.10) if int(len(rest) * 0.10) > 0 else 1)]"""

    to_breed = random.sample(elites, 1) + random.sample(elites, 1)

    tmp_generation: GENERATION = []

    while len(tmp_generation) < len(generation):
        tmp_generation += breed(*to_breed)
        to_breed = random.sample(elites, 1) + random.sample(elites, 1)

    if len(tmp_generation) > len(generation):
        tmp_generation = tmp_generation[:len(generation)]

    new_generation = tmp_generation.copy()

    for i in new_generation:
        i.mutate(std_dev, mutation_probability)

    return new_generation


def train(
        generation: GENERATION,
        datasets: List[Dataset],
        epoch: int,
        elite_number: int,
        std_dev: float,
        mutation_probability: float
) -> GENERATION:
    new_generation = generation.copy()

    for i in range(epoch):
        result = run_generation(new_generation, datasets)

        if i % 2000 == 1999:
            print(f"[Train error @{i + 1}]: {min(result, key=lambda x: x[1])[1]:.6f}", )

        new_generation = construct_new_generation(result, elite_number, std_dev, mutation_probability)

    return new_generation


def main():
    train_dataset = csv_parser('sine_train.txt')
    test_dataset = csv_parser('sine_test.txt')

    generation_size = 10

    layer_parameters = [
        ((1, 5), {'output_function': RElU}),
        ((5, 5), {'output_function': RElU}),
        ((5, 1), {'_is_output': True})
    ]

    generation = [NeuralNetwork([Layer(*(i[0]), **(i[1])) for i in layer_parameters]) for _ in range(generation_size)]
    datasets = [train_dataset.copy() for _ in range(generation_size)]

    result = train(generation, datasets, 10000, 2, 0.1, 0.1)

    result = run_generation(result, [test_dataset.copy() for _ in range(generation_size)])

    best = min(result, key=lambda x: x[1])[0]

    result = run_generation([best], [test_dataset])

    print(f"[Test error]: {min(result, key=lambda x: x[1])[1]:.6f}")


if __name__ == '__main__':
    main()
